from fastapi import FastAPI
import uvicorn
from api.controllers.paciente_controller import router 
from api.models.paciente import APIRouter


app = FastAPI(
    title="Visualion API",
    docs="/api/docs",
    openapi_url="/api/openapi.json",

) 

app.include_router(router, prefix="/api/pacientes", tags=["Pacientes"])

@app.get("/api/controller")
async def get_controller():
    return {"message": "This is the PacienteController endpoint"}

@app.get("/api/health")
async def health_check():
    return {"status": "Front end and backend successfully connected"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="127.0.0.1", port=5328,reload=True)
