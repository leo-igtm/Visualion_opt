#crear data base de empleados en postgres y agregar funciones para insertar, eliminar, actualizar y consultar empleados
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database.dbconnections_opt import declarative_base

Base = declarative_base()

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

    matricula:Mapped[str | None] = mapped_column(String(50))
    especialidad:Mapped[str | None] = mapped_column(String(100))

    __mapper_args__ = {
        "polymorphic_identity": "medico",
    }

class Tecnico(Empleado):
    __tablename__ = "tecnicos"

    area_experiencia:Mapped[str | None] = mapped_column(String(100))

    __mapper_args__ = {
        "polymorphic_identity": "tecnico",
    }

