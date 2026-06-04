from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from Backend.database.dbconnections_opt import Base

# =====================================================================
# NIVEL 1: LA CLASE MADRE (La tabla "personas")
# =====================================================================
class Persona(Base):
    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    dni: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
    apellido: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(100))

    # El discriminador maestro que le dice a SQLAlchemy quién es quién
    tipo_persona: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_on": tipo_persona,
        "polymorphic_identity": "persona"
    }


class Paciente(Persona):
    __tablename__ = "pacientes"
    
    # Su PK es al mismo tiempo la FK que lo une a la tabla personas
    id: Mapped[int] = mapped_column(ForeignKey("personas.id"), primary_key=True)
    
    obra_social: Mapped[str | None] = mapped_column(String(100))
    historial_medico: Mapped[str | None] = mapped_column(String(500))

    __mapper_args__ = {
        "polymorphic_identity": "paciente"
    }




# =====================================================================
# NIVEL 2: LAS ESPECIALIZACIONES DIRECTAS
# =====================================================================

class Empleado(Persona):
    __tablename__ = "empleados"
    
    # Su PK es al mismo tiempo la FK que lo une a la tabla personas
    id: Mapped[int] = mapped_column(ForeignKey("personas.id"), primary_key=True)
    
    legajo: Mapped[str] = mapped_column(String(50), unique=True)
    usuario: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    contraseña: Mapped[str] = mapped_column(String(100))
    rol: Mapped[str] = mapped_column(String(50)) # "medico", "tecnico", "vendedor"

    __mapper_args__ = {
        # Si creás un empleado general, usará esta identidad
        "polymorphic_identity": "empleado" 
    }


# =====================================================================
# NIVEL 3: LOS SUBTIPOS DE EMPLEADO (Nietos de Persona)
# =====================================================================

class Medico(Empleado):
    __tablename__ = "medicos"
    
    # Su PK se conecta al ID de la tabla empleados
    id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), primary_key=True)
    
    matricula: Mapped[str] = mapped_column(String(50))
    especialidad: Mapped[str] = mapped_column(String(100))

    __mapper_args__ = {
        "polymorphic_identity": "medico"
    }


class Tecnico(Empleado):
    __tablename__ = "tecnicos"
    
    id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), primary_key=True)
    
    matricula_optico: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "tecnico"
    }


class Vendedor(Empleado):
    __tablename__ = "vendedores"
    
    id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), primary_key=True)
    
    comisiones: Mapped[float] = mapped_column(Float, default=0.0)

    __mapper_args__ = {
        "polymorphic_identity": "vendedor"
    }