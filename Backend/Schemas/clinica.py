from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, Any
from ..validators.optica_validators import PrescriptionValidator


class TurnoBase(BaseModel):
    paciente_id: int
    medico_id: int 
    fecha_hora: datetime
    motivo: Optional[str] = None
    estado: Optional[str] = "pendiente"   # Valor por defecto

    class Config:
        from_attributes = True


class TurnoCreate(TurnoBase):
    pass


class TurnoResponse(TurnoBase):
    id: int

##Receta Medica

class RecetaMedicaBase(BaseModel):
    turno_id: Optional[int] = None
    paciente_id: int
    medico_id: Optional[int] = None
    fecha_vencimiento: datetime

    od_esfera: float = 0.0
    od_cilindro: float = 0.0
    od_eje: int = 0
    od_adicion: float = 0.0

    oi_esfera: float = 0.0
    oi_cilindro: float = 0.0
    oi_eje: int = 0
    oi_adicion: float = 0.0

    distancia_pupilar: Optional[float] = None
    tipo_lente: Optional[str] = None

    @field_validator('od_eje')
    @classmethod
    def validate_od_eje(cls, v: Any):
        return PrescriptionValidator.validate_axis(v, "OD Eje")

    @field_validator('od_esfera')
    @classmethod
    def validate_od_esfera(cls, v: Any):
        return PrescriptionValidator.validate_sphere(v, "OD Esfera")

    @field_validator('od_cilindro')
    @classmethod
    def validate_od_cilindro(cls, v: Any):
        return PrescriptionValidator.validate_cylinder(v, "OD Cilindro")

    @field_validator('od_adicion')
    @classmethod
    def validate_od_adicion(cls, v: Any):
        return PrescriptionValidator.validate_addition(v, "OD Adición")

    @field_validator('oi_eje')
    @classmethod
    def validate_oi_eje(cls, v: Any):
        return PrescriptionValidator.validate_axis(v, "OI Eje")

    @field_validator('oi_esfera')
    @classmethod
    def validate_oi_esfera(cls, v: Any):
        return PrescriptionValidator.validate_sphere(v, "OI Esfera")

    @field_validator('oi_cilindro')
    @classmethod
    def validate_oi_cilindro(cls, v: Any):
        return PrescriptionValidator.validate_cylinder(v, "OI Cilindro")

    @field_validator('oi_adicion')
    @classmethod
    def validate_oi_adicion(cls, v: Any):
        return PrescriptionValidator.validate_addition(v, "OI Adición")

    @field_validator('distancia_pupilar')
    @classmethod
    def validate_distancia(cls, v: Any):
        return PrescriptionValidator.validate_pupilary_distance(v)


class RecetaMedicaCreate(RecetaMedicaBase):
    pass

class RecetaMedicaResponse(RecetaMedicaCreate):
    uuid: int
    fecha_emision: datetime
    class Config:
        from_attributes = True
