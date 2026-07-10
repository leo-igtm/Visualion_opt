from sqlalchemy import Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.dbconnections_opt import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Usuarios import Paciente, Medico
    from .optica import Venta


class Turno(Base):
    __tablename__ = 'turnos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_hora: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    motivo: Mapped[str] = mapped_column(String(255), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False, default="pendiente")  # "pendiente", "completado", "cancelado"

    paciente_id: Mapped[int] = mapped_column(ForeignKey('pacientes.id'), nullable=False)
    medico_id: Mapped[int] = mapped_column(ForeignKey('medicos.id'), nullable=False)

    paciente: Mapped["Paciente"] = relationship("Paciente", back_populates="turnos")
    medico: Mapped["Medico"] = relationship("Medico", back_populates="turnos")
    receta: Mapped["RecetaMedica"] = relationship("RecetaMedica", back_populates="turno", uselist=False)


class RecetaMedica(Base):
    __tablename__ = 'recetas'
    uuid: Mapped[int] = mapped_column(Integer, primary_key=True)
    turno_id: Mapped[int | None] = mapped_column(ForeignKey('turnos.id'), nullable=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey('pacientes.id'), nullable=False)
    medico_id: Mapped[int] = mapped_column(ForeignKey('medicos.id'), nullable=False)

    fecha_emision: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    fecha_vencimiento: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    # ---- GRADUACIÓN OJO DERECHO (OD) ----
    od_esfera: Mapped[float] = mapped_column(Float, default=0.0)
    od_cilindro: Mapped[float] = mapped_column(Float, default=0.0)
    od_eje: Mapped[int] = mapped_column(Integer, default=0)
    od_adicion: Mapped[float] = mapped_column(Float, default=0.0)

    # ---- GRADUACIÓN OJO IZQUIERDO (OI) ----
    oi_esfera: Mapped[float] = mapped_column(Float, default=0.0)
    oi_cilindro: Mapped[float] = mapped_column(Float, default=0.0)
    oi_eje: Mapped[int] = mapped_column(Integer, default=0)
    oi_adicion: Mapped[float] = mapped_column(Float, default=0.0)

    distancia_pupilar: Mapped[float | None] = mapped_column(Float, nullable=True)
    tipo_lente: Mapped[str | None] = mapped_column(String(50), nullable=True)  # "monofocal", "bifocal", "progresiva"
    # Relaciones
    turno: Mapped["Turno"] = relationship("Turno", back_populates="receta")
    ventas: Mapped[list["Venta"]] = relationship("Venta", back_populates="receta")
    paciente: Mapped["Paciente"] = relationship("Paciente", back_populates="recetas")
    medico: Mapped["Medico"] = relationship("Medico", back_populates="recetas")