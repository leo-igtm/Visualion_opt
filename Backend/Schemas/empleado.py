from typing import Optional
from Backend.Schemas.persona_base import PersonaBase

class EmpleadoCreate(PersonaBase):
    legajo: str
    usuario: str
    contraseña: str
    rol: str 
    
    # Campos opcionales dependiendo del rol
    matricula: Optional[str] = None
    especialidad: Optional[str] = None
    matricula_optico: Optional[str] = None
    comisiones: Optional[float] = None

class EmpleadoOut(PersonaBase):
    id: int
    legajo: str
    usuario: str
    rol: str