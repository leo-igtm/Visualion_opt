from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from Backend.Models.taller import EstadoOrden

'''''Esquemas para validación y serialización de datos relacionados con órdenes de trabajo, etapas de trabajo e histórico de estados en el módulo de taller.'''
class OrdenTrabajoBase(BaseModel):
    venta_id: int
    descripcion_trabajo: Optional[str] = None
    fecha_entrega_esperada: Optional[datetime] = None

    class Config:
        from_attributes = True

'''Los siguientes esquemas se utilizan para crear, actualizar y responder con datos de órdenes de trabajo, etapas de trabajo e histórico de estados. Incluyen validaciones específicas para campos como etapa y estado, asegurando que solo se acepten valores válidos.'''
class OrdenTrabajoCreate(OrdenTrabajoBase):
    pass

'''Esquema para actualizar una orden de trabajo, permitiendo modificar la descripción del trabajo y la fecha de entrega esperada.'''
class OrdenTrabajoUpdate(BaseModel):
    descripcion_trabajo: Optional[str] = None
    fecha_entrega_esperada: Optional[datetime] = None

    class Config:
        from_attributes = True

'''Esquema para representar la respuesta de una orden de trabajo, incluyendo su estado actual, fechas de creación y actualización, así como las etapas de trabajo e histórico de estados asociados.
Incluye validación para asegurar que el estado de la orden sea uno de los estados válidos definidos en la clase EstadoOrden.'''
class EtapaTrabajoBase(BaseModel):
    orden_id: int
    etapa: str
    tecnico_id: Optional[int] = None
    completado: bool = False
    notas: Optional[str] = None

    @field_validator('etapa')
    @classmethod
    def validate_etapa(cls, v: str):
        valid_etapas = ["biselado", "montaje", "control_calidad"]
        if v not in valid_etapas:
            raise ValueError(f"Etapa inválida. Debe ser una de: {', '.join(valid_etapas)}")
        return v

    class Config:
        from_attributes = True

'''Esquema para crear una nueva etapa de trabajo, reutilizando la estructura base y permitiendo la validación de la etapa.'''

class EtapaTrabajoCreate(EtapaTrabajoBase):
    pass

'''Esquema para representar la respuesta de una etapa de trabajo, incluyendo su estado de completado y fechas de creación y actualización.
Este esquema se utiliza para serializar la información de las etapas de trabajo al responder a las solicitudes de la API.'''
class EtapaTrabajoResponse(EtapaTrabajoBase):
    id: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    

'''Esquema para representar la respuesta del histórico de estados, incluyendo el estado anterior, el nuevo estado, el técnico asociado y la fecha de creación. Este esquema se utiliza para serializar la información del histórico de estados al responder a las solicitudes de la API.
Incluye validación para asegurar que el nuevo estado sea uno de los estados válidos definidos en la clase EstadoOrden.'''
class HistoricoEstadosBase(BaseModel):
    orden_id: int
    estado_anterior: Optional[str] = None
    estado_nuevo: str
    tecnico_id: Optional[int] = None

    @field_validator('estado_nuevo')
    @classmethod
    def validate_estado(cls, v: str):
        if v not in EstadoOrden.all_estados():
            raise ValueError(f"Estado inválido: {v}")
        return v

    class Config:
        from_attributes = True

'''Esquema para crear una nueva entrada en el histórico de estados, reutilizando la estructura base y permitiendo la validación del nuevo estado.'''
class HistoricoEstadosResponse(HistoricoEstadosBase):
    id: int
    fecha_creacion: datetime

    

'''
Esquema para cambiar el estado de una orden de trabajo, incluyendo el nuevo estado, el técnico asociado y las notas opcionales. Este esquema se utiliza para validar la información al realizar una solicitud para cambiar el estado de una orden de trabajo.
Incluye validación para asegurar que el nuevo estado sea uno de los estados válidos definidos en la clase EstadoOrden.'''
class CambiarEstadoOrden(BaseModel):
    estado_nuevo: str
    tecnico_id: Optional[int] = None
    notas: Optional[str] = None

    @field_validator('estado_nuevo')
    @classmethod
    def validate_estado(cls, v: str):
        if v not in EstadoOrden.all_estados():
            raise ValueError(f"Estado inválido: {v}")
        return v

    class Config:
        from_attributes = True

'''Esquema para representar la respuesta de una orden de trabajo, incluyendo su estado actual, fechas de creación y actualización, así como las etapas de trabajo e histórico de estados asociados.'''
'''Indican que el esquema se puede construir a partir de objetos de la base de datos, lo que facilita la serialización de los datos al responder a las solicitudes de la API.'''
class OrdenTrabajoResponse(OrdenTrabajoBase):
    id: int
    estado: str
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    etapas: Optional[list[EtapaTrabajoResponse]] = None
    historico_estados: Optional[list[HistoricoEstadosResponse]] = None

    
