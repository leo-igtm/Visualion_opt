from fastapi import FastAPI
from Backend.controllers.empleado import router as empleado_router
from Backend.controllers.paciente import router as paciente_router
from Backend.controllers.clinica import router as clinica_router
from Backend.controllers.optica import router as optica_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(  
    title="Visualion API backend ",
)

app.include_router(empleado_router)
app.include_router(clinica_router)
app.include_router(optica_router)
app.include_router(paciente_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Visualion API!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)