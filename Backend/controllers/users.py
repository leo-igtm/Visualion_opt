from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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

@router.post("/create-employee", response_model=schemas_empleado.EmpleadoResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_data: schemas_empleado.EmpleadoCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint solo para administradores para crear un nuevo empleado con un rol específico.
    """
    result = await db.execute(select(Empleado).where(Empleado.usuario == employee_data.usuario))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Username already registered")

    allowed_roles = {"medico", "vendedor", "tecnico", "admin"}
    if employee_data.rol not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rol no válido. Roles permitidos: {', '.join(allowed_roles)}"
        )

    hashed_password = AuthService.hash_password(employee_data.password)

    # Usamos el modelo polimórfico correcto según el rol
    rol_class_map = {
        "medico": Medico,
        "tecnico": Tecnico,
        "vendedor": Vendedor,
        "admin": Empleado, # Un admin es un Empleado base
    }
    
    EmpleadoClass = rol_class_map[employee_data.rol]
    
    # Creamos la instancia del empleado con todos sus datos
    new_employee = EmpleadoClass(
        **employee_data.model_dump(exclude={"password"}),
        hashed_password=hashed_password
    )

    db.add(new_employee)
    await db.commit()
    await db.refresh(new_employee)
    
    return new_employee