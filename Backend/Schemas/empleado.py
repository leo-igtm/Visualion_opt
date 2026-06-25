from typing import Optional
from pydantic import BaseModel
from Backend.Schemas.persona_base import PersonaBase

# --- Schemas para Autenticación ---

class EmpleadoCreate(PersonaBase):
    """Schema para crear cualquier tipo de empleado (usado por administradores)."""
    legajo: str
    usuario: str
    password: str
    rol: str

    # Campos opcionales dependiendo del rol
    matricula: Optional[str] = None
    especialidad: Optional[str] = None
    matricula_optico: Optional[str] = None
    comisiones: Optional[float] = None

class PacienteRegister(PersonaBase):
    """Schema simple para el registro público de pacientes."""
    password: str

class UsuarioLogin(BaseModel):
    usuario: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    usuario: Optional[str] = None

# --- Schemas para Respuestas y Actualizaciones ---

class EmpleadoResponse(PersonaBase):
    """Schema para las respuestas de la API, no incluye la contraseña."""
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
    password: Optional[str] = None
    rol: Optional[str] = None

    # Campos opcionales dependiendo del rol
    matricula: Optional[str] = None
    especialidad: Optional[str] = None
    matricula_optico: Optional[str] = None
    comisiones: Optional[float] = None