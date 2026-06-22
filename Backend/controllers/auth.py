from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from Backend.database.dbconnections_opt import get_db
from Backend.Models.Usuarios import Empleado
from Backend.Schemas.empleado import EmpleadoRegister, UsuarioLogin, TokenResponse, EmpleadoOut, EmpleadoUpdate
from Backend.services.auth_service import AuthService
from Backend.services.oauth_service import GoogleOAuthService, GitHubOAuthService
from Backend.sanitizers.data_sanitizer import DataSanitizer
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=EmpleadoOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: EmpleadoRegister, db: AsyncSession = Depends(get_db)):
    """Registrar nuevo empleado"""
    
    try:
        new_user = await AuthService.register_user(db, user_data)
        return new_user
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail="El usuario, DNI o email ya existe")
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar usuario: {str(e)}")
        


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UsuarioLogin, db: AsyncSession = Depends(get_db)):
    """Logear usuario"""
    try:
        token = await AuthService.login_user(db, login_data.usuario, login_data.contraseña)
        return {"access_token": token}
    except ValueError:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuarios", response_model=list[EmpleadoOut])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    """Listar todos los usuarios (CRUD Read)"""
    try:
        query = select(Empleado)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuarios/{id}", response_model=EmpleadoOut)
async def obtener_usuario(id: int, db: AsyncSession = Depends(get_db)):
    """Obtener usuario por ID"""
    try:
        query = select(Empleado).where(Empleado.id == id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/usuarios/{id}", response_model=EmpleadoOut)
async def actualizar_usuario(id: int, data: EmpleadoUpdate, db: AsyncSession = Depends(get_db)):
    """Actualizar usuario (CRUD Update)"""
    try:
        query = select(Empleado).where(Empleado.id == id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Sanitizar y actualizar campos
        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                if field == "contraseña":
                    value = AuthService.hash_password(value)
                elif isinstance(value, str):
                    value = DataSanitizer.sanitize_string(value)
                setattr(user, field, value)

        await db.commit()
        await db.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/usuarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(id: int, db: AsyncSession = Depends(get_db)):
    """Eliminar usuario (CRUD Delete)"""
    try:
        query = select(Empleado).where(Empleado.id == id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        await db.delete(user)
        await db.commit()
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/oauth/google/url")
async def get_google_auth_url():
    """Retorna URL para autenticar con Google"""
    if not GoogleOAuthService.CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth no está configurado")
    return {"url": GoogleOAuthService.get_auth_url()}


@router.post("/oauth/google/callback")
async def google_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Callback después de autenticación con Google"""

    user_info = await GoogleOAuthService.verify_token(code)

    if not user_info:
        raise HTTPException(status_code=401, detail="Google authentication failed")

    # Crear o obtener usuario
    query = select(Empleado).where(Empleado.email == user_info["email"])
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        # Crear nuevo usuario con Google
        user = Empleado(
            dni="GOOGLE_" + user_info["email"],
            nombre=user_info.get("name", "Google User"),
            email=user_info["email"],
            usuario=user_info["email"],
            contraseña="OAUTH_GOOGLE",
            rol="empleado",
            legajo="OAUTH_" + str(datetime.now().timestamp())
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Generar JWT
    token = AuthService.hash_password(str(user.id))

    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "nombre": user.nombre,
            "provider": "google"
        }
    }


@router.get("/oauth/github/url")
async def get_github_auth_url():
    """Retorna URL para autenticar con GitHub"""
    if not GitHubOAuthService.CLIENT_ID:
        raise HTTPException(status_code=500, detail="GitHub OAuth no está configurado")
    return {"url": GitHubOAuthService.get_auth_url()}


@router.post("/oauth/github/callback")
async def github_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Callback después de autenticación con GitHub"""

    user_info = await GitHubOAuthService.verify_token(code)

    if not user_info:
        raise HTTPException(status_code=401, detail="GitHub authentication failed")

    # Crear o obtener usuario
    query = select(Empleado).where(Empleado.email == user_info["email"])
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        # Crear nuevo usuario con GitHub
        user = Empleado(
            dni="GITHUB_" + user_info.get("username", user_info["email"]),
            nombre=user_info.get("name", user_info.get("username", "GitHub User")),
            email=user_info["email"],
            usuario=user_info.get("username", user_info["email"]),
            contraseña="OAUTH_GITHUB",
            rol="empleado",
            legajo="OAUTH_" + str(datetime.now().timestamp())
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Generar JWT
    token = AuthService.hash_password(str(user.id))

    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "nombre": user.nombre,
            "username": user_info.get("username"),
            "provider": "github"
        }
    }

