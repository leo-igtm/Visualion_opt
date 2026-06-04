from typing import Optional
from Backend.Schemas.persona_base import PersonaBase


class PacienteCreate(PersonaBase):
    obra_social: Optional[str] = None
    historial_medico: Optional[str] = None

class PacienteOut(PacienteCreate):
    id: int

    class Config:
        from_attributes = True