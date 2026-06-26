from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Type, Union
from sqlalchemy.exc import IntegrityError

from Backend.database.dbconnections_opt import get_db
from Backend.Schemas import empleado as schemas_empleado
from Backend.Models.Usuarios import Empleado, Medico, Tecnico, Vendedor
from Backend.dependencies import get_current_active_admin_user
from Backend.services.auth_service import AuthService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_active_admin_user)] # Protege todas las rutas de este router
)

#crear empleados medico,tecnico,vendedor

@router.post("/create-employee", response_model=schemas_empleado.EmpleadoResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_data: schemas_empleado.EmpleadoCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas_empleado.EmpleadoResponse: # Add return type hint
    """
    Endpoint solo para administradores para crear un nuevo empleado con un rol específico.
    Este endpoint es robusto: valida y selecciona los campos adecuados según el rol.
    """
    result = await db.execute(select(Empleado).where(Empleado.usuario == employee_data.usuario))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")

    allowed_roles = {"medico", "vendedor", "tecnico", "admin"}
    if employee_data.rol not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rol no válido. Roles permitidos: {', '.join(allowed_roles)}"
        )

    hashed_password = AuthService.hash_password(employee_data.password)

    # Define a type alias for the employee model classes
    EmployeeModelType = Union[Type[Empleado], Type[Medico], Type[Tecnico], Type[Vendedor]]

    # Preparamos los datos del empleado. El campo 'rol' se obtiene directamente
    # del model_dump() y ya no se excluye.
    employee_model_data = employee_data.model_dump(
        exclude={"password", "matricula", "especialidad", "matricula_optico", "comisiones"}
    )
    employee_model_data['contraseña'] = hashed_password

    rol_class_map: dict[str, EmployeeModelType] = { # Add type hint
        "medico": Medico,
        "tecnico": Tecnico,
        "vendedor": Vendedor,
        "admin": Empleado,
    }
    EmpleadoClass: EmployeeModelType = rol_class_map[employee_data.rol] # Add type hint

    # Añadimos los campos específicos del rol y validamos su presencia
    if employee_data.rol == "medico":
        if employee_data.matricula is None or employee_data.especialidad is None:
            raise HTTPException(status_code=400, detail="El rol 'medico' requiere 'matricula' y 'especialidad'.")
        employee_model_data["matricula"] = employee_data.matricula
        employee_model_data["especialidad"] = employee_data.especialidad
    elif employee_data.rol == "tecnico":
        if employee_data.matricula_optico is None:
            raise HTTPException(status_code=400, detail="El rol 'tecnico' requiere 'matricula_optico'.")
        employee_model_data["matricula_optico"] = employee_data.matricula_optico
    elif employee_data.rol == "vendedor":
        if employee_data.comisiones is not None:
            employee_model_data["comisiones"] = employee_data.comisiones
    # Para 'admin', no se necesitan campos adicionales. 'rol' ya está incluido.

    # Creamos la instancia de forma segura
    try:
        new_employee: Empleado = EmpleadoClass(**employee_model_data) # Add type hint
        db.add(new_employee)
        await db.commit()
        await db.refresh(new_employee)
    except IntegrityError as e:
        await db.rollback() # Important to rollback on error
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, # 409 Conflict for integrity errors
            detail=f"Error de integridad de datos: {e.orig.pgerror if hasattr(e.orig, 'pgerror') else e.orig}"
        )
    except TypeError as e:
        await db.rollback() # Rollback in case of type error before commit
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de tipo al crear empleado. Verifique los campos: {e}"
        )
    except Exception as e: # Catch all other unexpected errors
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor al crear empleado: {e}"
        )
    
    return new_employee