from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backend.database.dbconnections_opt import Base

#Documentacion de estas clases 

class Persona(Base):
    '''Clase base para personas, con atributos comunes a pacientes y empleados'''
    ''' Incluye campos como DNI, nombre, apellido, teléfono y email, que son esenciales para identificar a cualquier persona en el sistema.
    se relaciona con pacientes y empleados para que puedan heredar estos atributos y agregar los suyos propios.'''
    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    dni: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
    apellido: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(String(100))
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # El discriminador maestro que le dice a SQLAlchemy quién es quién
    tipo_persona: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_on": tipo_persona,
        "polymorphic_identity": "persona"
    }


class Paciente(Persona):
    '''Clase para pacientes, hereda de Persona'''
    ''' Agregamos campos específicos para pacientes, como obra social e historial médico.
    se relaciona con turnos, ventas y recetas para poder acceder a su información médica y comercial.'''
    __tablename__ = "pacientes"
    
    # Su PK es al mismo tiempo la FK que lo une a la tabla personas
    id: Mapped[int] = mapped_column(ForeignKey("personas.id"), primary_key=True)
    
    obra_social: Mapped[str | None] = mapped_column(String(100))
    historial_medico: Mapped[str | None] = mapped_column(String(500))

    __mapper_args__ = {
        "polymorphic_identity": "paciente"
    }
    turnos = relationship("Turno", back_populates="paciente")
    ventas = relationship("Venta", back_populates="paciente")
    recetas = relationship("RecetaMedica", back_populates="paciente")

class Empleado(Persona):
    '''Clase para empleados, hereda de Persona'''
    ''' Agregamos campos específicos para empleados, como legajo, usuario, contraseña y rol.'''
    __tablename__ = "empleados"
    
    # Su PK es al mismo tiempo la FK que lo une a la tabla personas
    id: Mapped[int] = mapped_column(ForeignKey("personas.id"), primary_key=True)
    
    legajo: Mapped[str] = mapped_column(String(50), unique=True)
    usuario: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    contraseña: Mapped[str] = mapped_column(String(255))
    rol: Mapped[str] = mapped_column(String(50)) # "medico", "tecnico", "vendedor"

    __mapper_args__ = {
        # Si creás un empleado general, usará esta identidad
        "polymorphic_identity": "empleado" 
    }

class Medico(Empleado):
    '''Clase para médicos, hereda de Empleado'''
    ''' Agregamos un campo de matrícula para los médicos, que se usará para validar su identidad y experiencia.'''
    __tablename__ = "medicos"
    
    # Su PK se conecta al ID de la tabla empleados
    id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), primary_key=True)
    
    matricula: Mapped[str] = mapped_column(String(50))
    especialidad: Mapped[str] = mapped_column(String(100))

    __mapper_args__ = {
        "polymorphic_identity": "medico"
    }

    turnos = relationship("Turno", back_populates="medico")
    recetas = relationship("RecetaMedica", back_populates="medico")


class Tecnico(Empleado):
    '''Clase para técnicos, hereda de Empleado'''
    ''' Agregamos un campo de matrícula para los técnicos, que se usará para validar su identidad y experiencia.'''
    __tablename__ = "tecnicos"
    
    id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), primary_key=True)
    
    matricula_optico: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "tecnico"
    }


class Vendedor(Empleado):
    '''Clase para vendedores, hereda de Empleado'''
    ''' Agregamos un campo de comisiones para los vendedores, que se actualizará cada vez que realicen una venta.'''
    __tablename__ = "vendedores"
    
    id: Mapped[int] = mapped_column(ForeignKey("empleados.id"), primary_key=True)
    
    comisiones: Mapped[float] = mapped_column(Float, default=0.0)

    __mapper_args__ = {
        "polymorphic_identity": "vendedor"
    }
    ventas = relationship("Venta", back_populates="vendedor")
