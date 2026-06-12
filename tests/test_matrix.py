import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestMatrixAlgebra(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def set_val(self, entry, val):
        entry.delete(0, tk.END)
        entry.insert(0, str(val))

    def test_matrix_determinant_2x2(self):
        self.app.matrix_controller.matrix_size.set("2x2")
        self.app.matrix_controller.update_dimensions()

        # Input Matrix A = [[5, -2], [3, 4]] => Det = 20 - (-6) = 26
        self.set_val(self.app.matrix_controller.grid_a_entries[0][0], 5)
        self.set_val(self.app.matrix_controller.grid_a_entries[0][1], -2)
        self.set_val(self.app.matrix_controller.grid_a_entries[1][0], 3)
        self.set_val(self.app.matrix_controller.grid_a_entries[1][1], 4)

        self.app.matrix_controller.run_unary_op("det")
        res = self.app.matrix_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("26", res)

    def test_matrix_inverse_2x2(self):
        self.app.matrix_controller.matrix_size.set("2x2")
        self.app.matrix_controller.update_dimensions()

        # Input Matrix A = [[1, 2], [3, 4]] => Inv = [[-2, 1], [1.5, -0.5]]
        self.set_val(self.app.matrix_controller.grid_a_entries[0][0], 1)
        self.set_val(self.app.matrix_controller.grid_a_entries[0][1], 2)
        self.set_val(self.app.matrix_controller.grid_a_entries[1][0], 3)
        self.set_val(self.app.matrix_controller.grid_a_entries[1][1], 4)

        self.app.matrix_controller.run_unary_op("inv")
        res = self.app.matrix_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("-2", res)
        self.assertIn("1.5", res)
        self.assertIn("-0.5", res)

    def test_matrix_multiplication_3x3(self):
        self.app.matrix_controller.matrix_size.set("3x3")
        self.app.matrix_controller.update_dimensions()

        # Identity Matrix A * Identity Matrix B = Identity Matrix
        for i in range(3):
            for j in range(3):
                # Clear default '0' first
                self.set_val(self.app.matrix_controller.grid_a_entries[i][j], 1 if i == j else 0)
                self.set_val(self.app.matrix_controller.grid_b_entries[i][j], 1 if i == j else 0)

        self.app.matrix_controller.run_binary_op("mul")
        res = self.app.matrix_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("[ 1  0  0 ]", res)
        self.assertIn("[ 0  1  0 ]", res)
        self.assertIn("[ 0  0  1 ]", res)

    def test_singular_matrix_error(self):
        self.app.matrix_controller.matrix_size.set("2x2")
        self.app.matrix_controller.update_dimensions()

        # [[1, 2], [2, 4]] => det = 0
        self.set_val(self.app.matrix_controller.grid_a_entries[0][0], 1)
        self.set_val(self.app.matrix_controller.grid_a_entries[0][1], 2)
        self.set_val(self.app.matrix_controller.grid_a_entries[1][0], 2)
        self.set_val(self.app.matrix_controller.grid_a_entries[1][1], 4)

        self.app.matrix_controller.run_unary_op("inv")
        res = self.app.matrix_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("singular", res.lower())


if __name__ == "__main__":
    unittest.main()
