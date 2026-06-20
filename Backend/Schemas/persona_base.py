from typing import Optional
from pydantic import BaseModel, EmailStr

'''Esquema base para representar los datos comunes de una persona, incluyendo campos como DNI, nombre, apellido, teléfono y correo electrónico. Este esquema se utiliza como base para otros esquemas específicos de pacientes, empleados u otros tipos de personas en el sistema.'''
'''se usa para crear usuarios de empleados y pacientes, y para responder con su información, asegurando que los datos sean consistentes y validados correctamente.'''
class PersonaBase(BaseModel):
    dni: str
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True
