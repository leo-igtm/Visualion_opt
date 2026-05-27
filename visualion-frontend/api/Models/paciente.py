from api.datebase.dbconnections_opt import DatabaseConnection, Base
from api.controllers.paciente_controller import router as paciente_router
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError

class PacienteController:
    def __init__(self):
        self.router = APIRouter()
        self.router.include_router(paciente_router, prefix="/pacientes", tags=["Pacientes"])
    def get_router(self):
        return self.router
    