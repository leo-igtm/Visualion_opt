from typing import Optional
from pydantic import BaseModel
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

class EmpleadoUpdate(BaseModel):
    dni: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    legajo: Optional[str] = None
    usuario: Optional[str] = None
    contraseña: Optional[str] = None
    rol: Optional[str] = None
    
    # Campos opcionales dependiendo del rol
    matricula: Optional[str] = None
    especialidad: Optional[str] = None
    matricula_optico: Optional[str] = None
    comisiones: Optional[float] = None