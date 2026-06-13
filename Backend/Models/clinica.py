from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import Float
from sqlalchemy.orm import relationship
from Backend.database.dbconnections_opt import Base

class Turno(Base):
    __tablename__ = 'turnos'
    id = Column(Integer, primary_key=True)
    fecha_hora = Column(DateTime, nullable=False)
    motivo = Column(String(255), nullable=False)
    estado = Column(String(50), nullable=False ,default="pendiente")  # "pendiente", "completado", "cancelado"

    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    medico_id = Column(Integer, ForeignKey('medicos.id'), nullable=False)

    paciente = relationship("Paciente", back_populates="turnos")
    medico = relationship("Medico", back_populates="turnos")
    receta = relationship("RecetaMedica", back_populates="turno", uselist=False)


class RecetaMedica(Base):
    __tablename__ = 'recetas'
    uuid = Column(Integer, primary_key=True)
    turno_id = Column(Integer, ForeignKey('turnos.id'), nullable=False)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    medico_id = Column(Integer, ForeignKey('medicos.id'), nullable=False)

    fecha_emision = Column(DateTime, nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=False)

    # ---- GRADUACIÓN OJO DERECHO (OD) ----
    od_esfera = Column(Float, default=0.0)
    od_cilindro = Column(Float, default=0.0)
    od_eje = Column(Integer, default=0)
    od_adicion = Column(Float, default=0.0)

    # ---- GRADUACIÓN OJO IZQUIERDO (OI) ----
    oi_esfera = Column(Float, default=0.0)
    oi_cilindro = Column(Float, default=0.0)
    oi_eje = Column(Integer, default=0)
    oi_adicion = Column(Float, default=0.0)

    distancia_pupilar = Column(Float, nullable=True)
    tipo_lente = Column(String(50), nullable=True)  # "monofocal", "bifocal", "progresiva"
    # Relaciones
    turno = relationship("Turno", back_populates="receta")
    ventas = relationship("Venta", back_populates="receta")
    paciente = relationship("Paciente", back_populates="recetas")
    medico = relationship("Medico", back_populates="recetas")