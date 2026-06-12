import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestFormulaSolver(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def set_val(self, entry, val):
        entry.delete(0, tk.END)
        entry.insert(0, str(val))

    def test_solve_preset_ohms_law(self):
        # Preset Ohm's Law: V = I * R
        self.app.formula_controller.formula_preset.set("Ohm's Law")
        self.app.formula_controller.on_preset_change()

        # Solve for V, set I = 2, R = 10 => V = 20
        self.app.formula_controller.target_var.set("V")
        self.app.formula_controller.on_target_var_change("V")
        self.set_val(self.app.formula_controller.var_entries["I"], 2)
        self.set_val(self.app.formula_controller.var_entries["R"], 10)

        self.app.formula_controller.solve()
        res = self.app.formula_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("V = 20", res)

    def test_solve_preset_kinetic_energy(self):
        # Preset Kinetic Energy: KE = 0.5 * m * v^2
        self.app.formula_controller.formula_preset.set("Kinetic Energy")
        self.app.formula_controller.on_preset_change()

        # Solve for v, set KE = 10, m = 5 => v = 2
        self.app.formula_controller.target_var.set("v")
        self.app.formula_controller.on_target_var_change("v")
        self.set_val(self.app.formula_controller.var_entries["KE"], 10)
        self.set_val(self.app.formula_controller.var_entries["m"], 5)

        self.app.formula_controller.solve()
        res = self.app.formula_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("v = 2", res)

    def test_solve_custom_formula(self):
        # Custom Formula: F = m * a
        self.app.formula_controller.formula_preset.set("Custom Formula")
        self.app.formula_controller.on_preset_change()
        
        self.app.formula_controller.eq_entry.delete(0, tk.END)
        self.app.formula_controller.eq_entry.insert(0, "F = m * a")
        self.app.formula_controller.rebuild_variables_ui()

        # Solve for a, set F = 25, m = 5 => a = 5
        self.app.formula_controller.target_var.set("a")
        self.app.formula_controller.on_target_var_change("a")
        self.set_val(self.app.formula_controller.var_entries["F"], 25)
        self.set_val(self.app.formula_controller.var_entries["m"], 5)

        self.app.formula_controller.solve()
        res = self.app.formula_controller.result_text.get("1.0", tk.END).strip()
        self.assertIn("a = 5", res)


if __name__ == "__main__":
    unittest.main()
