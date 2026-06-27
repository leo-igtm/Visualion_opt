import unittest
from decimal import Decimal

# Import patterns to test
from Backend.patterns.singleton import Singleton
from Backend.patterns.strategy import CashPaymentStrategy, CreditCardPaymentStrategy, PaymentStrategyFactory

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

    def test_payment_strategy_factory(self):
        strategy = PaymentStrategyFactory.get_strategy(" EFECTIVO ")
        self.assertIsInstance(strategy, CashPaymentStrategy)
        self.assertIn("pendiente", PaymentStrategyFactory.get_available_payment_states())

        with self.assertRaises(ValueError):
            PaymentStrategyFactory.get_strategy("")


class TestConstants(unittest.TestCase):
    def test_auth_constants(self):
        self.assertEqual(AuthConstants.JWT_ALGORITHM, "HS256")
        self.assertTrue(AuthConstants.PASSWORD_MIN_LENGTH >= 8)

if __name__ == "__main__":
    unittest.main()
