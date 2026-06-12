import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestVariablesRegistry(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def test_user_variables_evaluation(self):
        # Assign A = 10, B = 2 + 3 => B = 5
        self.app.variables_controller.user_entries["A"].delete(0, tk.END)
        self.app.variables_controller.user_entries["A"].insert(0, "10")
        self.app.variables_controller.user_entries["B"].delete(0, tk.END)
        self.app.variables_controller.user_entries["B"].insert(0, "2 + 3")

        # Evaluate "A * B" in the main calculator => 10 * 5 = 50
        self.app.display.set_text("A * B")
        self.app.on_button_click("=")
        res = self.app.display.get_text()
        self.assertEqual(res, "50")

    def test_constants_lookup(self):
        # Evaluate "2 * c" (c = 299792458) => 599584916
        self.app.display.set_text("2 * c")
        self.app.on_button_click("=")
        res = self.app.display.get_text()
        self.assertEqual(res, "599584916")

    def test_insert_constant(self):
        self.app.display.set_text("")
        self.app.variables_controller.insert_constant("h")
        self.assertEqual(self.app.display.get_text(), "h")

    def test_custom_saved_function(self):
        # Define custom function f(x, y) = x^2 + y^2
        self.app.variables_controller.func_name_entry.delete(0, tk.END)
        self.app.variables_controller.func_name_entry.insert(0, "f(x, y)")
        self.app.variables_controller.func_body_entry.delete(0, tk.END)
        self.app.variables_controller.func_body_entry.insert(0, "x^2 + y^2")
        self.app.variables_controller.save_custom_function()

        # Evaluate "f(3, 4)" in main calculator => 3^2 + 4^2 = 25
        self.app.display.set_text("f(3, 4)")
        self.app.on_button_click("=")
        res = self.app.display.get_text()
        self.assertEqual(res, "25")

    def test_custom_saved_function_nested(self):
        # Define f(x) = x + 1, g(x) = x^2
        self.app.variables_controller.func_name_entry.delete(0, tk.END)
        self.app.variables_controller.func_name_entry.insert(0, "f(x)")
        self.app.variables_controller.func_body_entry.delete(0, tk.END)
        self.app.variables_controller.func_body_entry.insert(0, "x + 1")
        self.app.variables_controller.save_custom_function()

        self.app.variables_controller.func_name_entry.delete(0, tk.END)
        self.app.variables_controller.func_name_entry.insert(0, "g(x)")
        self.app.variables_controller.func_body_entry.delete(0, tk.END)
        self.app.variables_controller.func_body_entry.insert(0, "x^2")
        self.app.variables_controller.save_custom_function()

        # Evaluate "g(f(2))" => (2+1)^2 = 9
        self.app.display.set_text("g(f(2))")
        self.app.on_button_click("=")
        res = self.app.display.get_text()
        self.assertEqual(res, "9")


if __name__ == "__main__":
    unittest.main()
