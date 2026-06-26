from datetime import datetime, timedelta, timezone
from typing import Optional, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Backend.database.dbconnections_opt import get_db
from Backend.Models.Usuarios import Empleado
from Backend.Schemas.empleado import TokenData
from .config import settings
from .security import verify_password

# This tells FastAPI where to look for the token.
# The tokenUrl should match the path to your login endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[Empleado]:
    """
    Authenticates a user by checking the database.
    """
    result = await db.execute(select(Empleado).where(Empleado.usuario == username))
    user = result.scalars().first()
    if not user:
        return None
    if not verify_password(password, user.contraseña):
        return None
    return user

def create_access_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None):
    """
    Creates a new JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> Empleado:
    """
    Dependency to get the current authenticated user from a token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(usuario=username)
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(Empleado).where(Empleado.usuario == token_data.usuario))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
    return user