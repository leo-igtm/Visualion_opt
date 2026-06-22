import unittest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from datetime import timedelta

# Import patterns to test
from Backend.patterns.singleton import Singleton
from Backend.patterns.strategy import CashPaymentStrategy, CreditCardPaymentStrategy, TransferPaymentStrategy
from Backend.patterns.observer import EventSubject, Event, Observer
from Backend.patterns.composite import OrdenCompuesta, EtapaOtrabajo
from Backend.constants import AuthConstants

class TestSingleton(unittest.TestCase):
    def test_singleton_instance(self):
        class MySingleton(Singleton):
            pass
        
        inst1 = MySingleton()
        inst2 = MySingleton()
        
        self.assertIs(inst1, inst2, "Singleton instances should be the exact same object")

class TestStrategy(unittest.TestCase):
    def test_cash_strategy(self):
        strategy = CashPaymentStrategy()
        amount = Decimal("100.00")
        
        self.assertTrue(strategy.validate({}))
        self.assertEqual(strategy.get_fee(amount), Decimal("0.00"))
        
        result = strategy.process(amount)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["method"], "cash")

    def test_credit_card_strategy(self):
        strategy = CreditCardPaymentStrategy()
        amount = Decimal("100.00")
        
        self.assertFalse(strategy.validate({}))
        self.assertTrue(strategy.validate({"card_number": "123", "cvv": "123", "expiry": "12/25"}))
        
        fee = strategy.get_fee(amount)
        self.assertEqual(fee, Decimal("2.50")) # 2.5% of 100
        
        result = strategy.process(amount)
        self.assertEqual(result["status"], "pending")

class TestObserver(unittest.TestCase):
    def test_observer_notification(self):
        class MockObserver(Observer):
            def __init__(self):
                self.notified = False
                self.last_event = None
                
            def update(self, event):
                self.notified = True
                self.last_event = event

        subject = EventSubject()
        observer = MockObserver()
        subject.attach(observer)
        
        event = Event("test_event", {"key": "value"})
        subject.notify(event)
        
        self.assertTrue(observer.notified)
        self.assertEqual(observer.last_event.event_type, "test_event")

class TestComposite(unittest.TestCase):
    def test_composite_duration_and_cost(self):
        orden = OrdenCompuesta("ORD-001")
        etapa1 = EtapaOtrabajo("Biselado", 2.0, 150.0)
        etapa2 = EtapaOtrabajo("Montaje", 1.5, 100.0)
        
        orden.agregar_etapa(etapa1)
        orden.agregar_etapa(etapa2)
        
        self.assertEqual(orden.obtener_costo(), 250.0)
        self.assertEqual(orden.obtener_duracion_estimada(), timedelta(hours=3.5))

class TestConstants(unittest.TestCase):
    def test_auth_constants(self):
        self.assertEqual(AuthConstants.JWT_ALGORITHM, "HS256")
        self.assertTrue(AuthConstants.PASSWORD_MIN_LENGTH >= 8)

if __name__ == "__main__":
    unittest.main()
