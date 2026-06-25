from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

'''
Esquemas Pydantic para el módulo de Óptica.

Estos esquemas validan y serializan los datos para productos, ventas y sus detalles,
asegurando la integridad de los datos en las operaciones de la API.
'''

class ProductoBase(BaseModel):
    sku: str
    tipoNombre: str
    precio: float
    stockDisponible: int

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    '''Esquema para la respuesta de un producto, incluyendo su ID.'''
    id: int

    class Config:
        # Permite crear el esquema desde un modelo ORM.
        from_attributes = True

''' Esquema para representar la información básica de una venta, incluyendo el número de comprobante, el ID del vendedor, el ID del paciente, el ID de la receta (si aplica) y el estado del pago. Este esquema se utiliza para validar la información al crear una nueva venta.
Incluye un valor por defecto para el estado del pago, que se establece como "pendiente" al crear una nueva venta.'''
class DetalleVentaBase(BaseModel):
    producto_id: int
    cantidad: int

class DetalleVentaCreate(DetalleVentaBase):
    pass


class DetalleVentaResponse(BaseModel):
    '''Esquema para la respuesta de un detalle de venta.'''
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

    class Config:
        # Permite crear el esquema desde un modelo ORM.
        from_attributes = True

class VentaBase(BaseModel):
    '''
    Esquema base para una venta.
    Define los campos comunes para la creación y respuesta de ventas.
    '''
    # Se usa alias para mantener 'numeroComprobante' en el JSON, pero 'numero_comprobante' en Python.
    numero_comprobante: str = Field(..., alias="numeroComprobante")
    vendedor_id: int
    paciente_id: int
    receta_id: Optional[int] = None
    estado_pago: str = "pendiente"  # Valor por defecto

class VentaCreate(VentaBase):
    '''Esquema para crear una nueva venta, incluyendo los items.'''
    items: List[DetalleVentaCreate]

class VentaResponse(VentaBase):
    '''Esquema para la respuesta de una venta, con todos sus detalles.'''
    id: int
    fecha_creacion: datetime
    total: float
    items: List[DetalleVentaResponse]

    class Config:
        from_attributes = True
        populate_by_name = True # Permite usar el alias en la creación del objeto