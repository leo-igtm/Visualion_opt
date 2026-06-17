from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession    
from sqlalchemy import select
from Backend.Schemas.empleado import EmpleadoOut , EmpleadoCreate, EmpleadoUpdate
from Backend.Models.Usuarios import Empleado, Medico, Tecnico, Vendedor , Persona 
from Backend.database.dbconnections_opt import get_db

router = APIRouter(
    prefix="/empleados",
    tags=["Gestion de empleados"]
)

#Crear empleado
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

    match rol:
        case "medico":
            nuevo_empleado = Medico(
                dni=empleado_in.dni,
                nombre=empleado_in.nombre,
                apellido=empleado_in.apellido,
                telefono=empleado_in.telefono,
                email=empleado_in.email,
                legajo=empleado_in.legajo,
                usuario=empleado_in.usuario,
                contraseña=empleado_in.contraseña,
                rol=rol,
                especialidad=empleado_in.especialidad,
                matricula=empleado_in.matricula
            )
        case "tecnico":
            nuevo_empleado = Tecnico(
                dni=empleado_in.dni,
                nombre=empleado_in.nombre,
                apellido=empleado_in.apellido,
                telefono=empleado_in.telefono,
                email=empleado_in.email,
                legajo=empleado_in.legajo,
                usuario=empleado_in.usuario,
                contraseña=empleado_in.contraseña,
                rol=rol,
                matricula_optico=empleado_in.matricula_optico
            )
        case "vendedor":
            nuevo_empleado = Vendedor(
                dni=empleado_in.dni,
                nombre=empleado_in.nombre,
                apellido=empleado_in.apellido,
                telefono=empleado_in.telefono,
                email=empleado_in.email,
                legajo=empleado_in.legajo,
                usuario=empleado_in.usuario,
                contraseña=empleado_in.contraseña,
                rol=rol,
                comisiones=empleado_in.comisiones or 0.0
            )
        case _:
            raise HTTPException(status_code=400, detail="Rol no válido.")

    db.add(nuevo_empleado)
    await db.commit()
    await db.refresh(nuevo_empleado)
    return nuevo_empleado


@router.get("/rol/{empleado_rol}", response_model=list[EmpleadoOut])
async def obtener_empleados_por_rol(empleado_rol: str, db: AsyncSession = Depends(get_db)):
    query = select(Empleado).where(Empleado.rol == empleado_rol)
    resultado = await db.execute(query)
    empleados = resultado.scalars().all()
    return empleados

@router.get("/{empleado_id}", response_model=EmpleadoOut)
async def obtener_empleado_por_id(empleado_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Empleado).where(Empleado.id == empleado_id)
    resultado = await db.execute(query)
    empleado = resultado.scalars().first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")
    return empleado

@router.put("/{empleado_id}", response_model=EmpleadoOut)
async def actualizar_empleado(empleado_id: int, empleado_in: EmpleadoUpdate, db: AsyncSession = Depends(get_db)):
    query = select(Empleado).where(Empleado.id == empleado_id)
    resultado = await db.execute(query)
    empleado = resultado.scalars().first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")
    
    for key, value in empleado_in.model_dump(exclude_unset=True).items():
        setattr(empleado, key, value)

    await db.commit()
    await db.refresh(empleado)
    return empleado

@router.delete("/{empleado_id}")
async def eliminar_empleado(empleado_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Empleado).where(Empleado.id == empleado_id)
    resultado = await db.execute(query)
    empleado = resultado.scalars().first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")
    
    await db.delete(empleado)
    await db.commit()
    return {"detail": "Empleado eliminado exitosamente."}

@router.get("/", response_model=list[EmpleadoOut])
async def listar_empleados(db: AsyncSession = Depends(get_db)):
    query = select(Empleado)
    resultado = await db.execute(query)
    empleados = resultado.scalars().all()
    return empleados


    