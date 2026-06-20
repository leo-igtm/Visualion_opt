from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

''' Esquemas para representar los datos de productos, ventas y detalles de venta en el módulo de óptica. Estos esquemas se utilizan para validar la información al crear o actualizar productos y ventas, así como para serializar la información al responder a las solicitudes de la API.'''
class ProductoBase(BaseModel):
    sku: str
    tipoNombre: str
    precio: float
    stockDisponible: int
''' Esquema para representar la respuesta de un producto, incluyendo su ID. Este esquema se utiliza para serializar la información del producto al responder a las solicitudes de la API.'''
class ProductoCreate(ProductoBase):
    pass
''' Esquema para representar la respuesta de un producto, incluyendo su ID. Este esquema se utiliza para serializar la información del producto al responder a las solicitudes de la API.'''
'''class config se utiliza para indicar que los datos pueden ser creados a partir de atributos de objetos, lo que facilita la conversión de modelos de base de datos a esquemas de Pydantic.'''
class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True

''' Esquema para representar la información básica de una venta, incluyendo el número de comprobante, el ID del vendedor, el ID del paciente, el ID de la receta (si aplica) y el estado del pago. Este esquema se utiliza para validar la información al crear una nueva venta.
Incluye un valor por defecto para el estado del pago, que se establece como "pendiente" al crear una nueva venta.'''
class DetalleVentaBase(BaseModel):
    producto_id: int
    cantidad: int

''' Esquema para representar la información de un detalle de venta, incluyendo el ID del producto, la cantidad vendida y el precio unitario. Este esquema se utiliza para serializar la información del detalle de venta al responder a las solicitudes de la API.'''

class DetalleVentaCreate(DetalleVentaBase):
    pass


class DetalleVentaResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

    class Config:
        from_attributes = True

''' Esquema para representar la información básica de una venta, incluyendo el número de comprobante, el ID del vendedor, el ID del paciente, el ID de la receta (si aplica) y el estado del pago. Este esquema se utiliza para validar la información al crear una nueva venta.
Incluye un valor por defecto para el estado del pago, que se establece como "pendiente" al crear una nueva venta.'''
class VentaBase(BaseModel):
    numeroComprobante: str
    vendedor_id: int
    paciente_id: int
    receta_id: Optional[int] = None
    estado_pago: str = "pendiente"  # Valor por defecto
    
    
''' Esquema para representar la información de una venta, incluyendo su ID, fecha de creación, total y detalles de venta asociados. Este esquema se utiliza para serializar la información de la venta al responder a las solicitudes de la API.
Incluye un valor por defecto para el estado del pago, que se establece como "pendiente" al crear una nueva venta.'''
class VentaCreate(VentaBase):
    items: List[DetalleVentaCreate]

''' Esquema para representar la información de una venta, incluyendo su ID, fecha de creación, total y detalles de venta asociados. Este esquema se utiliza para serializar la información de la venta al responder a las solicitudes de la API.'''
class VentaResponse(VentaBase):
    id: int
    fecha_creacion: datetime
    total: float
    items: List[DetalleVentaResponse]

    class Config:
        from_attributes = True