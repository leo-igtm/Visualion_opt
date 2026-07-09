from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Backend.database.dbconnections_opt import get_db
from Backend.Models.optica import Venta, Producto, DetalleVenta, OrdenTrabajo, EstadoOrden
from Backend.Models.Usuarios import Paciente, Vendedor
from Backend.Models.clinica import RecetaMedica
from Backend.Schemas import optica as schemas
from Backend.patterns.strategy import PaymentStrategyFactory

router = APIRouter(prefix="/optica", tags=["Optica - Ventas y Productos"])


@router.post("/ventas/", response_model=schemas.VentaResponse, status_code=status.HTTP_201_CREATED)
async def crear_venta(venta_in: schemas.VentaCreate, db: AsyncSession = Depends(get_db)):
    query_paciente = select(Paciente).where(Paciente.id == venta_in.paciente_id)
    resultado_paciente = await db.execute(query_paciente)
    if not resultado_paciente.scalars().first():
        raise HTTPException(status_code=404, detail=f"Paciente con ID {venta_in.paciente_id} no encontrado")

    query_vendedor = select(Vendedor).where(Vendedor.id == venta_in.vendedor_id)
    resultado_vendedor = await db.execute(query_vendedor)
    if not resultado_vendedor.scalars().first():
        raise HTTPException(status_code=404, detail=f"Vendedor con ID {venta_in.vendedor_id} no encontrado")

    if venta_in.receta_id is not None:
        query_receta = select(RecetaMedica).where(RecetaMedica.uuid == venta_in.receta_id)
        resultado_receta = await db.execute(query_receta)
        if not resultado_receta.scalars().first():
            raise HTTPException(status_code=404, detail=f"Receta con ID {venta_in.receta_id} no encontrada")

    if venta_in.estado_pago not in PaymentStrategyFactory.get_available_payment_states():
        raise HTTPException(status_code=400, detail=f"Estado de pago no soportado: {venta_in.estado_pago}")

    nueva_venta = Venta(
        numeroComprobante=venta_in.numero_comprobante,
        estado_pago=venta_in.estado_pago,
        total=0.0,
        paciente_id=venta_in.paciente_id,
        vendedor_id=venta_in.vendedor_id,
        receta_id=venta_in.receta_id,
    )
    db.add(nueva_venta)

    await db.flush()

    nueva_orden = OrdenTrabajo(
        venta_id=nueva_venta.id,
        estado=EstadoOrden.RECIBIDA,
    )
    db.add(nueva_orden)

    total_venta = 0.0

    for item in venta_in.items:
        query_prod = select(Producto).where(Producto.id == item.producto_id)
        resultado_prod = await db.execute(query_prod)
        db_producto = resultado_prod.scalars().first()

        if not db_producto:
            await db.rollback()
            raise HTTPException(status_code=404, detail=f"Producto con ID {item.producto_id} no encontrado")

        if db_producto.stockDisponible < item.cantidad:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{db_producto.tipoNombre}'. Disponibles: {db_producto.stockDisponible}",
            )

        db_producto.stockDisponible -= item.cantidad
        precio_historico = db_producto.precio
        total_venta += precio_historico * item.cantidad

        detalle_venta = DetalleVenta(
            venta_id=nueva_venta.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=precio_historico,
        )
        db.add(detalle_venta)

    nueva_venta.total = total_venta

    try:
        await db.commit()
        await db.refresh(nueva_venta)
        return nueva_venta
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar la venta: {str(e)}")


@router.post("/productos/", response_model=schemas.ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto_in: schemas.ProductoCreate, db: AsyncSession = Depends(get_db)):
    query_sku = select(Producto).where(Producto.sku == producto_in.sku)
    resultado_sku = await db.execute(query_sku)
    if resultado_sku.scalars().first():
        raise HTTPException(status_code=400, detail="El SKU ya esta registrado.")

    nuevo_producto = Producto(
        sku=producto_in.sku,
        tipoNombre=producto_in.tipoNombre,
        precio=producto_in.precio,
        stockDisponible=producto_in.stockDisponible,
    )
    db.add(nuevo_producto)
    try:
        await db.commit()
        await db.refresh(nuevo_producto)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    return nuevo_producto
