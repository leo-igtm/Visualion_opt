from typing import Literal, Optional, Union
from pydantic import BaseModel
from .persona_base import PersonaBase

# --- Schemas para Creación de Usuarios (Refactorizado) ---

class PacienteCreate(PersonaBase):
    """Schema para crear un Paciente. Usado por administradores."""
    rol: Literal["paciente"] = "paciente"
    obra_social: Optional[str] = None

class EmpleadoCreateBase(PersonaBase):
    """Schema base para crear cualquier tipo de Empleado. No usar directamente."""
    legajo: str  # El legajo es OBLIGATORIO para todos los empleados.
    usuario: str
    password: str

class MedicoCreate(EmpleadoCreateBase):
    """Schema para crear un Medico."""
    rol: Literal["medico"] = "medico"
    matricula: str
    especialidad: str

class TecnicoCreate(EmpleadoCreateBase):
    """Schema para crear un Tecnico."""
    rol: Literal["tecnico"] = "tecnico"
    matricula_optico: str

class VendedorCreate(EmpleadoCreateBase):
    """Schema para crear un Vendedor."""
    rol: Literal["vendedor"] = "vendedor"
    comisiones: float = 0.0

class AdminCreate(EmpleadoCreateBase):
    """Schema para crear un Administrador."""
    rol: Literal["admin"] = "admin"

# Union Discriminada para el endpoint /users/create.
# FastAPI usará el campo 'rol' para determinar qué schema validar.
# Esto generará un menú desplegable en la documentación de Swagger.
UserCreate = Union[PacienteCreate, MedicoCreate, TecnicoCreate, VendedorCreate, AdminCreate]

# --- Schemas para Autenticación ---

class PacienteRegister(PersonaBase):
    """Schema simple para el registro público de pacientes."""

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
    legajo: Optional[str] = None # Un Paciente no tiene legajo
    usuario: str
    rol: str

class PacienteResponse(PersonaBase):
    """Schema para las respuestas de la API al crear un paciente."""
    id: int
    obra_social: Optional[str] = None


class EmpleadoUpdate(BaseModel):
    dni: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    legajo: Optional[str] = None
    usuario: Optional[str] = None # El cambio de usuario debería ser un proceso separado y más controlado
    password: Optional[str] = None
    rol: Optional[str] = None

    # Campos opcionales dependiendo del rol
    matricula: Optional[str] = None
    especialidad: Optional[str] = None
    matricula_optico: Optional[str] = None
    comisiones: Optional[float] = None