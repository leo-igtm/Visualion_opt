#inicio de sesion - registro - olvide contraseña crear usuario  para el sistema de gestión de la oftalmología Visualion 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.database.dbconnections_opt import get_db

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login")
async def login(username: str, password: str, db: AsyncSession = Depends(get_db)):
    username = username.strip()
    password = password.strip()

    if not username or not password:
        raise HTTPException(status_code=400, detail="El nombre de usuario y la contraseña no pueden estar vacíos.")



    # Aquí iría la lógica para verificar el usuario y contraseña
    # Por ejemplo, podrías consultar la base de datos para validar las credenciales
    if username == "admin" and password == "password":  # Esto es solo un ejemplo, no uses esto en producción
        return {"message": "Login exitoso"}
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    