from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from Backend.database.dbconnections_opt import get_db
from Backend.Models import taller as models
from Backend.Models.optica import Venta
from Backend.Models.Usuarios import Tecnico
from Backend.Schemas import taller as schemas
from Backend.validators.taller_validators import OrdenTrabajoValidator
from pydantic import ValidationError

router = APIRouter(prefix="/taller", tags=["Taller y Laboratorio"])


@router.post("/ordenes", response_model=schemas.OrdenTrabajoResponse, status_code=status.HTTP_201_CREATED)
async def crear_orden_trabajo(orden_in: schemas.OrdenTrabajoCreate, db: AsyncSession = Depends(get_db)):
    """Create a new work order from a sale"""
    try:
        # Validación 1: Verificar que la venta exista
        query_venta = select(Venta).where(Venta.id == orden_in.venta_id)
        resultado_venta = await db.execute(query_venta)
        db_venta = resultado_venta.scalars().first()
        if not db_venta:
            raise HTTPException(status_code=404, detail=f"Venta con ID {orden_in.venta_id} no encontrada")

        # Validación 2: Verificar que no exista otra orden para esta venta
        query_orden_existente = select(models.OrdenTrabajo).where(models.OrdenTrabajo.venta_id == orden_in.venta_id)
        resultado_orden = await db.execute(query_orden_existente)
        orden_existente = resultado_orden.scalars().first()
        if orden_existente:
            raise HTTPException(status_code=400, detail=f"Ya existe una orden de trabajo para la venta {orden_in.venta_id}")

        # Crear la orden
        nueva_orden = models.OrdenTrabajo(
            venta_id=orden_in.venta_id,
            estado=models.EstadoOrden.RECIBIDA,
            descripcion_trabajo=orden_in.descripcion_trabajo,
            fecha_entrega_esperada=orden_in.fecha_entrega_esperada
        )
        db.add(nueva_orden)
        await db.commit()
        await db.refresh(nueva_orden)
        return nueva_orden

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/ordenes", response_model=list[schemas.OrdenTrabajoResponse])
async def listar_ordenes_trabajo(
    estado: str | None = None,
    tecnico_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    """List all work orders with optional filters"""
    query = select(models.OrdenTrabajo).options(
        selectinload(models.OrdenTrabajo.etapas),
        selectinload(models.OrdenTrabajo.historico_estados)
    )

    if estado:
        query = query.where(models.OrdenTrabajo.estado == estado)

    if tecnico_id is not None:
        query = query.join(models.EtapaTrabajo).where(models.EtapaTrabajo.tecnico_id == tecnico_id).distinct()

    resultado = await db.execute(query)
    return resultado.scalars().all()


@router.get("/ordenes/{orden_id}", response_model=schemas.OrdenTrabajoResponse)
async def obtener_orden_trabajo(orden_id: int, db: AsyncSession = Depends(get_db)):
    """Get order details with all stages and history"""
    query = select(models.OrdenTrabajo).where(models.OrdenTrabajo.id == orden_id).options(
        selectinload(models.OrdenTrabajo.etapas),
        selectinload(models.OrdenTrabajo.historico_estados)
    )
    resultado = await db.execute(query)
    db_orden = resultado.scalars().first()
    if not db_orden:
        raise HTTPException(status_code=404, detail=f"Orden con ID {orden_id} no encontrada")
    return db_orden


@router.put("/ordenes/{orden_id}/estado", response_model=schemas.OrdenTrabajoResponse)
async def cambiar_estado_orden(
    orden_id: int,
    datos: schemas.CambiarEstadoOrden,
    db: AsyncSession = Depends(get_db)
):
    """Update order state with validation"""
    # Obtener la orden
    query = select(models.OrdenTrabajo).where(models.OrdenTrabajo.id == orden_id)
    resultado = await db.execute(query)
    db_orden = resultado.scalars().first()
    if not db_orden:
        raise HTTPException(status_code=404, detail=f"Orden con ID {orden_id} no encontrada")

    # Validar transición
    es_valida, mensaje_error = OrdenTrabajoValidator.validar_transicion(db_orden, datos.estado_nuevo)
    if not es_valida:
        raise HTTPException(status_code=400, detail=mensaje_error)

    # Validar técnico si se proporciona
    if datos.tecnico_id:
        query_tecnico = select(Tecnico).where(Tecnico.id == datos.tecnico_id)
        resultado_tecnico = await db.execute(query_tecnico)
        db_tecnico = resultado_tecnico.scalars().first()
        if not db_tecnico:
            raise HTTPException(status_code=404, detail=f"Técnico con ID {datos.tecnico_id} no encontrado")

    # Actualizar estado
    estado_anterior = db_orden.estado
    db_orden.estado = datos.estado_nuevo

    # Registrar en histórico
    historico = models.HistoricoEstados(
        orden_id=orden_id,
        estado_anterior=estado_anterior,
        estado_nuevo=datos.estado_nuevo,
        tecnico_id=datos.tecnico_id
    )
    db.add(historico)
    db.add(db_orden)
    await db.commit()
    await db.refresh(db_orden)
    return db_orden


@router.put("/ordenes/{orden_id}/etapa", response_model=schemas.EtapaTrabajoResponse)
async def actualizar_etapa_trabajo(
    orden_id: int,
    etapa_in: schemas.EtapaTrabajoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Mark a production stage as complete"""
    # Validar técnico si se proporciona
    if etapa_in.tecnico_id:
        query_tecnico = select(Tecnico).where(Tecnico.id == etapa_in.tecnico_id)
        resultado_tecnico = await db.execute(query_tecnico)
        db_tecnico = resultado_tecnico.scalars().first()
        if not db_tecnico:
            raise HTTPException(status_code=404, detail=f"Técnico con ID {etapa_in.tecnico_id} no encontrado")

    # Buscar o crear etapa
    query = select(models.EtapaTrabajo).where(
        models.EtapaTrabajo.orden_id == orden_id,
        models.EtapaTrabajo.etapa == etapa_in.etapa
    )
    resultado = await db.execute(query)
    db_etapa = resultado.scalars().first()

    if db_etapa:
        db_etapa.tecnico_id = etapa_in.tecnico_id
        db_etapa.completado = etapa_in.completado
        if etapa_in.notas:
            db_etapa.notas = etapa_in.notas
    else:
        db_etapa = models.EtapaTrabajo(
            orden_id=orden_id,
            etapa=etapa_in.etapa,
            tecnico_id=etapa_in.tecnico_id,
            completado=etapa_in.completado,
            notas=etapa_in.notas
        )
        db.add(db_etapa)

    await db.commit()
    await db.refresh(db_etapa)
    return db_etapa


@router.get("/ordenes/{orden_id}/historico", response_model=list[schemas.HistoricoEstadosResponse])
async def obtener_historico_estados(orden_id: int, db: AsyncSession = Depends(get_db)):
    """Get audit trail of all state transitions"""
    # Validar que la orden existe
    query = select(models.OrdenTrabajo).where(models.OrdenTrabajo.id == orden_id)
    resultado = await db.execute(query)
    db_orden = resultado.scalars().first()
    if not db_orden:
        raise HTTPException(status_code=404, detail=f"Orden con ID {orden_id} no encontrada")

    # Obtener histórico ordenado por fecha descendente
    query_historico = select(models.HistoricoEstados).where(
        models.HistoricoEstados.orden_id == orden_id
    ).order_by(models.HistoricoEstados.fecha_creacion.desc())
    resultado_historico = await db.execute(query_historico)
    return resultado_historico.scalars().all()
