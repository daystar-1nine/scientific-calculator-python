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


if __name__ == "__main__":
    unittest.main()
