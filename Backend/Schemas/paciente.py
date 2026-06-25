from typing import Optional
from Backend.Schemas.persona_base import PersonaBase
from pydantic import BaseModel

''' Esquemas para representar los datos de un paciente, incluyendo su obra social e historial médico. Estos esquemas se utilizan para validar la información al crear o actualizar un paciente, así como para serializar la información del paciente al responder a las solicitudes de la API.'''
class PacienteCreate(PersonaBase):
    obra_social: Optional[str] = None
    historial_medico: Optional[str] = None

''' Esquema para representar la respuesta de un paciente, incluyendo su ID, obra social e historial médico. Este esquema se utiliza para serializar la información del paciente al responder a las solicitudes de la API.'''
class PacienteOut(PersonaBase):
    id: int
    obra_social: Optional[str] = None
    historial_medico: Optional[str] = None

''' Esquema para actualizar la información de un paciente, reutilizando la estructura base y permitiendo la actualización de campos específicos como obra social e historial médico. Este esquema se utiliza para validar la información al realizar una solicitud de actualización de un paciente.'''
class PacienteUpdate(BaseModel):
    # Hacemos todos los campos opcionales para permitir actualizaciones parciales (PATCH)
    dni: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    obra_social: Optional[str] = None
    historial_medico: Optional[str] = None
