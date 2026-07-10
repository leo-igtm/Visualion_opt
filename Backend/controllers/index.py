from fastapi import FastAPI
from ..controllers import users

# Puedes agregar más routers a medida que crezcan los módulos
# from Backend.routers import pacientes, optica, etc.

app = FastAPI(
    title="Visualion API",
    description="API para la gestión integral de clínicas oftalmológicas y ópticas.",
    version="1.0.0"
)

# Incluir los routers en la aplicación principal
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Visualion API"}