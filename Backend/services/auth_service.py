from typing import Any
from passlib.context import CryptContext  # type: ignore[import-not-found]
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from Backend.Models.Usuarios import Empleado, Medico, Tecnico, Vendedor
from Backend.Schemas.empleado import EmpleadoRegister
from Backend.sanitizers.data_sanitizer import DataSanitizer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    '''Servicio de autenticación y registro de usuarios, que incluye funciones para hash de contraseñas, verificación de credenciales y registro de nuevos usuarios.'''
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    @staticmethod
    async def register_user(db: AsyncSession, user_data: EmpleadoRegister) -> Empleado:
        """Registra nuevo usuario con sanitización y creación del subclass correcto según rol"""
        # Obtener datos como dict y sanitizar
        data_dict = user_data.model_dump()

        # Sanitizar campos string
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

        # Hash password
        hashed_pw = AuthService.hash_password(data_dict["contraseña"])

        # Create appropriate subclass based on role
        rol = data_dict.get("rol", "empleado")

        if rol == "medico":
            user = Medico(
                dni=data_dict["dni"],
                nombre=data_dict["nombre"],
                apellido=data_dict["apellido"],
                telefono=data_dict.get("telefono"),
                email=data_dict.get("email"),
                usuario=data_dict["usuario"],
                contraseña=hashed_pw,
                rol="medico",
                legajo=data_dict["legajo"],
                matricula=data_dict.get("matricula") or "",
                especialidad=data_dict.get("especialidad") or ""
            )
        elif rol == "tecnico":
            user = Tecnico(
                dni=data_dict["dni"],
                nombre=data_dict["nombre"],
                apellido=data_dict["apellido"],
                telefono=data_dict.get("telefono"),
                email=data_dict.get("email"),
                usuario=data_dict["usuario"],
                contraseña=hashed_pw,
                rol="tecnico",
                legajo=data_dict["legajo"],
                matricula_optico=data_dict.get("matricula_optico") or ""
            )
        elif rol == "vendedor":
            user = Vendedor(
                dni=data_dict["dni"],
                nombre=data_dict["nombre"],
                apellido=data_dict["apellido"],
                telefono=data_dict.get("telefono"),
                email=data_dict.get("email"),
                usuario=data_dict["usuario"],
                contraseña=hashed_pw,
                rol="vendedor",
                legajo=data_dict["legajo"],
                comisiones=data_dict.get("comisiones") or 0.0
            )
        else:
            user = Empleado(
                dni=data_dict["dni"],
                nombre=data_dict["nombre"],
                apellido=data_dict["apellido"],
                telefono=data_dict.get("telefono"),
                email=data_dict.get("email"),
                usuario=data_dict["usuario"],
                contraseña=hashed_pw,
                rol=rol,
                legajo=data_dict["legajo"]
            )

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def login_user(db: AsyncSession, username: str, password: str) -> str:
        """Autentica usuario y retorna token"""
        query = select(Empleado).where(Empleado.usuario == username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user or not AuthService.verify_password(password, user.contraseña):
            raise ValueError("Credenciales inválidas")

        return f"token_{user.id}_{user.usuario}"
