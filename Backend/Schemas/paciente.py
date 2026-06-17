from typing import Optional
from Backend.Schemas.persona_base import PersonaBase


class PacienteCreate(PersonaBase):
    obra_social: Optional[str] = None
    historial_medico: Optional[str] = None

class PacienteOut(PersonaBase):
    id: int
    class Config:
        from_attributes = True

class PacienteUpdate(PersonaBase):
    dni: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    obra_social: Optional[str] = None
    historial_medico: Optional[str] = None
