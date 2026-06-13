from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class ProductoBase(BaseModel):
    sku: str
    tipoNombre: str
    precio: float
    stockDisponible: int

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True

class DetalleVentaBase(BaseModel):
    producto_id: int
    cantidad: int


class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

    class Config:
        from_attributes = True

class VentaBase(BaseModel):
    numeroComprobante: str
    vendedor_id: int
    paciente_id: int
    receta_id: Optional[int] = None
    estado_pago: str = "pendiente"  # Valor por defecto
    
class VentaCreate(VentaBase):
    items: List[DetalleVentaCreate]


class VentaResponse(VentaBase):
    id: int
    fecha_creacion: datetime
    total: float
    items: List[DetalleVentaResponse]

    class Config:
        from_attributes = True