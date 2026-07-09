from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.database.dbconnections_opt import get_db
from Backend.Schemas.paciente import PacienteCreate, PacienteOut, PacienteUpdate
from Backend.Models.Usuarios import Paciente, Persona

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

#
@router.post("/", response_model=PacienteOut)
async def crear_paciente(paciente_in: PacienteCreate, db: AsyncSession = Depends(get_db)):
    query_dni = select(Persona).where(Persona.dni == paciente_in.dni)
    resultado_dni = await db.execute(query_dni)
    # ACÁ ESTÁ LA MAGIA: .scalars().first() extrae el dato real o devuelve None
    if resultado_dni.scalars().first():
        raise HTTPException(status_code=400, detail="El DNI ya está registrado.")


    nuevo_paciente = Paciente(
        dni=paciente_in.dni,
        nombre=paciente_in.nombre,
        apellido=paciente_in.apellido,
        telefono=paciente_in.telefono,
        email=paciente_in.email,
        obra_social=paciente_in.obra_social,
        historial_medico=paciente_in.historial_medico
    )

    db.add(nuevo_paciente)
    try:
        await db.commit()
        await db.refresh(nuevo_paciente)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    return nuevo_paciente


@router.get("/{paciente_obra_social}", response_model=PacienteOut)
async def obtener_paciente(paciente_obra_social: str, db: AsyncSession = Depends(get_db)):
    query = select(Paciente).where(Paciente.obra_social == paciente_obra_social)
    resultado = await db.execute(query)
    paciente = resultado.scalars().first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado.")
    return paciente

@router.get("/dni/{paciente_dni}", response_model=PacienteOut)
async def obtener_paciente_por_dni(paciente_dni: str, db: AsyncSession = Depends(get_db)):
    query = select(Paciente).where(Paciente.dni == paciente_dni)
    resultado = await db.execute(query)
    paciente = resultado.scalars().first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado.")
    return paciente


@router.put("/{paciente_id}", response_model=PacienteOut)
async def actualizar_paciente(paciente_id: int, paciente_in: PacienteUpdate, db: AsyncSession = Depends(get_db)):
    query = select(Paciente).where(Paciente.id == paciente_id)
    resultado = await db.execute(query)
    paciente = resultado.scalars().first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado.")

    # Actualizar campos solo si se enviaron
    if paciente_in.telefono is not None:
        paciente.telefono = paciente_in.telefono
    if paciente_in.email is not None:
        paciente.email = paciente_in.email
    if paciente_in.obra_social is not None:
        paciente.obra_social = paciente_in.obra_social
    if paciente_in.historial_medico is not None:
        paciente.historial_medico = paciente_in.historial_medico

    db.add(paciente)
    try:
        await db.commit()
        await db.refresh(paciente)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    return paciente


@router.delete("/{paciente_dni}")
async def eliminar_paciente(paciente_dni: str, db: AsyncSession = Depends(get_db)):
    query = select(Paciente).where(Paciente.dni == paciente_dni)
    resultado = await db.execute(query)
    paciente = resultado.scalars().first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado.")

    try:
        await db.delete(paciente)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    return {"detail": "Paciente eliminado exitosamente."}

@router.get("/", response_model=list[PacienteOut]) 
async def listar_pacientes(db: AsyncSession = Depends(get_db)):
    query = select(Paciente)
    resultado = await db.execute(query)
    pacientes = resultado.scalars().all()
    return pacientes