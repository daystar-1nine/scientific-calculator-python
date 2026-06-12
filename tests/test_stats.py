import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestStatisticsSuite(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def test_descriptive_statistics(self):
        self.app.stats_controller.stats_type.set("Descriptive Stats")
        self.app.stats_controller.on_type_change()

        # Input: 2, 4, 4, 4, 5, 5, 7, 9 => count = 8, mean = 40/8 = 5.0, median = 4.5
        self.app.stats_controller.param_entries["values"].delete(0, tk.END)
        self.app.stats_controller.param_entries["values"].insert(0, "2, 4, 4, 4, 5, 5, 7, 9")

        self.app.stats_controller.calculate()
        res = self.app.stats_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("Count (n):    8", res)
        self.assertIn("Mean (x̄):     5", res)
        self.assertIn("Median:       4.5", res)

    def test_linear_regression(self):
        self.app.stats_controller.stats_type.set("Linear Regression")
        self.app.stats_controller.on_type_change()

        # Input X: 1, 2, 3, 4, 5; Y: 2, 4, 5, 4, 5
        self.app.stats_controller.param_entries["x_vals"].delete(0, tk.END)
        self.app.stats_controller.param_entries["x_vals"].insert(0, "1, 2, 3, 4, 5")
        self.app.stats_controller.param_entries["y_vals"].delete(0, tk.END)
        self.app.stats_controller.param_entries["y_vals"].insert(0, "2, 4, 5, 4, 5")

        self.app.stats_controller.calculate()
        res = self.app.stats_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("Slope (m):      0.6", res)
        self.assertIn("Intercept (c):  2.2", res)
        self.assertIn("y = 0.6*x + 2.2", res)

    def test_probability_helpers(self):
        self.app.stats_controller.stats_type.set("Probability Helpers")
        self.app.stats_controller.on_type_change()

        # 1. Combos: 5 C 2 = 10
        self.app.stats_controller.prob_op.set("nCr")
        self.app.stats_controller.on_prob_op_change()
        self.app.stats_controller.param_entries["prob"]["n"].delete(0, tk.END)
        self.app.stats_controller.param_entries["prob"]["n"].insert(0, "5")
        self.app.stats_controller.param_entries["prob"]["r"].delete(0, tk.END)
        self.app.stats_controller.param_entries["prob"]["r"].insert(0, "2")
        self.app.stats_controller.calculate()
        res = self.app.stats_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("10", res)

        # 2. Permutations: 5 P 2 = 20
        self.app.stats_controller.prob_op.set("nPr")
        self.app.stats_controller.on_prob_op_change()
        self.app.stats_controller.param_entries["prob"]["n"].delete(0, tk.END)
        self.app.stats_controller.param_entries["prob"]["n"].insert(0, "5")
        self.app.stats_controller.param_entries["prob"]["r"].delete(0, tk.END)
        self.app.stats_controller.param_entries["prob"]["r"].insert(0, "2")
        self.app.stats_controller.calculate()
        res = self.app.stats_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("20", res)

        # 3. Normal CDF: z = 0 => CDF = 0.5
        self.app.stats_controller.prob_op.set("Normal CDF (z)")
        self.app.stats_controller.on_prob_op_change()
        self.app.stats_controller.param_entries["prob"]["z"].delete(0, tk.END)
        self.app.stats_controller.param_entries["prob"]["z"].insert(0, "0")
        self.app.stats_controller.calculate()
        res = self.app.stats_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("0.5", res)


if __name__ == "__main__":
    unittest.main()
