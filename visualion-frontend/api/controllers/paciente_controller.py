import os
from fastapi import APIRouter, HTTPException
from api.database.dbconnections_opt import DatabaseConnection
from api.models.paciente import paciente_controller

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)



@router.get("/")
def listar_pacientes():
    # Aquí puedes implementar la lógica para obtener la lista de pacientes desde la base de datos
    # Por ejemplo, usando SQLAlchemy para consultar la tabla de pacientes
    # return db.query(Paciente).all()
    pacientes = paciente_controller.listar_pacientes()

    return {"message": "List of patients", "pacientes": pacientes}


@router.post("/")
async def create_paciente(paciente: dict):
    # Aquí puedes implementar la lógica para crear un nuevo paciente en la base de datos
    # Por ejemplo, usando SQLAlchemy para insertar un nuevo registro en la tabla de pacientes
    # new_paciente = Paciente(**paciente)
    # db.add(new_paciente)
    # db.commit()
    paciente_controller.crear_paciente(paciente)
    new_paciente = paciente_controller.crear_paciente(paciente)

    return {"message": "Paciente created successfully"}