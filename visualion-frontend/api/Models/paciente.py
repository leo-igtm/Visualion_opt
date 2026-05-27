from api.database.dbconnections_opt import DatabaseConnection
from api.controllers.paciente_controller import router as paciente_router
from fastapi import APIRouter, HTTPException


# modelo de manejo de datos de paciente,medico,administrador
class Paciente:
    def __init__(self, id: int, name: str, age: int):
        self.id = id
        self.name = name
        self.age = age

class medico:
    def __init__(self, id: int, name: str, specialty: str):
        self.id = id
        self.name = name
        self.specialty = specialty



if __name__ == "__main__":
    # Test the database connection
    try:
        db = DatabaseConnection.get_instance()
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")   
    
    
    