from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.database.dbconnections_opt import get_db
from Backend.Schemas.paciente import PacienteCreate, PacienteOut
from Backend.Models.Usuarios import Paciente, Persona

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

@router.post("/", response_model=PacienteOut)
def crear_paciente(paciente_in: PacienteCreate, db: Session = Depends(get_db)):
    if db.query(Persona).filter(Persona.dni == paciente_in.dni).first():
        raise HTTPException(status_code=400, detail="El DNI ya está registrado.")

    nuevo_paciente = Paciente(
        dni=paciente_in.dni,
        nombre=paciente_in.nombre,
        apellido=paciente_in.apellido,
        telefono=paciente_in.telefono,
        email=paciente_in.email,
        obra_social=paciente_in.obra_social,
        historial_medico=paciente_in.historial_medico
    )

    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)
    return nuevo_paciente