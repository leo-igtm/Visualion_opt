from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from Backend.database.dbconnections_opt import get_db
from Backend.Models.Usuarios import Empleado
from Backend.Schemas.empleado import EmpleadoRegister, UsuarioLogin, TokenResponse, EmpleadoOut, EmpleadoUpdate
from Backend.services.auth_service import AuthService
from Backend.sanitizers.data_sanitizer import DataSanitizer

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
