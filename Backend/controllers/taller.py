from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..database.dbconnections_opt import get_db
from ..Models import optica as models
from ..Models.optica import Venta, OrdenTrabajo, EtapaTrabajo, HistoricoEstado
from ..Models.Usuarios import Tecnico
from ..Schemas import taller as schemas
from ..validators.taller_validators import OrdenTrabajoValidator
from ..patterns.observer import Event
from ..services.event_service import EventService
from ..services.orden_service import OrdenService
from pydantic import ValidationError
from typing import List, Any

router = APIRouter(prefix="/taller", tags=["Taller y Laboratorio"])

# Obtener sujeto de eventos global
orden_subject = EventService.get_orden_subject()


@router.post("/ordenes", response_model=schemas.OrdenTrabajoResponse, status_code=status.HTTP_201_CREATED)
async def crear_orden_trabajo(orden_in: schemas.OrdenTrabajoCreate, db: AsyncSession = Depends(get_db)) -> OrdenTrabajo:
    """Create a new work order from a sale"""
    try:
        # Validación 1: Verificar que la venta exista
        query_venta = select(Venta).where(Venta.id == orden_in.venta_id)
        resultado_venta = await db.execute(query_venta)
        db_venta = resultado_venta.scalars().first()
        if not db_venta:
            raise HTTPException(status_code=404, detail=f"Venta con ID {orden_in.venta_id} no encontrada")

        # Validación 2: Verificar que no exista otra orden para esta venta
        query_orden_existente = select(OrdenTrabajo).where(OrdenTrabajo.venta_id == orden_in.venta_id)
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

        # CORRECCIÓN BUG #3: serializar estado como string explícito
        event = Event(
            event_type="orden_creada",
            data={
                "orden_id": nueva_orden.id,
                "venta_id": nueva_orden.venta_id,
                "estado": nueva_orden.estado
            }
        )
        orden_subject.notify(event)

        return nueva_orden

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/ordenes", response_model=list[schemas.OrdenTrabajoResponse])
async def listar_ordenes_trabajo(
    estado: str | None = None,
    tecnico_id: int | None = None,
    db: AsyncSession = Depends(get_db)
) -> List[OrdenTrabajo]:
    """List all work orders with optional filters"""
    query = select(OrdenTrabajo).options(
        selectinload(OrdenTrabajo.etapas),
        selectinload(OrdenTrabajo.historico_estados)
    )

    if estado:
        query = query.where(OrdenTrabajo.estado == models.EstadoOrden(estado))

    if tecnico_id is not None:
        query = query.join(EtapaTrabajo).where(EtapaTrabajo.tecnico_id == tecnico_id).distinct()

    resultado = await db.execute(query)
    return list(resultado.scalars().all())


@router.get("/ordenes/{orden_id}", response_model=schemas.OrdenTrabajoResponse)
async def obtener_orden_trabajo(orden_id: int, db: AsyncSession = Depends(get_db)) -> OrdenTrabajo:
    """Get order details with all stages and history"""
    query = select(OrdenTrabajo).where(OrdenTrabajo.id == orden_id).options(
        selectinload(OrdenTrabajo.etapas),
        selectinload(OrdenTrabajo.historico_estados)
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
) -> OrdenTrabajo:
    """Update order state with validation and notify observers"""
    # CORRECCIÓN BUG #1: Cargar relaciones desde el principio para el response
    query = select(OrdenTrabajo).where(OrdenTrabajo.id == orden_id).options(
        selectinload(OrdenTrabajo.etapas),
        selectinload(OrdenTrabajo.historico_estados)
    )
    resultado = await db.execute(query)
    db_orden = resultado.scalars().first()
    if not db_orden:
        raise HTTPException(status_code=404, detail=f"Orden con ID {orden_id} no encontrada")

    try:
        estado_nuevo_enum = models.EstadoOrden(datos.estado_nuevo)
    except ValueError:
        raise HTTPException(status_code=422, detail=f"'{datos.estado_nuevo}' no es un estado válido.")

    # Validar transición
    es_valida, mensaje_error = OrdenTrabajoValidator.validar_transicion(db_orden, estado_nuevo_enum)
    if not es_valida:
        raise HTTPException(status_code=400, detail=mensaje_error)

    # Validar técnico si se proporciona
    if datos.tecnico_id:
        query_tecnico = select(Tecnico).where(Tecnico.id == datos.tecnico_id)
        resultado_tecnico = await db.execute(query_tecnico)
        db_tecnico = resultado_tecnico.scalars().first()
        if not db_tecnico:
            raise HTTPException(status_code=404, detail=f"Técnico con ID {datos.tecnico_id} no encontrado")

    estado_anterior = db_orden.estado

    # CORRECCIÓN BUG #2: Primero agregar ambos cambios (estado + histórico) y commitear JUNTOS
    db_orden.estado = estado_nuevo_enum

    historico = HistoricoEstado(
        orden_id=orden_id,
        estado_anterior=estado_anterior,
        estado_nuevo=estado_nuevo_enum,
        tecnico_id=datos.tecnico_id
    )
    db.add(historico)
    db.add(db_orden)

    try:
        await db.commit()
        await db.refresh(db_orden)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

    # Notificar cambio de estado a observadores
    event = Event(
        event_type="orden_estado_cambio",
        data={
            "orden_id": orden_id,
            "estado_anterior": estado_anterior,
            "estado_nuevo": estado_nuevo_enum,
            "tecnico_id": datos.tecnico_id,
            "venta_id": db_orden.venta_id
        }
    )
    orden_subject.notify(event)

    return db_orden


@router.put("/ordenes/{orden_id}/etapa", response_model=schemas.EtapaTrabajoResponse)
async def actualizar_etapa_trabajo(
    orden_id: int,
    etapa_in: schemas.EtapaTrabajoCreate,  # CORRECCIÓN BUG #6: ya no lleva orden_id en body
    db: AsyncSession = Depends(get_db)
) -> EtapaTrabajo:
    """Mark a production stage as complete"""
    # Verificar que la orden existe
    query_orden = select(OrdenTrabajo).where(OrdenTrabajo.id == orden_id)
    resultado_orden = await db.execute(query_orden)
    if not resultado_orden.scalars().first():
        raise HTTPException(status_code=404, detail=f"Orden con ID {orden_id} no encontrada")

    # Validar técnico si se proporciona
    if etapa_in.tecnico_id:
        query_tecnico = select(Tecnico).where(Tecnico.id == etapa_in.tecnico_id)
        resultado_tecnico = await db.execute(query_tecnico)
        db_tecnico = resultado_tecnico.scalars().first()
        if not db_tecnico:
            raise HTTPException(status_code=404, detail=f"Técnico con ID {etapa_in.tecnico_id} no encontrado")

    # Buscar o crear etapa
    query = select(EtapaTrabajo).where(
        EtapaTrabajo.orden_id == orden_id,
        EtapaTrabajo.etapa == etapa_in.etapa
    )
    resultado = await db.execute(query)
    db_etapa = resultado.scalars().first()

    if db_etapa:
        db_etapa.tecnico_id = etapa_in.tecnico_id
        db_etapa.completado = etapa_in.completado
        if etapa_in.notas:
            db_etapa.notas = etapa_in.notas
    else:
        db_etapa = EtapaTrabajo(
            orden_id=orden_id,
            etapa=etapa_in.etapa,
            tecnico_id=etapa_in.tecnico_id,
            completado=etapa_in.completado,
            notas=etapa_in.notas
        )
        db.add(db_etapa)

    try:
        await db.commit()
        await db.refresh(db_etapa)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

    # Notificar completación de etapa
    event = Event(
        event_type="etapa_completada",
        data={
            "orden_id": orden_id,
            "etapa": etapa_in.etapa,
            "completado": etapa_in.completado,
            "tecnico_id": etapa_in.tecnico_id
        }
    )
    orden_subject.notify(event)

    return db_etapa


@router.get("/ordenes/{orden_id}/historico", response_model=list[schemas.HistoricoEstadosResponse])
async def obtener_historico_estados(orden_id: int, db: AsyncSession = Depends(get_db)) -> List[HistoricoEstado]:
    """Get audit trail of all state transitions"""
    query = select(OrdenTrabajo).where(OrdenTrabajo.id == orden_id)
    resultado = await db.execute(query)
    db_orden = resultado.scalars().first()
    if not db_orden:
        raise HTTPException(status_code=404, detail=f"Orden con ID {orden_id} no encontrada")

    query_historico = select(HistoricoEstado).where(
        HistoricoEstado.orden_id == orden_id
    ).order_by(HistoricoEstado.fecha_creacion.desc())
    resultado_historico = await db.execute(query_historico)
    return list(resultado_historico.scalars().all())


@router.get("/ordenes-composite/{numero_orden}/resumen")
async def obtener_resumen_orden_composite(numero_orden: str) -> dict[str, Any]:
    """Obtiene resumen de orden usando Composite Pattern (demo)"""
    orden = OrdenService.crear_orden_estandar(numero_orden)
    return OrdenService.calcular_resumen(orden)


@router.post("/ordenes-composite/crear-personalizada")
async def crear_orden_personalizada(
    numero_orden: str,
    etapas: List[schemas.EtapaOrdenData]
) -> dict[str, Any]:
    """Crea orden personalizada usando Composite Pattern"""
    try:
        orden = OrdenService.crear_orden_personalizada(numero_orden, etapas)
        return OrdenService.calcular_resumen(orden)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
