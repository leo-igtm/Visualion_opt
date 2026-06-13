from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

# Ajusta estos imports a tu proyecto
from Backend.database.dbconnections_opt import get_db 
from Backend.Models import optica as models
from Backend.Schemas import optica as schemas

router = APIRouter(prefix="/optica", tags=["Óptica - Ventas y Productos"])


@router.post("/ventas/", response_model=schemas.VentaResponse, status_code=status.HTTP_201_CREATED)
async def crear_venta(venta_in: schemas.VentaCreate, db: AsyncSession = Depends(get_db)):
    
    # 1. Creamos la cabecera de la venta
    nueva_venta = models.Venta(
        numeroComprobante=venta_in.numeroComprobante,
        fecha_creacion=datetime.now(),
        estado_pago=venta_in.estado_pago,
        total=0.0,
        paciente_id=venta_in.paciente_id,
        vendedor_id=venta_in.vendedor_id,
        receta_id=venta_in.receta_id
    )
    db.add(nueva_venta)
    
    # MUY IMPORTANTE: await en el flush para que la BD nos devuelva el 'id' de la venta
    await db.flush()  

    total_venta = 0.0

    # 2. Iteramos los productos
    for item in venta_in.items:
        # CONSULTA ASÍNCRONA: Igual que hiciste con el DNI del paciente
        query_prod = select(models.Producto).where(models.Producto.id == item.producto_id)
        resultado_prod = await db.execute(query_prod)
        db_producto = resultado_prod.scalars().first()
        
        # Validaciones con rollback asíncrono
        if not db_producto:
            await db.rollback()
            raise HTTPException(status_code=404, detail=f"Producto con ID {item.producto_id} no encontrado")
            
        if db_producto.stockDisponible < item.cantidad:
            await db.rollback()
            raise HTTPException(
                status_code=400, 
                detail=f"Stock insuficiente para '{db_producto.tipoNombre}'. Disponibles: {db_producto.stockDisponible}"
            )

        # 3. Descontamos stock y sumamos al total
        db_producto.stockDisponible -= item.cantidad
        precio_historico = db_producto.precio
        total_venta += precio_historico * item.cantidad

        # 4. Creamos el detalle (renglón)
        detalle_venta = models.DetalleVenta(
            venta_id=nueva_venta.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=precio_historico
        )
        db.add(detalle_venta)

    # Actualizamos el total real
    nueva_venta.total = total_venta

    try:
        # Guardamos definitivamente en la base de datos
        await db.commit()
        await db.refresh(nueva_venta)
        return nueva_venta
    except Exception as e:        
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar la venta: {str(e)}")



@router.post("/productos/", response_model=schemas.ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto_in: schemas.ProductoCreate, db: AsyncSession = Depends(get_db)):
    #validacion crear producto
    query_sku = select(models.Producto).where(models.Producto.sku == producto_in.sku)
    resultado_sku = await db.execute(query_sku)
    if resultado_sku.scalars().first():
        raise HTTPException(status_code=400, detail="El SKU ya está registrado.")

    
    nuevo_producto = models.Producto(
        sku=producto_in.sku,
        tipoNombre=producto_in.tipoNombre,
        precio=producto_in.precio,
        stockDisponible=producto_in.stockDisponible
    )
    db.add(nuevo_producto)
    await db.commit()
    await db.refresh(nuevo_producto)
    return nuevo_producto