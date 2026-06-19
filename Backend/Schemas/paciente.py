from typing import Optional
from Backend.Schemas.persona_base import PersonaBase


class PacienteCreate(PersonaBase):
    obra_social: Optional[str] = None
    historial_medico: Optional[str] = None

class PacienteOut(PersonaBase):
    id: int

class PacienteUpdate(PersonaBase):
    obra_social: Optional[str] = None
    historial_medico: Optional[str] = None
