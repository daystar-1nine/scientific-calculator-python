import unittest
from core.parser import Parser
from utils.error_handler import InvalidExpressionError


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_basic_normalization(self):
        self.assertEqual(self.parser.parse("  2 + 3  "), "2 + 3")
        self.assertEqual(self.parser.parse("2 ^ 3"), "2 ** 3")
        self.assertEqual(self.parser.parse("SIN(pi)"), "sin(PI)")
        self.assertEqual(self.parser.parse("CoS(E)"), "cos(E)")
        self.assertEqual(self.parser.parse("LOG(10) + LN(e)"), "log(10) + ln(E)")

    def test_implicit_multiplication_parentheses(self):
        self.assertEqual(self.parser.parse("2(3)"), "2*(3)")
        self.assertEqual(self.parser.parse("2.5(3 + 4)"), "2.5*(3 + 4)")
        self.assertEqual(self.parser.parse("(3)2"), "(3)*2")
        self.assertEqual(self.parser.parse("(3)2.5"), "(3)*2.5")
        self.assertEqual(self.parser.parse("(2)(3)"), "(2)*(3)")

    def test_implicit_multiplication_constants_and_functions(self):
        self.assertEqual(self.parser.parse("2pi"), "2*PI")
        self.assertEqual(self.parser.parse("2PI"), "2*PI")
        self.assertEqual(self.parser.parse("2.5e"), "2.5*E")
        self.assertEqual(self.parser.parse("2sin(3)"), "2*sin(3)")
        self.assertEqual(self.parser.parse("(2)sin(3)"), "(2)*sin(3)")
        self.assertEqual(self.parser.parse("(2)PI"), "(2)*PI")
        self.assertEqual(self.parser.parse("PI(3)"), "PI*(3)")
        self.assertEqual(self.parser.parse("PI E"), "PI*E")
        self.assertEqual(self.parser.parse("PI sin(3)"), "PI*sin(3)")

    def test_factorial_parsing(self):
        self.assertEqual(self.parser.parse("5!"), "factorial(5)")
        self.assertEqual(self.parser.parse("5.0!"), "factorial(5.0)")
        self.assertEqual(self.parser.parse("PI!"), "factorial(PI)")
        self.assertEqual(self.parser.parse("(2+3)!"), "factorial((2+3))")
        self.assertEqual(self.parser.parse("sin(PI)!"), "factorial(sin(PI))")
        self.assertEqual(self.parser.parse("5!!"), "factorial(factorial(5))")

    def test_factorial_errors(self):
        with self.assertRaises(InvalidExpressionError):
            self.parser.parse("!")
        with self.assertRaises(InvalidExpressionError):
            self.parser.parse("5+!")
        with self.assertRaises(InvalidExpressionError):
            self.parser.parse("2+3)!")


if __name__ == "__main__":
    unittest.main()
