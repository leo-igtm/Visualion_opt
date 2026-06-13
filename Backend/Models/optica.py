from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Backend.database.dbconnections_opt import Base


class Producto(Base):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True, nullable=False)
    tipoNombre = Column(String(100), nullable=False)  # "lente de contacto", "gafa de sol", "montura", etc.
    precio = Column(Float, nullable=False)
    stockDisponible = Column(Integer, nullable=False)

    # Relaciones
    ventas = relationship("DetalleVenta", back_populates="producto")


class Venta(Base):
    __tablename__ = 'ventas'
    
    id = Column(Integer, primary_key=True)
    numeroComprobante = Column(String(50), unique=True, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    estado_pago = Column(String(50), nullable=False)  # "pendiente", "pagado", "cancelado"
    total = Column(Float, nullable=False)
    
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    vendedor_id = Column(Integer, ForeignKey('vendedores.id'), nullable=False)


    receta_id = Column(Integer, ForeignKey('recetas.uuid'), nullable=True)  # No todas las ventas tienen receta

    # Relaciones
    receta = relationship("RecetaMedica", back_populates="ventas")
    paciente = relationship("Paciente", back_populates="ventas")
    vendedor = relationship("Vendedor", back_populates="ventas")

    items = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")

class DetalleVenta(Base):
    __tablename__ = 'detalleVentas'
    
    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey('ventas.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    # Relaciones
    venta = relationship("Venta", back_populates="items")
    producto = relationship("Producto", back_populates="detalle_ventas")