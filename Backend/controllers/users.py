from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Type, Union
from sqlalchemy.exc import IntegrityError
from psycopg.errors import UniqueViolation

from Backend.database.dbconnections_opt import get_db
from Backend.Schemas.empleado import EmpleadoResponse, PacienteCreate, PacienteResponse, UserCreate
from Backend.Models.Usuarios import Empleado, Medico, Tecnico, Vendedor, Paciente, Persona

router = APIRouter(
    prefix="/users",
    tags=["Users"],
     # Protege todas las rutas de este router
)

#crear empleados medico,tecnico,vendedor y pacientes

UserModelType = Union[Type[Empleado], Type[Medico], Type[Tecnico], Type[Vendedor], Type[Paciente]]

@router.post("/create", response_model=Union[EmpleadoResponse, PacienteResponse], status_code=status.HTTP_201_CREATED)
async def create_user(
    # Usamos la Union Discriminada. FastAPI usará el campo 'rol' para validar el schema correcto.
    user_data: UserCreate = Body(..., discriminator="rol"),
    db: AsyncSession = Depends(get_db)
) -> Persona:
    """
    Endpoint solo para administradores para crear un nuevo usuario con un rol específico.
    Gracias a los esquemas Pydantic, la validación de campos por rol es automática.
    Puede crear: Paciente, Medico, Vendedor, Tecnico, Admin.
    """
    # 1. Lógica para crear un Paciente
    if isinstance(user_data, PacienteCreate):
        # Verificamos si ya existe un paciente con el mismo DNI
        existing_paciente = await db.execute(select(Paciente).where(Paciente.dni == user_data.dni))
        if existing_paciente.scalars().first():
            raise HTTPException(status_code=409, detail="Ya existe un paciente con este DNI.")
        
        # Creamos la instancia del modelo Paciente
        new_user = Paciente(**user_data.model_dump())

    # 2. Lógica para crear cualquier tipo de Empleado
    else:
        # Verificamos si ya existe un empleado con el mismo usuario o DNI
        existing_empleado = await db.execute(
            select(Empleado).where(
                (Empleado.usuario == user_data.usuario) | (Empleado.dni == user_data.dni)
            )
        )
        if existing_empleado.scalars().first():
            raise HTTPException(status_code=409, detail="Ya existe un empleado con este usuario o DNI.")

        # Hasheamos la contraseña antes de guardarla
        # Preparamos los datos para el modelo SQLAlchemy
        model_data = user_data.model_dump(exclude={"password"})

        # Mapeamos el rol del schema al modelo SQLAlchemy correspondiente
        rol_class_map: dict[str, UserModelType] = {
            "medico": Medico,
            "tecnico": Tecnico,
            "vendedor": Vendedor,
            "admin": Empleado,
        }
        UserClass = rol_class_map[user_data.rol]
        
        # Creamos la instancia del modelo de Empleado (o subclase)
        new_user = UserClass(**model_data)

    # 3. Guardamos en la base de datos y manejamos errores
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError as e:
        await db.rollback()
        # Capturamos violaciones de unicidad (ej. DNI, usuario)
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Conflicto de datos: un campo único ya existe. Detalle: {e.orig.diag.message_detail}"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de integridad no manejado: {e.orig}"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor al crear usuario: {e}"
        )

    return new_user