from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from Backend.Models.taller import EstadoOrden

'''Esquemas para validación y serialización de datos relacionados con órdenes de trabajo, etapas de trabajo e histórico de estados en el módulo de taller.'''


class OrdenTrabajoBase(BaseModel):
    venta_id: int
    descripcion_trabajo: Optional[str] = None
    fecha_entrega_esperada: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrdenTrabajoCreate(OrdenTrabajoBase):
    pass


class OrdenTrabajoUpdate(BaseModel):
    descripcion_trabajo: Optional[str] = None
    fecha_entrega_esperada: Optional[datetime] = None

    class Config:
        from_attributes = True


# CORRECCIÓN BUG #6: orden_id removido del body — llega por path parameter
class EtapaTrabajoCreate(BaseModel):
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


class EtapaTrabajoResponse(BaseModel):
    id: int
    orden_id: int
    etapa: str
    tecnico_id: Optional[int] = None
    completado: bool = False
    notas: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


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


class HistoricoEstadosResponse(HistoricoEstadosBase):
    id: int
    fecha_creacion: datetime


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


class OrdenTrabajoResponse(OrdenTrabajoBase):
    id: int
    estado: str
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    etapas: Optional[list[EtapaTrabajoResponse]] = None
    historico_estados: Optional[list[HistoricoEstadosResponse]] = None
