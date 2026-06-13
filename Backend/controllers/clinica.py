from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
# Ajusta estos imports a tu proyecto
from Backend.database.dbconnections_opt import get_db
from Backend.Models import clinica as models
from Backend.Models.Usuarios import Paciente, Medico
from Backend.Schemas import clinica as schemas

router = APIRouter(prefix="/clinica", tags=["Clínica - Turnos y Recetas"])
@router.post("/turnos/", response_model=schemas.TurnoResponse, status_code=status.HTTP_201_CREATED)
async def crear_turno(turno_in: schemas.TurnoCreate, db: AsyncSession = Depends(get_db)):
    
    # Validación 1: Verificar que el paciente exista
    query_paciente = select(Paciente).where(Paciente.id == turno_in.paciente_id)
    resultado_paciente = await db.execute(query_paciente)
    db_paciente = resultado_paciente.scalars().first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail=f"Paciente con ID {turno_in.paciente_id} no encontrado")

    # Validación 2: Verificar que el médico exista
    query_medico = select(Medico).where(Medico.id == turno_in.medico_id)
    resultado_medico = await db.execute(query_medico)
    db_medico = resultado_medico.scalars().first()
    if not db_medico:
        raise HTTPException(status_code=404, detail=f"Médico con ID {turno_in.medico_id} no encontrado")

    query_turno = select(models.Turno).where(
        models.Turno.medico_id == turno_in.medico_id,
        models.Turno.fecha_hora == turno_in.fecha_hora,
        models.Turno.estado != "cancelado"
    )
    resultado_turno = await db.execute(query_turno)
    turno_existente = resultado_turno.scalars().first()
    if turno_existente:
        raise HTTPException(status_code=400, detail=f"El médico ya tiene un turno programado para {turno_in.fecha_hora}")

    # Creación del turno
    nuevo_turno = models.Turno(
        fecha_hora=turno_in.fecha_hora,
        motivo=turno_in.motivo,
        estado=turno_in.estado,
        paciente_id=turno_in.paciente_id,
        medico_id=turno_in.medico_id
    )
    db.add(nuevo_turno)
    await db.commit()
    await db.refresh(nuevo_turno)
    return nuevo_turno

@router.post("/recetas/", response_model=schemas.RecetaMedicaResponse, status_code=status.HTTP_201_CREATED)
async def crear_receta(receta_in: schemas.RecetaMedicaCreate, db: AsyncSession = Depends(get_db)):
    # Validaciones: paciente, médico y turno existen, etc.
    # Validación 1: Verificar que el paciente exista
    query_paciente = select(Paciente).where(Paciente.id == receta_in.paciente_id)
    resultado_paciente = await db.execute(query_paciente)
    db_paciente = resultado_paciente.scalars().first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail=f"Paciente con ID {receta_in.paciente_id} no encontrado")

    # Validación 2: Verificar que el médico exista
    if receta_in.medico_id is not None:  # Solo validamos si se proporcionó un médico
        query_medico = select(Medico).where(Medico.id == receta_in.medico_id)
        resultado_medico = await db.execute(query_medico)
        db_medico = resultado_medico.scalars().first()
        if not db_medico:
            raise HTTPException(status_code=404, detail=f"Médico con ID {receta_in.medico_id} no encontrado")

        # Validación 3: Verificar que el turno exista
    if receta_in.turno_id is not None:  # Solo validamos si se proporcionó un turno
        query_turno = select(models.Turno).where(models.Turno.id == receta_in.turno_id)
        resultado_turno = await db.execute(query_turno)
        db_turno = resultado_turno.scalars().first()
        if not db_turno:
            raise HTTPException(status_code=404, detail=f"Turno con ID {receta_in.turno_id} no encontrado")

    
    nueva_receta = models.RecetaMedica(
        turno_id=receta_in.turno_id,
        paciente_id=receta_in.paciente_id,
        medico_id=receta_in.medico_id,
        fecha_vencimiento=receta_in.fecha_vencimiento,
        od_esfera=receta_in.od_esfera,
        od_cilindro=receta_in.od_cilindro,
        od_eje=receta_in.od_eje,
        od_adicion=receta_in.od_adicion,
        oi_esfera=receta_in.oi_esfera,
        oi_cilindro=receta_in.oi_cilindro,
        oi_eje=receta_in.oi_eje,
        oi_adicion=receta_in.oi_adicion,
        distancia_pupilar=receta_in.distancia_pupilar,
        tipo_lente=receta_in.tipo_lente
    )
    db.add(nueva_receta)
    await db.commit()
    await db.refresh(nueva_receta)
    return nueva_receta

