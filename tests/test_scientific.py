import unittest
import math
from core.evaluator import Evaluator
from utils.error_handler import MathOperationError, InvalidExpressionError


class TestScientificFunctions(unittest.TestCase):

    def setUp(self):
        self.evaluator = Evaluator()

    def test_constants(self):
        self.assertAlmostEqual(self.evaluator.evaluate("PI"), math.pi)
        self.assertAlmostEqual(self.evaluator.evaluate("E"), math.e)

    def test_trig_functions_rad(self):
        self.assertAlmostEqual(self.evaluator.evaluate("sin(0)", mode="RAD"), 0.0)
        self.assertAlmostEqual(self.evaluator.evaluate("sin(PI / 2)", mode="RAD"), 1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("cos(0)", mode="RAD"), 1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("cos(PI)", mode="RAD"), -1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("tan(0)", mode="RAD"), 0.0)
        
        # Test tangent domain error in RAD mode (cos(x) approx 0)
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("tan(PI / 2)", mode="RAD")

    def test_trig_functions_deg(self):
        self.assertAlmostEqual(self.evaluator.evaluate("sin(90)", mode="DEG"), 1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("sin(180)", mode="DEG"), 0.0)
        self.assertAlmostEqual(self.evaluator.evaluate("cos(0)", mode="DEG"), 1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("cos(180)", mode="DEG"), -1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("tan(45)", mode="DEG"), 1.0)
        
        # Test tangent domain error in DEG mode
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("tan(90)", mode="DEG")
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("tan(270)", mode="DEG")

    def test_log_functions(self):
        self.assertAlmostEqual(self.evaluator.evaluate("log(10)"), 1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("log(100)"), 2.0)
        self.assertAlmostEqual(self.evaluator.evaluate("ln(E)"), 1.0)
        
        # Domain errors
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("log(0)")
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("log(-5)")
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("ln(-1)")

    def test_sqrt(self):
        self.assertAlmostEqual(self.evaluator.evaluate("sqrt(4)"), 2.0)
        self.assertAlmostEqual(self.evaluator.evaluate("sqrt(0)"), 0.0)
        self.assertAlmostEqual(self.evaluator.evaluate("sqrt(2)"), math.sqrt(2))
        
        # Domain error
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("sqrt(-4)")

    def test_factorial(self):
        self.assertEqual(self.evaluator.evaluate("factorial(0)"), 1)
        self.assertEqual(self.evaluator.evaluate("factorial(5)"), 120)
        self.assertEqual(self.evaluator.evaluate("factorial(5.0)"), 120)
        
        # Domain errors
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("factorial(-1)")
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("factorial(5.5)")

    def test_nested_scientific(self):
        self.assertAlmostEqual(self.evaluator.evaluate("sqrt(sin(PI / 2) + 3)"), 2.0)
        self.assertEqual(self.evaluator.evaluate("factorial(sqrt(9))"), 6)

    def test_unknown_function(self):
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("invalidfunc(5)")

    def test_inverse_trig(self):
        self.assertAlmostEqual(self.evaluator.evaluate("asin(1)", mode="RAD"), math.pi / 2)
        self.assertAlmostEqual(self.evaluator.evaluate("asin(1)", mode="DEG"), 90.0)
        self.assertAlmostEqual(self.evaluator.evaluate("acos(0)", mode="RAD"), math.pi / 2)
        self.assertAlmostEqual(self.evaluator.evaluate("acos(0)", mode="DEG"), 90.0)
        self.assertAlmostEqual(self.evaluator.evaluate("atan(1)", mode="RAD"), math.pi / 4)
        self.assertAlmostEqual(self.evaluator.evaluate("atan(1)", mode="DEG"), 45.0)

        # Domain errors
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("asin(2)")
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("acos(-1.5)")

    def test_hyperbolic_functions(self):
        self.assertAlmostEqual(self.evaluator.evaluate("sinh(0)"), 0.0)
        self.assertAlmostEqual(self.evaluator.evaluate("cosh(0)"), 1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("tanh(0)"), 0.0)
        
        # Test large input error (overflow)
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("sinh(1000)")
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("cosh(1000)")

    def test_exp_function(self):
        self.assertAlmostEqual(self.evaluator.evaluate("exp(0)"), 1.0)
        self.assertAlmostEqual(self.evaluator.evaluate("exp(1)"), math.e)
        
        # Test overflow
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("exp(1000)")

    def test_safe_pow_limits_and_factorial_limits(self):
        # Exponent too large
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("2 ^ 10000000")
        # Log value too large (9^9^9 is 9^387420489)
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("9 ^ 9 ^ 9")
        
        # Factorial too large (max 1000)
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("factorial(1001)")
        # Complex result not supported
        with self.assertRaises(MathOperationError):
            self.evaluator.evaluate("(-4) ^ 0.5")


if __name__ == "__main__":
    unittest.main()
