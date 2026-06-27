import enum
from datetime import datetime
from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Enum as SQLAlchemyEnum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backend.database.dbconnections_opt import Base


class Producto(Base):
    __tablename__ = "productos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    tipoNombre: Mapped[str] = mapped_column("tipoNombre", String(100), nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    stockDisponible: Mapped[int] = mapped_column("stockDisponible", Integer, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    detalles_venta = relationship("DetalleVenta", back_populates="producto")


class Venta(Base):
    __tablename__ = "ventas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numeroComprobante: Mapped[str] = mapped_column("numeroComprobante", String(50), unique=True, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    estado_pago: Mapped[str] = mapped_column(String(50), nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"), nullable=False)
    vendedor_id: Mapped[int] = mapped_column(ForeignKey("vendedores.id"), nullable=False)
    receta_id: Mapped[int | None] = mapped_column(ForeignKey("recetas.uuid"))
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    paciente = relationship("Paciente", back_populates="ventas")
    vendedor = relationship("Vendedor", back_populates="ventas")
    receta = relationship("RecetaMedica", back_populates="venta")
    detalles = relationship("DetalleVenta", back_populates="venta")
    orden_trabajo = relationship("OrdenTrabajo", back_populates="venta", uselist=False)


class DetalleVenta(Base):
    __tablename__ = "detalleVentas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("ventas.id"), nullable=False)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")

class EstadoOrden(str, enum.Enum):
    RECIBIDA = "recibida"
    EN_PROCESO = "en_proceso"
    LISTA_PARA_ENTREGA = "lista_para_entrega"
    ENTREGADA = "entregada"
    CANCELADA = "cancelada"


class OrdenTrabajo(Base):
    __tablename__ = "ordenes_trabajo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("ventas.id"), unique=True, nullable=False)
    estado: Mapped[EstadoOrden] = mapped_column(SQLAlchemyEnum(EstadoOrden), default=EstadoOrden.RECIBIDA, nullable=False)
    descripcion_trabajo: Mapped[str | None] = mapped_column(Text)
    fecha_entrega_esperada: Mapped[datetime | None] = mapped_column(DateTime)

    venta = relationship("Venta", back_populates="orden_trabajo")
    etapas = relationship("EtapaTrabajo", back_populates="orden")
    historico_estados = relationship("HistoricoEstado", back_populates="orden")


class EtapaTrabajo(Base):
    __tablename__ = "etapas_trabajo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column(ForeignKey("ordenes_trabajo.id"), nullable=False)
    tecnico_id: Mapped[int | None] = mapped_column(ForeignKey("tecnicos.id"))
    etapa: Mapped[str] = mapped_column(String(50), nullable=False)
    completado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notas: Mapped[str | None] = mapped_column(Text)

    orden = relationship("OrdenTrabajo", back_populates="etapas")
    tecnico = relationship("Tecnico", back_populates="etapas_trabajo")


class HistoricoEstado(Base):
    __tablename__ = "historico_estados"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column(ForeignKey("ordenes_trabajo.id"), nullable=False)
    tecnico_id: Mapped[int | None] = mapped_column(ForeignKey("tecnicos.id"))
    estado_anterior: Mapped[EstadoOrden | None] = mapped_column(SQLAlchemyEnum(EstadoOrden))
    estado_nuevo: Mapped[EstadoOrden] = mapped_column(SQLAlchemyEnum(EstadoOrden), nullable=False)

    orden = relationship("OrdenTrabajo", back_populates="historico_estados")
    tecnico = relationship("Tecnico", back_populates="historico_estados")