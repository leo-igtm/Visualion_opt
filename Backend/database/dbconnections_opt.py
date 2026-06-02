# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase , Mapped , mapped_column
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func

# URL de conexión (reemplaza con tus credenciales)
DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5432/visualion_opt"

# SINGLETON: Creamos el motor asíncrono una sola vez para toda la app
engine = create_async_engine(DATABASE_URL, echo=True)

# Fábrica para generar sesiones asíncronas en cada petición
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Clase base de la que heredarán todos nuestros modelos ORM
class Base(DeclarativeBase):
    
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

    # Fecha en la que se modifica el registro por última vez
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )
    
    pass

# Dependencia para usar en las rutas de FastAPI (Inyección de Dependencias)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session