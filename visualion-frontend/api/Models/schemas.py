from pydantic import BaseModel, field_validator, ValidationError
from datetime import datetime,str,float,int
from models import Producto, RecetaMedica

class ProductoSchema(BaseModel):
    sku: str
    tipo_producto: str
    precio: int
    stock_disponible: int

    #validaciones estilo setters y getters para cada campo del producto
    @field_validator('precio')

    def validate_precio(cls, value):
        if value < 0:
            raise ValueError('El precio no puede ser negativo')
        return value
    
    @field_validator('stock_disponible')
    def validate_stock(cls, value):
        if value < 0:
            raise ValueError('El stock disponible no puede ser negativo')
        return value
    
    @field_validator('sku')
    def validate_sku(cls, value):
        if not value:
            raise ValueError('El SKU no puede estar vacío')
        return value
    
    @field_validator('tipo_producto')
    def validate_tipo_producto(cls, value):
        if not value:
            raise ValueError('El tipo de producto no puede estar vacío')
        return value
    
    def __repr__(self):
        return f"<Producto(sku='{self.sku}', tipo_producto='{self.tipo_producto}', precio='{self.precio}', stock_disponible='{self.stock_disponible}')>"
    
    def to_dict(self):
        return {
            "sku": self.sku,
            "tipo_producto": self.tipo_producto,
            "precio": self.precio,
            "stock_disponible": self.stock_disponible
        }



class RecetaMedicaSchema(BaseModel):
    uuid: str
    paciente_id: str
    medico_id: str
    fecha_emision: datetime
    fecha_vencimiento: datetime
    odEsfera: float
    odAdicion: float
    odCilindro: float
    odEje: float
    oiEsfera: float
    oiAdicion: float
    oiCilindro: float
    oiEje: float
    distancia_pupilar: float
    Tipolente: str


    # Getters y setters para cada campo de la receta médica
    @field_validator('uuid')
    def validate_uuid(cls, value):
        if not value:
            raise ValueError('El UUID no puede estar vacío')
        return value
    @field_validator('paciente_id')
    def validate_paciente_id(cls, value):
        if not value:
            raise ValueError('El ID del paciente no puede estar vacío')
        return value
    @field_validator('medico_id')
    def validate_medico_id(cls, value):
        if not value:
            raise ValueError('El ID del médico no puede estar vacío')
        return value
    @field_validator('fecha_emision')
    def validate_fecha_emision(cls, value):
        if value > datetime.now():
            raise ValueError('La fecha de emisión no puede ser en el futuro')
        return value
    @field_validator('fecha_vencimiento')
    def validate_fecha_vencimiento(cls, value):
        if value < datetime.now():
            raise ValueError('La fecha de vencimiento no puede ser en el pasado')
        return value
    @field_validator('odEsfera', 'odAdicion', 'odCilindro', 'odEje', 'oiEsfera', 'oiAdicion', 'oiCilindro', 'oiEje', 'distancia_pupilar')
    def validate_float_fields(cls, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Este campo debe ser un número')
        return float(value)
    @field_validator('Tipolente')
    def validate_Tipolente(cls, value):
        if not value:
            raise ValueError('El tipo de lente no puede estar vacío')
        return value
    def  __repr__(self):
        return f"<RecetaMedica(uuid='{self.uuid}', paciente_id='{self.paciente_id}', medico_id='{self.medico_id}')>"
    
    def to_dict(self):
        return {
            "uuid": self.uuid,
            "paciente_id": self.paciente_id,
            "medico_id": self.medico_id,
            "fecha_emision": self.fecha_emision.isoformat() if self.fecha_emision else None,
            "fecha_vencimiento": self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            "odEsfera": self.odEsfera,
            "odAdicion": self.odAdicion,
            "odCilindro": self.odCilindro,
            "odEje": self.odEje,
            "oiEsfera": self.oiEsfera,
            "oiAdicion": self.oiAdicion,
            "oiCilindro": self.oiCilindro,
            "oiEje": self.oiEje,
            "distancia_pupilar": self.distancia_pupilar,
            "Tipolente": self.Tipolente
        }
    

if __name__ == "__main__":
    # Ejemplo de uso
    try:
        # Crear una instancia de RecetaMedicaSchema con datos de ejemplo
        receta = RecetaMedicaSchema(
            uuid="123e4567-e89b-12d3-a456-426614174000",
            paciente_id="paciente_001",
            medico_id="medico_001",
            fecha_emision=datetime(2024, 1, 1),
            fecha_vencimiento=datetime(2024, 12, 31),
            odEsfera=-2.5,
            odAdicion=1.0,
            odCilindro=-0.5,
            odEje=180,
            oiEsfera=-2.0,
            oiAdicion=0.5,
            oiCilindro=-0.25,
            oiEje=170,
            distancia_pupilar=62.0,
            Tipolente="Lentes de contacto"
        )
        print(receta)
        print(receta.to_dict())

        # Crear una instancia de ProductoSchema con datos de ejemplo
        producto = ProductoSchema(
            sku="PROD001",
            tipo_producto="Lentes de contacto",
            precio=100,
            stock_disponible=50
        )
        print(producto)
        print(producto.to_dict())

    except ValidationError as e:
        print("Errores de validación:", e.errors())