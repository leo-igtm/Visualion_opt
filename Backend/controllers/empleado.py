from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession    
from sqlalchemy import select


from Backend.Schemas.empleado import EmpleadoBase, EmpleadoCreate
from Backend.Models.empleados import Empleado , Medico , Tecnico , Vendedor
from Backend.database.dbconnections_opt import get_db

router = APIRouter(
    prefix="/empleados",
    tags=["Gestion de empleados"]
)

@router.post("/",response_model=EmpleadoBase)
async def create_empleado(empleado: EmpleadoCreate, db: AsyncSession = Depends(get_db)):
   
    match empleado.rol:
        case "medico":
            nuevo_empleado = Medico(
                nombre=empleado.nombre,
                apellido=empleado.apellido,
                dni=empleado.dni,
                usuario=empleado.usuario,
                contrasena=empleado.contrasena,
                matricula=empleado.matricula,
                especialidad=empleado.especialidad
            )
        case "tecnico":
            nuevo_empleado = Tecnico(
                nombre=empleado.nombre,
                apellido=empleado.apellido,
                dni=empleado.dni,
                usuario=empleado.usuario,
                contrasena=empleado.contrasena,
                matricula=empleado.matricula,
            )
        case "vendedor":
            nuevo_empleado = Vendedor(
                nombre=empleado.nombre,
                apellido=empleado.apellido,
                dni=empleado.dni,
                usuario=empleado.usuario,
                contrasena=empleado.contrasena,
                Legajo=empleado.Legajo,
                Comisiones=empleado.Comisiones
            )
        case _:
            raise HTTPException(status_code=400, detail="Rol no válido")
    db.add(nuevo_empleado)
    await db.commit()
    await db.refresh(nuevo_empleado)
    return nuevo_empleado

@router.get("/{empleado_id}")
async def get_empleado(empleado_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Empleado).where(Empleado.id == empleado_id))
    empleado = result.scalars().first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado