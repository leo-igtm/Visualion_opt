import os
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt  # type: ignore[import-not-found]
from passlib.context import CryptContext  # type: ignore[import-not-found]
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.constants import AuthConstants
from Backend.Models.Usuarios import Empleado, Medico, Tecnico, Vendedor
from Backend.Schemas.empleado import EmpleadoCreate
from Backend.sanitizers.data_sanitizer import DataSanitizer

SECRET_KEY: str = os.getenv("SECRET_KEY", "visualion_secret_key_2024_change_in_production")
ALGORITHM: str = AuthConstants.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_HOURS: int = AuthConstants.JWT_EXPIRATION_HOURS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Servicio de autenticacion JWT con bcrypt para Visualion_Opt."""

    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")[: AuthConstants.BCRYPT_MAX_PASSWORD_BYTES]
        return pwd_context.hash(password_bytes.decode("utf-8"))

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """
        Verifica la contrasena.

        Soporta hashes bcrypt y contrasenas en texto plano de usuarios migrados.
        """
        if hashed.startswith("$2b$") or hashed.startswith("$2a$"):
            try:
                password_bytes = plain.encode("utf-8")[: AuthConstants.BCRYPT_MAX_PASSWORD_BYTES]
                return pwd_context.verify(password_bytes.decode("utf-8"), hashed)
            except Exception:
                return False
        return plain == hashed

    @staticmethod
    def create_access_token(
        data: dict[str, Any],
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta if expires_delta else timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def create_user_access_token(user: Empleado) -> str:
        return AuthService.create_access_token(
            {
                "sub": str(user.id),
                "usuario": str(user.usuario),
                "rol": str(user.rol),
            }
        )

    @staticmethod
    def decode_token(token: str) -> dict[str, Any] | None:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except Exception:
            return None

    @staticmethod
    async def login_user(db: AsyncSession, username: str, password: str) -> str:
        """Autentica usuario y retorna un JWT firmado."""
        query = select(Empleado).where(Empleado.usuario == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user or not AuthService.verify_password(password, user.hashed_password):
            raise ValueError("Credenciales invalidas")

        if not (user.hashed_password.startswith("$2b$") or user.hashed_password.startswith("$2a$")):
            user.hashed_password = AuthService.hash_password(password)
            await db.commit()

        return AuthService.create_user_access_token(user)

    @staticmethod
    async def register_user(db: AsyncSession, user_data: EmpleadoCreate) -> Empleado:
        """Registra nuevo usuario con sanitizacion y crea el subclass correcto segun rol."""
        data_dict = user_data.model_dump()

        if data_dict.get("nombre"):
            data_dict["nombre"] = DataSanitizer.sanitize_string(data_dict["nombre"])
        if data_dict.get("apellido"):
            data_dict["apellido"] = DataSanitizer.sanitize_string(data_dict["apellido"])
        if data_dict.get("email"):
            data_dict["email"] = DataSanitizer.sanitize_email(data_dict["email"])
        if data_dict.get("usuario"):
            data_dict["usuario"] = DataSanitizer.sanitize_string(data_dict["usuario"], max_length=50)
        if data_dict.get("dni"):
            data_dict["dni"] = DataSanitizer.sanitize_dni(data_dict["dni"])

        hashed_pw = AuthService.hash_password(user_data.password) # Use user_data.password
        rol = data_dict.get("rol", "empleado")

        if rol == "medico":
            user: Empleado = Medico(
                dni=data_dict["dni"],
                nombre=data_dict["nombre"],
                apellido=data_dict["apellido"],
                telefono=data_dict.get("telefono"),
                email=data_dict.get("email"),
                usuario=data_dict["usuario"],
                hashed_password=hashed_pw, # Use hashed_password
                rol="medico",
                legajo=data_dict["legajo"],
                matricula=data_dict.get("matricula") or "",
                especialidad=data_dict.get("especialidad") or "",
            )
        elif rol == "tecnico":
            user = Tecnico(
                dni=data_dict["dni"],
                nombre=data_dict["nombre"],
                apellido=data_dict["apellido"],
                telefono=data_dict.get("telefono"),
                email=data_dict.get("email"),
                usuario=data_dict["usuario"],
                hashed_password=hashed_pw, # Use hashed_password
                rol="tecnico",
                legajo=data_dict["legajo"],
                matricula_optico=data_dict.get("matricula_optico") or "",
            )
        elif rol == "vendedor":
            user = Vendedor(
                dni=data_dict["dni"],
                nombre=data_dict["nombre"],
                apellido=data_dict["apellido"],
                telefono=data_dict.get("telefono"),
                email=data_dict.get("email"),
                usuario=data_dict["usuario"],
                hashed_password=hashed_pw, # Use hashed_password
                rol="vendedor",
                legajo=data_dict["legajo"],
                comisiones=data_dict.get("comisiones") or 0.0,
            )
        else: # Default to Empleado
            user = Empleado(
                dni=data_dict["dni"],
                nombre=data_dict["nombre"],
                apellido=data_dict["apellido"],
                telefono=data_dict.get("telefono"),
                email=data_dict.get("email"),
                usuario=data_dict["usuario"],
                hashed_password=hashed_pw, # Use hashed_password
                rol=rol,
                legajo=data_dict["legajo"],
            )

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
