import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestComplexConverter(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def test_convert_to_polar_deg(self):
        controller = self.app.complex_converter_controller
        self.app.mode_manager.set_degree()

        controller.real_entry.delete(0, tk.END)
        controller.real_entry.insert(0, "3.0")
        controller.imag_entry.delete(0, tk.END)
        controller.imag_entry.insert(0, "4.0")

        controller.convert_to_polar()
        res = controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("5", res)
        self.assertIn("53.13", res)
        self.assertIn("Rectangular: 3.0 + 4.0i", res)

    def test_convert_to_rectangular_deg(self):
        controller = self.app.complex_converter_controller
        self.app.mode_manager.set_degree()

        controller.mag_entry.delete(0, tk.END)
        controller.mag_entry.insert(0, "5.0")
        controller.ang_entry.delete(0, tk.END)
        controller.ang_entry.insert(0, "53.1301")

        controller.convert_to_rectangular()
        res = controller.result_text.get("1.0", tk.END).strip()
        # Should be approximately 3 + 4i
        self.assertIn("3", res)
        self.assertIn("4", res)

    def test_convert_to_polar_rad(self):
        controller = self.app.complex_converter_controller
        self.app.mode_manager.set_radian()

        controller.real_entry.delete(0, tk.END)
        controller.real_entry.insert(0, "1.0")
        controller.imag_entry.delete(0, tk.END)
        controller.imag_entry.insert(0, "1.0")

        controller.convert_to_polar()
        res = controller.result_text.get("1.0", tk.END).strip()
        # sqrt(2) is ~1.414, angle is pi/4 ~0.785
        self.assertIn("1.414", res)
        self.assertIn("0.785", res)


if __name__ == "__main__":
    unittest.main()
