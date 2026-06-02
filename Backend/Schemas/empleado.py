import os 
from typing import Optional
from pydantic import BaseModel
from typing import Optional

class EmpleadoBase(BaseModel):
    id: int
    nombre: str
    apellido: str
    dni: str
    usuario: str
    rol: str

    class Config:
        from_attributes = True

class MedicoOut(EmpleadoBase):
    matricula: Optional[str]
    especialidad: Optional[str]

class TecnicoOut(EmpleadoBase):
    matricula_optico: Optional[str]

class EmpleadoCreate(BaseModel):
    nombre: str
    apellido: str
    dni: str
    usuario: str
    contraseña: str
    rol: str
    matricula: Optional[str] = None
    especialidad: Optional[str] = None
    matricula_optico: Optional[str] = None