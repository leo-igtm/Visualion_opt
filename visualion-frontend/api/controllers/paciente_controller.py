import os
from api.datebase.dbconnections_opt import DatabaseConnection, Base
from api.controllers.paciente_controller import router as paciente_router
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError