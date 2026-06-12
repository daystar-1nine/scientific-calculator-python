import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestEquationSolvers(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def test_root_finder_quadratic(self):
        self.app.solver_controller.solver_type.set("Root Finder")
        self.app.solver_controller.on_type_change()

        # Solve x^2 - 9 = 0 starting at guess 1.0 => root = 3.0
        self.app.solver_controller.param_entries["expr"].delete(0, tk.END)
        self.app.solver_controller.param_entries["expr"].insert(0, "x^2 - 9")
        self.app.solver_controller.param_entries["guess"].delete(0, tk.END)
        self.app.solver_controller.param_entries["guess"].insert(0, "1.0")

        self.app.solver_controller.solve()
        res = self.app.solver_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("3", res)

    def test_linear_systems_2x2(self):
        self.app.solver_controller.solver_type.set("Linear Systems")
        self.app.solver_controller.on_type_change()
        self.app.solver_controller.sub_type.set("2 Variables")
        self.app.solver_controller.on_linear_size_change()

        # System:
        # 2x + y = 5
        # x - y = 1
        # Solution: x = 2, y = 1
        grid = self.app.solver_controller.param_entries["grid"]
        
        # Row 1
        grid[0][0].delete(0, tk.END); grid[0][0].insert(0, "2")
        grid[0][1].delete(0, tk.END); grid[0][1].insert(0, "1")
        grid[0][2].delete(0, tk.END); grid[0][2].insert(0, "5")
        
        # Row 2
        grid[1][0].delete(0, tk.END); grid[1][0].insert(0, "1")
        grid[1][1].delete(0, tk.END); grid[1][1].insert(0, "-1")
        grid[1][2].delete(0, tk.END); grid[1][2].insert(0, "1")

        self.app.solver_controller.solve()
        res = self.app.solver_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("x = 2", res)
        self.assertIn("y = 1", res)

    def test_polynomial_quadratic_complex(self):
        self.app.solver_controller.solver_type.set("Polynomials")
        self.app.solver_controller.on_type_change()
        self.app.solver_controller.sub_type.set("Quadratic (2nd)")
        self.app.solver_controller.on_poly_degree_change()

        # Solve x^2 + 9 = 0 => roots = 3i, -3i
        poly = self.app.solver_controller.param_entries["poly"]
        poly["a"].delete(0, tk.END); poly["a"].insert(0, "1")
        poly["b"].delete(0, tk.END); poly["b"].insert(0, "0")
        poly["c"].delete(0, tk.END); poly["c"].insert(0, "9")

        self.app.solver_controller.solve()
        res = self.app.solver_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("3i", res)
        self.assertIn("-3i", res)

    def test_polynomial_cubic(self):
        self.app.solver_controller.solver_type.set("Polynomials")
        self.app.solver_controller.on_type_change()
        self.app.solver_controller.sub_type.set("Cubic (3rd)")
        self.app.solver_controller.on_poly_degree_change()

        # Solve x^3 - 6x^2 + 11x - 6 = 0 => roots = 1, 2, 3
        poly = self.app.solver_controller.param_entries["poly"]
        poly["a"].delete(0, tk.END); poly["a"].insert(0, "1")
        poly["b"].delete(0, tk.END); poly["b"].insert(0, "-6")
        poly["c"].delete(0, tk.END); poly["c"].insert(0, "11")
        poly["d"].delete(0, tk.END); poly["d"].insert(0, "-6")

        self.app.solver_controller.solve()
        res = self.app.solver_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("1", res)
        self.assertIn("2", res)
        self.assertIn("3", res)


if __name__ == "__main__":
    unittest.main()
