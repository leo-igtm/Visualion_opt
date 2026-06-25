from datetime import datetime
from hashlib import sha1
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.database.dbconnections_opt import get_db
from Backend.Models.Usuarios import Empleado
from Backend.Schemas.empleado import (
    EmpleadoOut,
    EmpleadoRegister,
    EmpleadoUpdate,
    TokenResponse,

)
from Backend.sanitizers.data_sanitizer import DataSanitizer
from Backend.services.auth_service import AuthService
from Backend.services.oauth_service import GitHubOAuthService, GoogleOAuthService, OAuthUserInfo

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


class OAuthCallbackRequest(BaseModel):
    code: str


def _extract_oauth_code(query_code: str | None, body: OAuthCallbackRequest | None) -> str:
    code = query_code or (body.code if body else None)
    if not code or not code.strip():
        raise HTTPException(status_code=422, detail="Codigo OAuth requerido")
    return code.strip()


def _sanitize_update_value(field: str, value: Any) -> Any:
    if value is None:
        return None
    if field == "contraseña":
        return AuthService.hash_password(value)
    if field == "email":
        return DataSanitizer.sanitize_email(value)
    if field == "dni":
        return DataSanitizer.sanitize_dni(value)
    if field == "telefono":
        return DataSanitizer.sanitize_phone(value)
    if isinstance(value, str):
        return DataSanitizer.sanitize_string(value)
    return value


def _split_oauth_name(full_name: str | None, fallback: str) -> tuple[str, str]:
    cleaned_name = DataSanitizer.sanitize_string(full_name or fallback)
    parts = cleaned_name.split(maxsplit=1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return cleaned_name, "OAuth"


async def _get_or_create_oauth_user(
    db: AsyncSession,
    user_info: OAuthUserInfo,
    provider: str,
) -> Empleado:
    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail=f"{provider} no devolvio un email valido")

    email = DataSanitizer.sanitize_email(email)
    query = select(Empleado).where(Empleado.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user:
        return user

    username = user_info.get("username") or email
    display_name = user_info.get("name") or username
    nombre, apellido = _split_oauth_name(display_name, username)
    timestamp = str(datetime.now().timestamp())
    oauth_dni = f"{provider[:3].upper()}_{sha1(email.encode('utf-8')).hexdigest()[:12].upper()}"

    user = Empleado(
        dni=oauth_dni,
        nombre=nombre,
        apellido=apellido,
        email=email,
        usuario=DataSanitizer.sanitize_string(username, max_length=50),
        contraseña=AuthService.hash_password(f"OAUTH_{provider.upper()}_{timestamp}"),
        rol="empleado",
        legajo=f"OAUTH_{provider.upper()}_{timestamp}",
    )
    db.add(user)

    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="El usuario OAuth ya existe")
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear usuario OAuth: {str(exc)}")


@router.post("/register", response_model=EmpleadoOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: EmpleadoRegister, db: AsyncSession = Depends(get_db)):
    """Registrar nuevo empleado."""
    try:
        return await AuthService.register_user(db, user_data)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="El usuario, DNI o email ya existe")
    except ValueError as exc:
        await db.rollback()
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar usuario: {str(exc)}")


@router.post("/login", response_model=TokenResponse)
async def login(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """Loguear usuario."""
    try:
        token = await AuthService.login_user(
            db, form_data.username, form_data.password
        )
        return {"access_token": token}
    except ValueError:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/usuarios", response_model=list[EmpleadoOut])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    """Listar todos los usuarios."""
    try:
        query = select(Empleado)
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/usuarios/{id}", response_model=EmpleadoOut)
async def obtener_usuario(id: int, db: AsyncSession = Depends(get_db)):
    """Obtener usuario por ID."""
    try:
        query = select(Empleado).where(Empleado.id == id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.put("/usuarios/{id}", response_model=EmpleadoOut)
async def actualizar_usuario(id: int, data: EmpleadoUpdate, db: AsyncSession = Depends(get_db)):
    """Actualizar usuario."""
    try:
        query = select(Empleado).where(Empleado.id == id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        for field, value in data.model_dump(exclude_unset=True).items():
            sanitized_value = _sanitize_update_value(field, value)
            if sanitized_value is not None:
                setattr(user, field, sanitized_value)

        await db.commit()
        await db.refresh(user)
        return user
    except HTTPException:
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="El usuario, DNI, email o legajo ya existe")
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("/usuarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(id: int, db: AsyncSession = Depends(get_db)):
    """Eliminar usuario."""
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
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/oauth/google/url")
async def get_google_auth_url():
    """Retorna URL para autenticar con Google."""
    if not GoogleOAuthService.CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth no esta configurado")
    return {"url": GoogleOAuthService.get_auth_url()}


@router.api_route("/oauth/google/callback", methods=["GET", "POST"], response_model=TokenResponse)
async def google_callback(
    code: str | None = Query(default=None),
    body: OAuthCallbackRequest | None = Body(default=None),
    db: AsyncSession = Depends(get_db),
):
    """Callback despues de autenticacion con Google."""
    oauth_code = _extract_oauth_code(code, body)
    user_info = await GoogleOAuthService.verify_token(oauth_code)
    if not user_info:
        raise HTTPException(status_code=401, detail="Google authentication failed")

    user = await _get_or_create_oauth_user(db, user_info, "google")
    token = AuthService.create_user_access_token(user)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/oauth/github/url")
async def get_github_auth_url():
    """Retorna URL para autenticar con GitHub."""
    if not GitHubOAuthService.CLIENT_ID:
        raise HTTPException(status_code=500, detail="GitHub OAuth no esta configurado")
    return {"url": GitHubOAuthService.get_auth_url()}


@router.api_route("/oauth/github/callback", methods=["GET", "POST"], response_model=TokenResponse)
async def github_callback(
    code: str | None = Query(default=None),
    body: OAuthCallbackRequest | None = Body(default=None),
    db: AsyncSession = Depends(get_db),
):
    """Callback despues de autenticacion con GitHub."""
    oauth_code = _extract_oauth_code(code, body)
    user_info = await GitHubOAuthService.verify_token(oauth_code)
    if not user_info:
        raise HTTPException(status_code=401, detail="GitHub authentication failed")

    user = await _get_or_create_oauth_user(db, user_info, "github")
    token = AuthService.create_user_access_token(user)

    return {"access_token": token, "token_type": "bearer"}
