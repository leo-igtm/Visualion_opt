from fastapi import FastAPI
from Backend.controllers.empleado import router as empleado_router
from Backend.controllers.paciente import router as paciente_router
from Backend.controllers.clinica import router as clinica_router
from Backend.controllers.optica import router as optica_router


app = FastAPI(  
    title="Visualion API backend ",
)

app.include_router(empleado_router)
app.include_router(clinica_router)
app.include_router(optica_router)
app.include_router(paciente_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Visualion API!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)