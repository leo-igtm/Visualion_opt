from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated

from Backend.database.dbconnections_opt import get_db
from Backend.Schemas import empleado as schemas_empleado
from Backend.Models.Usuarios import Empleado
from Backend.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register", response_model=schemas_empleado.EmpleadoResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: schemas_empleado.PacienteRegister, 
    db: AsyncSession = Depends(get_db)
):
    """
    Registro público para nuevos usuarios. Se crea un Empleado con rol 'paciente'.
    """
    result = await db.execute(select(Empleado).where(Empleado.email == user_data.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = AuthService.hash_password(user_data.password)
    
    # El modelo polimórfico Empleado requiere legajo y usuario.
    # Usamos el email como usuario y generamos un legajo simple.
    new_user = Empleado(
        **user_data.model_dump(exclude={"password"}),
        hashed_password=hashed_password,
        usuario=user_data.email, # Usamos email como nombre de usuario
        legajo=f"P-{user_data.dni}", # Generamos un legajo único para el paciente
        rol="paciente"
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=schemas_empleado.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
):
    """
    Inicia sesión y devuelve un token de acceso JWT.
    """
    # El login se hace con el campo 'usuario', no 'email'. form_data.username es el campo del formulario.
    result = await db.execute(select(Empleado).where(Empleado.usuario == form_data.username))
    user = result.scalars().first()

    if not user or not AuthService.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = AuthService.create_access_token(data={"sub": user.usuario, "rol": user.rol})
    return {"access_token": access_token, "token_type": "bearer"}