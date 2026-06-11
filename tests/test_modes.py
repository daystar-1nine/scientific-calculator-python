import unittest
from core.modes import CalculatorMode


class TestCalculatorMode(unittest.TestCase):

    def setUp(self):
        self.mode_manager = CalculatorMode()

    def test_default_mode(self):
        self.assertEqual(self.mode_manager.get_mode(), CalculatorMode.DEGREE)

    def test_set_radian(self):
        self.mode_manager.set_radian()
        self.assertEqual(self.mode_manager.get_mode(), CalculatorMode.RADIAN)

    def test_set_degree(self):
        self.mode_manager.set_radian()
        self.mode_manager.set_degree()
        self.assertEqual(self.mode_manager.get_mode(), CalculatorMode.DEGREE)


if __name__ == "__main__":
    unittest.main()
