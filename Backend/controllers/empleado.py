from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession    
from sqlalchemy import select
from typing import Union
from Backend.Schemas.empleado import EmpleadoOut , EmpleadoCreate
from sqlalchemy.orm import Session
from Backend.Models.Usuarios import Empleado, Medico, Tecnico, Vendedor , Persona 
from Backend.database.dbconnections_opt import get_db

router = APIRouter(
    prefix="/empleados",
    tags=["Gestion de empleados"]
)

@router.post("/", response_model=EmpleadoOut)
async def crear_empleado(empleado_in: EmpleadoCreate, db: AsyncSession = Depends(get_db)):
    query_dni = select(Persona).where(Persona.dni == empleado_in.dni)
    resultado_dni = await db.execute(query_dni)
    # ACÁ ESTÁ LA MAGIA: .scalars().first() extrae el dato real o devuelve None
    if resultado_dni.scalars().first():
        raise HTTPException(status_code=400, detail="El DNI ya está registrado.")
    
    # 2. Validar Usuario y Legajo
    query_emp = select(Empleado).where(
        (Empleado.usuario == empleado_in.usuario) | (Empleado.legajo == empleado_in.legajo)
    )
    resultado_emp = await db.execute(query_emp)
    if resultado_emp.scalars().first():
        raise HTTPException(status_code=400, detail="Usuario o legajo en uso.")
    rol = empleado_in.rol.lower()
    base_data = {
        "dni": empleado_in.dni, "nombre": empleado_in.nombre, "apellido": empleado_in.apellido,
        "telefono": empleado_in.telefono, "email": empleado_in.email, "legajo": empleado_in.legajo,
        "usuario": empleado_in.usuario, "contraseña": empleado_in.contraseña, "rol": rol
    }

    match rol:
        case "medico":
            nuevo_empleado = Medico(**base_data, especialidad=empleado_in.especialidad, matricula=empleado_in.matricula)
        case "tecnico":
            nuevo_empleado = Tecnico(**base_data, matricula_optico=empleado_in.matricula_optico)
        case "vendedor":
            nuevo_empleado = Vendedor(**base_data, comisiones=empleado_in.comisiones or 0.0)
        case _:
            raise HTTPException(status_code=400, detail="Rol no válido.")

    db.add(nuevo_empleado)
    await db.commit()
    await db.refresh(nuevo_empleado)
    return nuevo_empleado