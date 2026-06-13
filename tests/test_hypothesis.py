import unittest
import tkinter as tk
from gui.app import CalculatorApp
from gui.hypothesis_testing_controller import (
    HypothesisTestingController,
    std_normal_cdf,
    std_normal_ppf,
    student_t_cdf,
    student_t_ppf,
    chi_square_cdf,
    chi_square_ppf
)

class TestHypothesisSuite(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()
        self.frame = tk.Frame(self.app.root)
        self.controller = HypothesisTestingController(self.app, self.frame)

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def test_distribution_helpers(self):
        # test std_normal_cdf/ppf
        self.assertAlmostEqual(std_normal_cdf(0.0), 0.5, places=5)
        self.assertAlmostEqual(std_normal_cdf(1.96), 0.975002, places=4)
        self.assertAlmostEqual(std_normal_ppf(0.5), 0.0, places=5)
        self.assertAlmostEqual(std_normal_ppf(0.975), 1.96, places=2)

        # test student_t_cdf/ppf
        self.assertAlmostEqual(student_t_cdf(0.0, 10), 0.5, places=5)
        self.assertAlmostEqual(student_t_ppf(0.975, 24), 2.06389, delta=0.01)

        # test chi_square_cdf/ppf
        self.assertAlmostEqual(chi_square_cdf(5.991, 2), 0.95, places=2)
        self.assertAlmostEqual(chi_square_ppf(0.95, 2), 5.991, delta=0.06)

    def test_z_test_two_tailed(self):
        self.controller.test_type.set("1-Sample Z-Test")
        self.controller.tail_type.set("Two-Tailed (≠)")
        self.controller.alpha_entry.delete(0, tk.END)
        self.controller.alpha_entry.insert(0, "0.05")

        self.controller.on_test_change()
        self.controller.param_entries["mean"].delete(0, tk.END)
        self.controller.param_entries["mean"].insert(0, "5.2")
        self.controller.param_entries["stddev"].delete(0, tk.END)
        self.controller.param_entries["stddev"].insert(0, "0.5")
        self.controller.param_entries["size"].delete(0, tk.END)
        self.controller.param_entries["size"].insert(0, "25")
        self.controller.param_entries["null"].delete(0, tk.END)
        self.controller.param_entries["null"].insert(0, "5.0")

        self.controller.run_test()
        res = self.controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("1-Sample Z-Test Report", res)
        self.assertIn("Test Statistic z = 2", res)
        self.assertIn("p-value          = 0.0455", res)
        self.assertIn("REJECT Null Hypothesis (H0)", res)

    def test_t_test_greater(self):
        self.controller.test_type.set("1-Sample T-Test")
        self.controller.tail_type.set("Greater Than (>)")
        self.controller.alpha_entry.delete(0, tk.END)
        self.controller.alpha_entry.insert(0, "0.05")

        self.controller.on_test_change()
        self.controller.param_entries["mean"].delete(0, tk.END)
        self.controller.param_entries["mean"].insert(0, "5.2")
        self.controller.param_entries["stddev"].delete(0, tk.END)
        self.controller.param_entries["stddev"].insert(0, "0.5")
        self.controller.param_entries["size"].delete(0, tk.END)
        self.controller.param_entries["size"].insert(0, "25")
        self.controller.param_entries["null"].delete(0, tk.END)
        self.controller.param_entries["null"].insert(0, "5.0")

        self.controller.run_test()
        res = self.controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("1-Sample T-Test Report", res)
        self.assertIn("Test Statistic t = 2", res)
        self.assertIn("REJECT Null Hypothesis (H0)", res)

    def test_two_sample_t_test(self):
        self.controller.test_type.set("2-Sample T-Test")
        self.controller.tail_type.set("Two-Tailed (≠)")
        self.controller.alpha_entry.delete(0, tk.END)
        self.controller.alpha_entry.insert(0, "0.05")

        self.controller.on_test_change()
        self.controller.param_entries["mean1"].delete(0, tk.END)
        self.controller.param_entries["mean1"].insert(0, "12.1")
        self.controller.param_entries["sd1"].delete(0, tk.END)
        self.controller.param_entries["sd1"].insert(0, "1.2")
        self.controller.param_entries["n1"].delete(0, tk.END)
        self.controller.param_entries["n1"].insert(0, "20")

        self.controller.param_entries["mean2"].delete(0, tk.END)
        self.controller.param_entries["mean2"].insert(0, "11.5")
        self.controller.param_entries["sd2"].delete(0, tk.END)
        self.controller.param_entries["sd2"].insert(0, "1.5")
        self.controller.param_entries["n2"].delete(0, tk.END)
        self.controller.param_entries["n2"].insert(0, "22")

        self.controller.run_test()
        res = self.controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("2-Sample T-Test", res)
        self.assertIn("FAIL TO REJECT", res)

    def test_chi_square_test(self):
        self.controller.test_type.set("Chi-Square Test")
        self.controller.alpha_entry.delete(0, tk.END)
        self.controller.alpha_entry.insert(0, "0.05")

        self.controller.on_test_change()
        self.controller.param_entries["obs"].delete(0, tk.END)
        self.controller.param_entries["obs"].insert(0, "10, 20, 30")
        self.controller.param_entries["exp"].delete(0, tk.END)
        self.controller.param_entries["exp"].insert(0, "15, 15, 30")

        self.controller.run_test()
        res = self.controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("Chi-Square Goodness-of-Fit Test", res)
        self.assertIn("Chi-Square χ²    = 3.33333", res)
        self.assertIn("FAIL TO REJECT", res)

if __name__ == "__main__":
    unittest.main()
