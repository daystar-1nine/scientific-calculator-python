import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestVectorMath(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def set_val(self, entry, val):
        entry.delete(0, tk.END)
        entry.insert(0, str(val))

    def test_vector_magnitudes_3d(self):
        self.app.vector_controller.vector_dim.set("3D Vector")
        self.app.vector_controller.update_dimension()

        # Vector A = [3, 4, 12] => |A| = 13
        self.set_val(self.app.vector_controller.entries_a["x"], 3)
        self.set_val(self.app.vector_controller.entries_a["y"], 4)
        self.set_val(self.app.vector_controller.entries_a["z"], 12)

        self.app.vector_controller.run_magnitude()
        res = self.app.vector_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("|A| = 13", res)

    def test_vector_dot_product_2d(self):
        self.app.vector_controller.vector_dim.set("2D Vector")
        self.app.vector_controller.update_dimension()

        # A = [2, 3], B = [4, -5] => A . B = 8 - 15 = -7
        self.set_val(self.app.vector_controller.entries_a["x"], 2)
        self.set_val(self.app.vector_controller.entries_a["y"], 3)
        self.set_val(self.app.vector_controller.entries_b["x"], 4)
        self.set_val(self.app.vector_controller.entries_b["y"], -5)

        self.app.vector_controller.run_dot()
        res = self.app.vector_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("-7", res)

    def test_vector_cross_product(self):
        self.app.vector_controller.vector_dim.set("3D Vector")
        self.app.vector_controller.update_dimension()

        # A = [1, 0, 0], B = [0, 1, 0] => A x B = [0, 0, 1]
        self.set_val(self.app.vector_controller.entries_a["x"], 1)
        self.set_val(self.app.vector_controller.entries_a["y"], 0)
        self.set_val(self.app.vector_controller.entries_a["z"], 0)
        self.set_val(self.app.vector_controller.entries_b["x"], 0)
        self.set_val(self.app.vector_controller.entries_b["y"], 1)
        self.set_val(self.app.vector_controller.entries_b["z"], 0)

        self.app.vector_controller.run_cross()
        res = self.app.vector_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("[ 0, 0, 1 ]", res)

    def test_vector_angle_degree(self):
        self.app.vector_controller.vector_dim.set("2D Vector")
        self.app.vector_controller.update_dimension()

        # A = [1, 0], B = [0, 1] => Angle = 90 degrees
        self.set_val(self.app.vector_controller.entries_a["x"], 1)
        self.set_val(self.app.vector_controller.entries_a["y"], 0)
        self.set_val(self.app.vector_controller.entries_b["x"], 0)
        self.set_val(self.app.vector_controller.entries_b["y"], 1)

        # Force Degree Mode
        self.app.mode_manager.set_degree()

        self.app.vector_controller.run_angle()
        res = self.app.vector_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("90°", res)


if __name__ == "__main__":
    unittest.main()
