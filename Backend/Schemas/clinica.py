from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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

    class Config:
        from_attributes = True

##Receta Medica

class RecetaMedicaBase(BaseModel):
    uuid: int
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

    distancia_pupilar: float = None
    tipo_lente: str = None


class RecetaMedicaCreate(RecetaMedicaBase):
    pass

class RecetaMedicaResponse(RecetaMedicaCreate):
    uuid: int
    fecha_emision: datetime
    class Config:
        from_attributes = True
