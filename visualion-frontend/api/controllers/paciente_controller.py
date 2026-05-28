import os
from fastapi import APIRouter, HTTPException
from api.database.dbconnections_opt import DatabaseConnection
from api.Models.models import Paciente


#implementar strategy pattern para manejar diferentes tipos de pacientes (por ejemplo, pacientes nuevos, pacientes recurrentes, etc.) y sus respectivas lógicas de negocio.


router = APIRouter(
    prefix="/api/pacientes",
    tags=["pacientes"],
    responses={404: {"description": "Not found"}},
)

@router.post("/create")
async def create_paciente(paciente: Paciente):
    try:
        db = DatabaseConnection()
        db.add(paciente)
        db.commit()
        return {"message": "Paciente creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{paciente_id}")
async def get_paciente(paciente_id: int):
    try:
        db = DatabaseConnection()
        paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if paciente is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        return paciente.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{paciente_id}")
async def update_paciente(paciente_id: int, paciente_data: Paciente):
    try:
        db = DatabaseConnection()
        paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if paciente is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        for key, value in paciente_data.to_dict().items():
            setattr(paciente, key, value)
        db.commit()
        return {"message": "Paciente actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    