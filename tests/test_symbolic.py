import unittest
from core.symbolic import differentiate

class TestSymbolicCAS(unittest.TestCase):

    def test_polynomial_diff(self):
        # x^3 + 3*x^2 + 5 -> 3 * x^2 + 6 * x
        res = differentiate("x^3 + 3*x^2 + 5", "x")
        self.assertIn("3 * x^2 + 6 * x", res)

    def test_trig_diff(self):
        # sin(x) -> cos(x)
        self.assertEqual(differentiate("sin(x)", "x"), "cos(x)")
        # cos(x) -> -sin(x)
        self.assertEqual(differentiate("cos(x)", "x"), "-sin(x)")

    def test_product_rule(self):
        # x * sin(x) -> sin(x) + x * cos(x)
        res = differentiate("x * sin(x)", "x")
        self.assertEqual(res, "sin(x) + x * cos(x)")

    def test_ln_diff(self):
        # ln(x) -> 1 / x
        self.assertEqual(differentiate("ln(x)", "x"), "1 / x")

    def test_power_diff_constant_base(self):
        # 2^x -> 2^x * ln(2)
        res = differentiate("2^x", "x")
        self.assertEqual(res, "2^x * ln(2)")

    def test_different_variable(self):
        # y^2 with respect to y -> 2 * y
        self.assertEqual(differentiate("y^2", "y"), "2 * y")

if __name__ == "__main__":
    unittest.main()
