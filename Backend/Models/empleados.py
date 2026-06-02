from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from Backend.database.dbconnections_opt import Base

class Empleado(Base):
    __tablename__ = "empleados"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre:Mapped[str] = mapped_column(String(100))
    apellido:Mapped[str] = mapped_column(String(100))
    dni:Mapped[str] = mapped_column(String(20), unique=True, index=True)
    usuario:Mapped[str] = mapped_column(String(50), unique=True, index=True)
    contraseña:Mapped[str] = mapped_column(String(100))

    rol:Mapped[str] = mapped_column(String(50))



    __mapper_args__ = {
        "polymorphic_identity": "empleado",
        "polymorphic_on": rol
    }

class Medico(Empleado):
    __tablename__ = "medicos"

    id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), primary_key=True)

    matricula:Mapped[str | None] = mapped_column(String(50))
    especialidad:Mapped[str | None] = mapped_column(String(100))

    __mapper_args__ = {
        "polymorphic_identity": "medico",
    }

class Tecnico(Empleado):
    __tablename__ = "tecnicos"

    id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), primary_key=True)

    area_experiencia:Mapped[str | None] = mapped_column(String(100))

    __mapper_args__ = {
        "polymorphic_identity": "tecnico",
    }

class Vendedor(Empleado):
    __tablename__ = "vendedores"

    id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), primary_key=True)

    legajo: Mapped[str | None] = mapped_column(String(50))
    comisiones: Mapped[float | None] = mapped_column(Float) 

    __mapper_args__ = {
        "polymorphic_identity": "vendedor",
    }