"""
Strategy Pattern Implementation
Define una familia de algoritmos, encapsula cada uno,
y hacen intercambiables
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from datetime import datetime


class PaymentStrategy(ABC):
    """
    Interfaz para estrategias de pago
    """

    @abstractmethod
    def validate(self, payment_data: dict) -> bool:
        """Valida los datos de pago"""
        pass

    @abstractmethod
    def process(self, amount: Decimal) -> dict:
        """Procesa el pago y retorna resultado"""
        pass

    @abstractmethod
    def get_fee(self, amount: Decimal) -> Decimal:
        """Calcula la tarifa o comisión"""
        pass


class CashPaymentStrategy(PaymentStrategy):
    """Pago en efectivo"""

    def validate(self, payment_data: dict) -> bool:
        return True

    def process(self, amount: Decimal) -> dict:
        return {
            "status": "completed",
            "method": "cash",
            "amount": str(amount),
            "timestamp": datetime.now().isoformat(),
            "reference": f"CASH_{datetime.now().timestamp()}"
        }

    def get_fee(self, amount: Decimal) -> Decimal:
        return Decimal("0.00")


class CreditCardPaymentStrategy(PaymentStrategy):
    """Pago con tarjeta de crédito"""

    def validate(self, payment_data: dict) -> bool:
        required = ["card_number", "cvv", "expiry"]
        return all(field in payment_data for field in required)

    def process(self, amount: Decimal) -> dict:
        return {
            "status": "pending",
            "method": "credit_card",
            "amount": str(amount),
            "timestamp": datetime.now().isoformat(),
            "reference": f"CC_{datetime.now().timestamp()}"
        }

    def get_fee(self, amount: Decimal) -> Decimal:
        return amount * Decimal("0.025")


class DebitCardPaymentStrategy(PaymentStrategy):
    """Pago con tarjeta de débito"""

    def validate(self, payment_data: dict) -> bool:
        required = ["card_number", "cvv", "expiry"]
        return all(field in payment_data for field in required)

    def process(self, amount: Decimal) -> dict:
        return {
            "status": "completed",
            "method": "debit_card",
            "amount": str(amount),
            "timestamp": datetime.now().isoformat(),
            "reference": f"DC_{datetime.now().timestamp()}"
        }

    def get_fee(self, amount: Decimal) -> Decimal:
        return amount * Decimal("0.015")


class TransferPaymentStrategy(PaymentStrategy):
    """Pago por transferencia bancaria"""

    def validate(self, payment_data: dict) -> bool:
        required = ["account_number", "bank_code"]
        return all(field in payment_data for field in required)

    def process(self, amount: Decimal) -> dict:
        return {
            "status": "pending",
            "method": "transfer",
            "amount": str(amount),
            "timestamp": datetime.now().isoformat(),
            "reference": f"TRF_{datetime.now().timestamp()}"
        }

    def get_fee(self, amount: Decimal) -> Decimal:
        return Decimal("50.00")


class CheckPaymentStrategy(PaymentStrategy):
    """Pago con cheque"""

    def validate(self, payment_data: dict) -> bool:
        required = ["check_number", "bank"]
        return all(field in payment_data for field in required)

    def process(self, amount: Decimal) -> dict:
        return {
            "status": "pending",
            "method": "check",
            "amount": str(amount),
            "timestamp": datetime.now().isoformat(),
            "reference": f"CHK_{datetime.now().timestamp()}"
        }

    def get_fee(self, amount: Decimal) -> Decimal:
        return Decimal("25.00")


# Factory para obtener estrategia por método
class PaymentStrategyFactory:
    """Factory para crear estrategias de pago"""

    _strategies = {
        "efectivo": CashPaymentStrategy(),
        "tarjeta_credito": CreditCardPaymentStrategy(),
        "tarjeta_debito": DebitCardPaymentStrategy(),
        "transferencia": TransferPaymentStrategy(),
        "cheque": CheckPaymentStrategy()
    }

    @classmethod
    def get_strategy(cls, method: str) -> PaymentStrategy:
        """Obtiene estrategia de pago por método"""
        strategy = cls._strategies.get(method.lower())
        if strategy is None:
            raise ValueError(f"Método de pago no soportado: {method}")
        return strategy

    @classmethod
    def get_available_methods(cls) -> list[str]:
        """Retorna lista de métodos disponibles"""
        return list(cls._strategies.keys())
