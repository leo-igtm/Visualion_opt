from sqlalchemy import Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backend.database.dbconnections_opt import Base
from datetime import datetime


class EstadoOrden:
    """Estado constants for OrdenTrabajo"""
    RECIBIDA = "recibida"
    BISELADO = "biselado"
    MONTAJE = "montaje"
    CONTROL_CALIDAD = "control_calidad"
    LISTO = "listo"

    @classmethod
    def all_estados(cls) -> list[str]:
        return [cls.RECIBIDA, cls.BISELADO, cls.MONTAJE, cls.CONTROL_CALIDAD, cls.LISTO]


class OrdenTrabajo(Base):
    __tablename__ = 'ordenes_trabajo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey('ventas.id'), nullable=False, unique=True)
    estado: Mapped[str] = mapped_column(String(50), default=EstadoOrden.RECIBIDA, nullable=False)
    descripcion_trabajo: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_entrega_esperada: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default="now()")
    fecha_actualizacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default="now()")

    # Relaciones
    venta = relationship("Venta", back_populates="orden_trabajo")
    etapas = relationship("EtapaTrabajo", back_populates="orden", cascade="all, delete-orphan")
    historico_estados = relationship("HistoricoEstados", back_populates="orden", cascade="all, delete-orphan")


class EtapaTrabajo(Base):
    __tablename__ = 'etapas_trabajo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    orden_id: Mapped[int] = mapped_column(ForeignKey('ordenes_trabajo.id'), nullable=False)
    etapa: Mapped[str] = mapped_column(String(50), nullable=False)
    tecnico_id: Mapped[int | None] = mapped_column(ForeignKey('tecnicos.id'), nullable=True)
    completado: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default="now()")
    fecha_actualizacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default="now()")

    # Relaciones
    orden = relationship("OrdenTrabajo", back_populates="etapas")
    tecnico = relationship("Tecnico")


class HistoricoEstados(Base):
    __tablename__ = 'historico_estados'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    orden_id: Mapped[int] = mapped_column(ForeignKey('ordenes_trabajo.id'), nullable=False)
    estado_anterior: Mapped[str | None] = mapped_column(String(50), nullable=True)
    estado_nuevo: Mapped[str] = mapped_column(String(50), nullable=False)
    tecnico_id: Mapped[int | None] = mapped_column(ForeignKey('tecnicos.id'), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default="now()")

    # Relaciones
    orden = relationship("OrdenTrabajo", back_populates="historico_estados")
    tecnico = relationship("Tecnico")
