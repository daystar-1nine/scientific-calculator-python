import unittest
import math
from core.evaluator import Evaluator
from utils.error_handler import InvalidExpressionError, MathOperationError


class TestCalculusEngine(unittest.TestCase):

    def setUp(self):
        self.evaluator = Evaluator()

    def test_differentiation_polynomial(self):
        # f(x) = x^2, f'(3) = 6
        res = self.evaluator.evaluate("diff(x^2, 3)")
        self.assertAlmostEqual(res, 6.0, places=4)

        # f(x) = x^3 - 2*x, f'(2) = 3(2)^2 - 2 = 10
        res = self.evaluator.evaluate("diff(x^3 - 2*x, 2)")
        self.assertAlmostEqual(res, 10.0, places=4)

    def test_differentiation_trig(self):
        # f(x) = sin(x), f'(0) = cos(0) = 1 in RAD mode
        res = self.evaluator.evaluate("diff(sin(x), 0)", mode="RAD")
        self.assertAlmostEqual(res, 1.0, places=4)

        # f(x) = cos(x), f'(pi) = -sin(pi) = 0 in RAD mode
        res = self.evaluator.evaluate("diff(cos(x), pi)", mode="RAD")
        self.assertAlmostEqual(res, 0.0, places=4)

    def test_integration_polynomial(self):
        # \int_{0}^{3} x^2 dx = [x^3/3]_0^3 = 9
        res = self.evaluator.evaluate("integrate(x^2, 0, 3)")
        self.assertAlmostEqual(res, 9.0, places=4)

        # \int_{1}^{2} (3*x^2 + 2*x) dx = [x^3 + x^2]_1^2 = (8+4) - (1+1) = 10
        res = self.evaluator.evaluate("integrate(3*x^2 + 2*x, 1, 2)")
        self.assertAlmostEqual(res, 10.0, places=4)

    def test_integration_trig(self):
        # \int_{0}^{pi} sin(x) dx = [-cos(x)]_0^pi = -(-1) - (-1) = 2 in RAD mode
        res = self.evaluator.evaluate("integrate(sin(x), 0, pi)", mode="RAD")
        self.assertAlmostEqual(res, 2.0, places=4)

    def test_invalid_argument_counts(self):
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("diff(x^2)")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("diff(x^2, 1, 2)")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("integrate(x^2, 0)")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("integrate(x^2, 0, 1, 2)")

    def test_complex_checks(self):
        # Diff point must be real
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("diff(x^2, 2 + 3i)")
        # Integration bounds must be real
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("integrate(x^2, 0, 1 + i)")


if __name__ == "__main__":
    unittest.main()
