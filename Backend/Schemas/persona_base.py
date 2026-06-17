from typing import Optional
from pydantic import BaseModel, EmailStr


class PersonaBase(BaseModel):
    dni: str
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True
