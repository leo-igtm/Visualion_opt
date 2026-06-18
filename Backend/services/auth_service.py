from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from Backend.Models.Usuarios import Empleado, Medico, Tecnico, Vendedor
from Backend.sanitizers.data_sanitizer import DataSanitizer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    @staticmethod
    async def register_user(db: AsyncSession, user_data) -> Empleado:
        """Registra nuevo usuario reutilizando estructura existente"""
        # Sanitizar datos
        user_data.nombre = DataSanitizer.sanitize_string(user_data.nombre)
        user_data.apellido = DataSanitizer.sanitize_string(user_data.apellido)
        user_data.email = DataSanitizer.sanitize_email(user_data.email)
        user_data.usuario = DataSanitizer.sanitize_string(user_data.usuario, max_length=50)
        user_data.dni = DataSanitizer.sanitize_dni(user_data.dni)

        # Hash password
        hashed_pw = AuthService.hash_password(user_data.contraseña)

        # Create appropriate subclass based on role
        if user_data.rol == "medico":
            user = Medico(
                dni=user_data.dni,
                nombre=user_data.nombre,
                apellido=user_data.apellido,
                telefono=user_data.telefono,
                email=user_data.email,
                usuario=user_data.usuario,
                contraseña=hashed_pw,
                rol="medico",
                legajo=user_data.legajo,
                matricula=user_data.matricula or "",
                especialidad=user_data.especialidad or ""
            )
        elif user_data.rol == "tecnico":
            user = Tecnico(
                dni=user_data.dni,
                nombre=user_data.nombre,
                apellido=user_data.apellido,
                telefono=user_data.telefono,
                email=user_data.email,
                usuario=user_data.usuario,
                contraseña=hashed_pw,
                rol="tecnico",
                legajo=user_data.legajo,
                matricula_optico=user_data.matricula_optico or ""
            )
        elif user_data.rol == "vendedor":
            user = Vendedor(
                dni=user_data.dni,
                nombre=user_data.nombre,
                apellido=user_data.apellido,
                telefono=user_data.telefono,
                email=user_data.email,
                usuario=user_data.usuario,
                contraseña=hashed_pw,
                rol="vendedor",
                legajo=user_data.legajo,
                comisiones=user_data.comisiones or 0.0
            )
        else:
            user = Empleado(
                dni=user_data.dni,
                nombre=user_data.nombre,
                apellido=user_data.apellido,
                telefono=user_data.telefono,
                email=user_data.email,
                usuario=user_data.usuario,
                contraseña=hashed_pw,
                rol=user_data.rol,
                legajo=user_data.legajo
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

        # TODO: Generar JWT token aquí. Por ahora retorna string simple
        return f"token_{user.id}_{user.usuario}"
