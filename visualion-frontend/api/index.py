from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from api.database.dbconnections_opt import DatabaseConnection
from api.controllers import paciente_controller
from api.Models.models import Producto, RecetaMedica
from api.Models.schemas import ProductoSchema, RecetaMedicaSchema

import uvicorn

models.Base.metadata.create_all(bind=DatabaseConnection.engine)


app = FastAPI(title="Visualion API", description="API para la gestión de productos y recetas médicas", version="1.0.0")

@app.get ("/productos/{sku}", response_model=ProductoSchema)
async def get_producto(sku: str, db: DatabaseConnection = DatabaseConnection.get_instance()):
    # Lógica para obtener un producto por su SKU
    db = DatabaseConnection.get_instance()
    producto = db.query(Producto).filter(Producto.sku == sku).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    pass

@app.get("/api/health")
async def health_check():
    return {"status": "Front end and backend successfully connected"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="127.0.0.1", port=5328,reload=True)
