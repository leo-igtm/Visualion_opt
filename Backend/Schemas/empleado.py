from typing import Optional
from pydantic import BaseModel, field_validator
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


class EmpleadoRegister(EmpleadoCreate):
    @field_validator('contraseña')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Contraseña debe tener mín 8 caracteres")
        if not any(c.isupper() for c in v):
            raise ValueError("Contraseña debe incluir mayúsculas")
        if not any(c.isdigit() for c in v):
            raise ValueError("Contraseña debe incluir dígitos")
        return v


class UsuarioLogin(BaseModel):
    usuario: str
    contraseña: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


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