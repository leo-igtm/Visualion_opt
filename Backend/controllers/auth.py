from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated, Union, Type

from Backend.database.dbconnections_opt import get_db
from Backend.Schemas import empleado as schemas_empleado
from Backend.Models.Usuarios import Persona, Empleado, Medico, Tecnico, Vendedor, Paciente
from Backend.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# Se usa Union en el response_model para que FastAPI pueda devolver el schema correcto
# tanto si se crea un Empleado como un Paciente.
@router.post("/register",
            response_model=Union[schemas_empleado.EmpleadoResponse, schemas_empleado.PacienteResponse],
            status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: schemas_empleado.EmpleadoCreate, 
    db: AsyncSession = Depends(get_db)
) -> Union[schemas_empleado.EmpleadoResponse, schemas_empleado.PacienteResponse]:
    """
    Registro para nuevos empleados/usuarios con roles.
    Este endpoint es usado para poblar la base de datos (seeding).
    """
    result = await db.execute(select(Persona).where(Persona.email == user_data.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail=f"Email '{user_data.email}' already registered")

    result = await db.execute(select(Persona).where(Persona.usuario == user_data.usuario))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail=f"Username '{user_data.usuario}' already registered")

    hashed_password = AuthService.hash_password(user_data.password)
        
    # Determinar la clase del modelo polimórfico a instanciar
    role_class_map: dict[str, Type[Persona]] = {
        "medico": Medico,
        "tecnico": Tecnico,
        "vendedor": Vendedor,
        "admin": Empleado,
        "paciente": Paciente
    }
    
    ModelClass = role_class_map.get(user_data.rol)
    if not ModelClass:
        raise HTTPException(status_code=400, detail=f"Role '{user_data.rol}' is not valid for registration via this endpoint.")

    create_data_raw = user_data.model_dump(exclude={"password"})

    # Filtra los datos para evitar TypeErrors, ya que EmpleadoCreate tiene campos para todos los roles.
    if user_data.rol == "paciente":
        allowed_fields = {'dni', 'nombre', 'apellido', 'telefono', 'email', 'usuario', 'obra_social', 'historial_medico'}
        create_data = {k: v for k, v in create_data_raw.items() if k in allowed_fields}
    else: # Para tipos de Empleado
        # Esta es una creación simplificada. Para más detalles (ej. matrícula de médico), usar /users/create-employee
        allowed_fields = {'dni', 'nombre', 'apellido', 'telefono', 'email', 'usuario', 'legajo', 'rol'}
        create_data = {k: v for k, v in create_data_raw.items() if k in allowed_fields}
    
    # Crear la instancia del usuario
    new_user: Persona = ModelClass(
        **create_data,
        contraseña=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Pydantic V2 usa `model_validate` para crear un esquema a partir de un objeto ORM.
    # Aunque FastAPI puede hacer esta conversión implícitamente gracias al decorador `response_model`,
    # ser explícito aquí satisface al analizador de tipos (Pylance) y elimina la advertencia.
    if isinstance(new_user, Paciente):
        return schemas_empleado.PacienteResponse.model_validate(new_user)
    else:
        return schemas_empleado.EmpleadoResponse.model_validate(new_user)

@router.post("/login", response_model=schemas_empleado.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
):
    """
    Inicia sesión y devuelve un token de acceso JWT.
    """
    # Se busca en la tabla base 'Persona' para permitir login de Empleados y Pacientes.
    result = await db.execute(select(Persona).where(Persona.usuario == form_data.username))
    user = result.scalars().first()

    # Verifica que el usuario exista, que tenga el atributo contraseña y que la contraseña sea correcta.
    if not user or not user.contraseña or not AuthService.verify_password(form_data.password, user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # El rol para el token se obtiene del campo 'rol' si es un Empleado, o se asigna 'paciente' si es un Paciente.
    user_role = getattr(user, 'rol', 'paciente')

    access_token = AuthService.create_access_token(data={"sub": user.usuario, "rol": user_role})
    return {"access_token": access_token, "token_type": "bearer"}