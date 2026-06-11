import unittest
from core.evaluator import Evaluator
from utils.error_handler import InvalidExpressionError, DivisionByZeroError, MathOperationError


class TestEvaluatorBasic(unittest.TestCase):

    def setUp(self):
        self.evaluator = Evaluator()

    def test_basic_addition(self):
        self.assertEqual(self.evaluator.evaluate("2 + 3"), 5)
        self.assertEqual(self.evaluator.evaluate("2.5 + 3.1"), 5.6)

    def test_basic_subtraction(self):
        self.assertEqual(self.evaluator.evaluate("5 - 3"), 2)
        self.assertEqual(self.evaluator.evaluate("3 - 5"), -2)

    def test_basic_multiplication(self):
        self.assertEqual(self.evaluator.evaluate("4 * 5"), 20)
        self.assertEqual(self.evaluator.evaluate("2.5 * 2"), 5.0)

    def test_basic_division(self):
        self.assertEqual(self.evaluator.evaluate("10 / 2"), 5.0)
        self.assertEqual(self.evaluator.evaluate("5 / 2"), 2.5)

    def test_basic_exponentiation(self):
        self.assertEqual(self.evaluator.evaluate("2 ^ 3"), 8)
        self.assertEqual(self.evaluator.evaluate("3 ^ 2"), 9)
        self.assertEqual(self.evaluator.evaluate("2 ** 3"), 8)

    def test_unary_operators(self):
        self.assertEqual(self.evaluator.evaluate("-5"), -5)
        self.assertEqual(self.evaluator.evaluate("+5"), 5)
        self.assertEqual(self.evaluator.evaluate("-(2 + 3)"), -5)

    def test_operator_precedence(self):
        self.assertEqual(self.evaluator.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(self.evaluator.evaluate("(2 + 3) * 4"), 20)
        self.assertEqual(self.evaluator.evaluate("2 * 3 ^ 2"), 18)
        self.assertEqual(self.evaluator.evaluate("(2 * 3) ^ 2"), 36)

    def test_division_by_zero(self):
        with self.assertRaises(DivisionByZeroError):
            self.evaluator.evaluate("5 / 0")
        with self.assertRaises(DivisionByZeroError):
            self.evaluator.evaluate("5 / (2 - 2)")

    def test_invalid_expressions(self):
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("2 + ")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("2 + (3")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("import os; os.system('ls')")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("True")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("")

    def test_variable_evaluation(self):
        self.assertEqual(self.evaluator.evaluate("x + 5", variables={"x": 10}), 15)
        self.assertAlmostEqual(self.evaluator.evaluate("sin(x)", variables={"x": 0}), 0.0)
        self.assertEqual(self.evaluator.evaluate("x * y", variables={"x": 3, "y": 4}), 12)


if __name__ == "__main__":
    unittest.main()
