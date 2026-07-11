"""
Strategy Pattern Implementation.

Define estrategias intercambiables para procesar pagos.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import ClassVar, Mapping

from ..constants import ComercialConstants


class PaymentStrategy(ABC):
    """Interfaz para estrategias de pago."""

    @abstractmethod
    def validate(self, payment_data: Mapping[str, object]) -> bool:
        """Valida los datos de pago."""
        raise NotImplementedError

    @abstractmethod
    def process(self, amount: Decimal) -> dict[str, str]:
        """Procesa el pago y retorna el resultado."""
        raise NotImplementedError

    @abstractmethod
    def get_fee(self, amount: Decimal) -> Decimal:
        """Calcula la tarifa o comision."""
        raise NotImplementedError


class CashPaymentStrategy(PaymentStrategy):
    """Pago en efectivo."""

    def validate(self, payment_data: Mapping[str, object]) -> bool:
        payment_data.get("amount")  # Solo se requiere la cantidad para efectivo
        return True

    def process(self, amount: Decimal) -> dict[str, str]:
        return {
            "status": "completed",
            "method": "cash",
            "amount": str(amount),
            "timestamp": datetime.now().isoformat(),
            "reference": f"CASH_{datetime.now().timestamp()}",
        }

    def get_fee(self, amount: Decimal) -> Decimal:
        amount = Decimal(amount)
        return Decimal("0.00")


class CreditCardPaymentStrategy(PaymentStrategy):
    """Pago con tarjeta de credito."""

    def validate(self, payment_data: Mapping[str, object]) -> bool:
        required = ("card_number", "cvv", "expiry")
        return all(bool(payment_data.get(field)) for field in required)

    def process(self, amount: Decimal) -> dict[str, str]:
        return {
            "status": "pending",
            "method": "credit_card",
            "amount": str(amount),
            "timestamp": datetime.now().isoformat(),
            "reference": f"CC_{datetime.now().timestamp()}",
        }

    def get_fee(self, amount: Decimal) -> Decimal:
        return amount * Decimal("0.025")


class DebitCardPaymentStrategy(PaymentStrategy):
    """Pago con tarjeta de debito."""

    def validate(self, payment_data: Mapping[str, object]) -> bool:
        required = ("card_number", "cvv", "expiry")
        return all(bool(payment_data.get(field)) for field in required)

    def process(self, amount: Decimal) -> dict[str, str]:
        return {
            "status": "completed",
            "method": "debit_card",
            "amount": str(amount),
            "timestamp": datetime.now().isoformat(),
            "reference": f"DC_{datetime.now().timestamp()}",
        }

    def get_fee(self, amount: Decimal) -> Decimal:
        return amount * Decimal("0.015")


class TransferPaymentStrategy(PaymentStrategy):
    """Pago por transferencia bancaria."""

    def validate(self, payment_data: Mapping[str, object]) -> bool:
        required = ("account_number", "bank_code")
        return all(bool(payment_data.get(field)) for field in required)

    def process(self, amount: Decimal) -> dict[str, str]:
        return {
            "status": "pending",
            "method": "transfer",
            "amount": str(amount),
            "timestamp": datetime.now().isoformat(),
            "reference": f"TRF_{datetime.now().timestamp()}",
        }

    def get_fee(self, amount: Decimal) -> Decimal:
        amount = Decimal(amount)
        return Decimal("50.00")


class CheckPaymentStrategy(PaymentStrategy):
    """Pago con cheque."""

    def validate(self, payment_data: Mapping[str, object]) -> bool:
        required = ("check_number", "bank")
        return all(bool(payment_data.get(field)) for field in required)

    def process(self, amount: Decimal) -> dict[str, str]:
        return {
            "status": "pending",
            "method": "check",
            "amount": str(amount),
            "timestamp": datetime.now().isoformat(),
            "reference": f"CHK_{datetime.now().timestamp()}",
        }

    def get_fee(self, amount: Decimal) -> Decimal:
        amount = Decimal(amount)
        return Decimal("25.00")


class PaymentStrategyFactory:
    """Factory para crear estrategias de pago."""

    _strategy_classes: ClassVar[dict[str, type[PaymentStrategy]]] = {
        "efectivo": CashPaymentStrategy,
        "tarjeta_credito": CreditCardPaymentStrategy,
        "tarjeta_debito": DebitCardPaymentStrategy,
        "transferencia": TransferPaymentStrategy,
        "cheque": CheckPaymentStrategy,
    }

    _legacy_state_to_method: ClassVar[dict[str, str]] = {
        ComercialConstants.ESTADO_PAGO_PAGADO: "efectivo",
    }

    @classmethod
    def get_strategy(cls, method: str) -> PaymentStrategy:
        """Obtiene una estrategia de pago por metodo."""
        if not method or not method.strip():
            raise ValueError("El metodo de pago debe ser una cadena no vacía.")

        normalized_method = method.strip().lower()
        normalized_method = cls._legacy_state_to_method.get(normalized_method, normalized_method)

        strategy_class = cls._strategy_classes.get(normalized_method)
        if strategy_class is None:
            raise ValueError(f"Metodo de pago no soportado: {method}")
        return strategy_class()

    @classmethod
    def get_available_methods(cls) -> list[str]:
        """Retorna la lista de metodos de pago disponibles."""
        return list(cls._strategy_classes.keys())

    @staticmethod
    def get_available_payment_states() -> list[str]:
        """Retorna los estados de pago disponibles para ventas."""
        return [
            ComercialConstants.ESTADO_PAGO_PENDIENTE,
            ComercialConstants.ESTADO_PAGO_PAGADO,
            ComercialConstants.ESTADO_PAGO_FALLIDO,
        ]
