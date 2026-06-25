from fastapi import FastAPI
from Backend.controllers.auth import router as auth_router
from Backend.controllers.users import router as users_router
from Backend.controllers.paciente import router as paciente_router
from Backend.controllers.clinica import router as clinica_router
from Backend.controllers.optica import router as optica_router
from Backend.controllers.taller import router as taller_router
from fastapi.middleware.cors import CORSMiddleware
from Backend.logger.logger import logger_manager

logger = logger_manager.get_logger()

'''Inicialización de la aplicación FastAPI'''
'''Se crean los routers para cada módulo y se agregan a la aplicación.'''
app = FastAPI(
    title="Visualion API backend ",
)

@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando aplicación Visualion API")


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(clinica_router)
app.include_router(optica_router)
app.include_router(taller_router)
app.include_router(paciente_router)

'''Configuración de CORS para permitir solicitudes desde el frontend
se especifican los orígenes permitidos, los métodos y los encabezados.'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

'''Ruta raíz de la API que devuelve un mensaje de bienvenida.'''
@app.get("/")
async def root():
    return {"message": "Welcome to the Visualion API!"}

'''Se ejecuta la aplicación FastAPI usando Uvicorn si el archivo se ejecuta directamente.
Se especifica el host y el puerto para la aplicación, y se puede acceder a la API en http://127.0.0.1:8000'''
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)