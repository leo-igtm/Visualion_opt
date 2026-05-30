# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# URL de conexión (reemplaza con tus credenciales)
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/visualion_opt"

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
    
    pass

# Dependencia para usar en las rutas de FastAPI (Inyección de Dependencias)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session