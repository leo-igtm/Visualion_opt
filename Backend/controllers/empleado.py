from pydantic import BaseModel
from typing import Optional
from ..Schemas.persona_base import PersonaBase

# Schema para los datos del token JWT
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Schema base para Empleado
class EmpleadoBase(PersonaBase):
    pass

# Schema para el registro público (pacientes)
class EmpleadoCreate(EmpleadoBase):
    password: str

# Schema para la creación interna de empleados (admins)
class EmpleadoCreateInternal(EmpleadoCreate):
    rol: str

# Schema para la respuesta de la API (sin contraseña)
class EmpleadoResponse(EmpleadoBase):
    id: int
    rol: str
    is_active: bool

    