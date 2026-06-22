import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from Backend.patterns.singleton import Singleton

load_dotenv()
database_url_raw = os.getenv("DATABASE_URL")

if database_url_raw is None:
    raise RuntimeError("DATABASE_URL no está definido en el entorno.")

database_url: str = database_url_raw


class DatabaseManager(Singleton):
    """
    Gestor de BD - Singleton
    Solo una instancia de conexión en toda la app
    """
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.engine = create_async_engine(database_url, echo=True)
            self.session_factory = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            self._initialized = True

    async def close(self):
        await self.engine.dispose()


db = DatabaseManager()
AsyncSessionLocal = db.session_factory


class Base(DeclarativeBase):
    __abstract__ = True

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
    )

    

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session