import unittest
from core.evaluator import Evaluator
from gui.app import CalculatorApp


class TestComplexNumbers(unittest.TestCase):

    def setUp(self):
        self.evaluator = Evaluator()

    def test_complex_parsing_and_evaluation(self):
        # Standalone imaginary unit i
        self.assertEqual(self.evaluator.evaluate("i"), 1j)
        
        # Coefficient with i
        self.assertEqual(self.evaluator.evaluate("3i"), 3j)
        self.assertEqual(self.evaluator.evaluate("2.5i"), 2.5j)
        
        # Addition and subtraction
        self.assertEqual(self.evaluator.evaluate("2 + 3i"), 2 + 3j)
        self.assertEqual(self.evaluator.evaluate("5 - i"), 5 - 1j)

    def test_complex_operations(self):
        # Multiplication: (2+3i) * (1-2i) = 2 - 4i + 3i - 6i^2 = 8 - i
        self.assertAlmostEqual(self.evaluator.evaluate("(2 + 3i) * (1 - 2i)"), 8 - 1j)
        
        # Division: (1+i) / (1-i) = i
        self.assertAlmostEqual(self.evaluator.evaluate("(1 + i) / (1 - i)"), 1j)

    def test_complex_power_roots(self):
        # Square root of negative number: (-9)^0.5 = 3i
        self.assertAlmostEqual(self.evaluator.evaluate("(-9) ^ 0.5"), 3j)
        
        # Euler's relation: e^(i * PI) = -1 (approximately)
        res = self.evaluator.evaluate("e ^ (i * PI)")
        self.assertAlmostEqual(res.real, -1.0)
        self.assertAlmostEqual(res.imag, 0.0, places=15)

    def test_complex_formatting(self):
        app = CalculatorApp()
        
        # Pure imaginary cases
        self.assertEqual(app.format_result(1j), "i")
        self.assertEqual(app.format_result(-1j), "-i")
        self.assertEqual(app.format_result(3.5j), "3.5i")
        
        # Pure real cases
        self.assertEqual(app.format_result(5.0 + 0j), "5")
        
        # Mixed complex cases
        self.assertEqual(app.format_result(2 + 3j), "2 + 3i")
        self.assertEqual(app.format_result(2 - 3j), "2 - 3i")
        self.assertEqual(app.format_result(2 - 1j), "2 - i")
        self.assertEqual(app.format_result(2 + 1j), "2 + i")
        
        app.root.update()
        app.root.destroy()


if __name__ == "__main__":
    unittest.main()
