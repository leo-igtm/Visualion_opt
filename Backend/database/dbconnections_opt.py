import os
from dotenv import load_dotenv
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


class _DatabaseSingleton:
    _instance: "_DatabaseSingleton | None" = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_async_engine(DATABASE_URL, echo=True)
            cls._instance.session_factory = async_sessionmaker(
                bind=cls._instance.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
        return cls._instance


db = _DatabaseSingleton()
AsyncSessionLocal = db.session_factory


class Base(DeclarativeBase):
    __abstract__ = True

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session