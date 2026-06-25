from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backend.database.dbconnections_opt import Base
from Backend.patterns.strategy import PaymentStrategyFactory
from decimal import Decimal


class Producto(Base):
    __tablename__ = 'productos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    tipoNombre: Mapped[str] = mapped_column(String(100), nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    stockDisponible: Mapped[int] = mapped_column(Integer, nullable=False)

    detalles = relationship("DetalleVenta", back_populates="producto")


class Venta(Base):
    __tablename__ = 'ventas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numeroComprobante: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    estado_pago: Mapped[str] = mapped_column(String(50), nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)

    paciente_id: Mapped[int] = mapped_column(ForeignKey('pacientes.id'), nullable=False)
    vendedor_id: Mapped[int] = mapped_column(ForeignKey('vendedores.id'), nullable=False)
    receta_id: Mapped[int | None] = mapped_column(ForeignKey('recetas.uuid'), nullable=True)

    receta = relationship("RecetaMedica", back_populates="ventas")
    paciente = relationship("Paciente", back_populates="ventas")
    vendedor = relationship("Vendedor", back_populates="ventas")
    orden_trabajo = relationship("OrdenTrabajo", back_populates="venta", uselist=False, cascade="all, delete-orphan")
    items = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")

    def get_payment_strategy(self, metodo_pago: str):
        """Obtiene estrategia de pago según método"""
        return PaymentStrategyFactory.get_strategy(metodo_pago)

    def procesar_pago(self, metodo_pago: str, payment_data: dict) -> dict:
        """Procesa pago usando estrategia"""
        strategy = self.get_payment_strategy(metodo_pago)

        if not strategy.validate(payment_data):
            raise ValueError("Datos de pago inválidos")

        amount = Decimal(str(self.total))
        fee = strategy.get_fee(amount)
        result = strategy.process(amount)

        return {
            "result": result,
            "fee": str(fee),
            "total_with_fee": str(amount + fee)
        }


class DetalleVenta(Base):
    __tablename__ = 'detalleVentas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey('ventas.id'), nullable=False)
    producto_id: Mapped[int] = mapped_column(ForeignKey('productos.id'), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    venta = relationship("Venta", back_populates="items")
    producto = relationship("Producto", back_populates="detalles")
