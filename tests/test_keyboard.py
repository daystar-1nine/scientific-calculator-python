import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestKeyboardBindings(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()
        self.app.root.update()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def _simulate_key(self, keysym, char=""):
        event = tk.Event()
        event.keysym = keysym
        event.char = char
        # Call the key press handler directly to avoid OS-level window focus flakiness
        self.app.on_key_press(event)
        self.app.root.update()

    def test_keyboard_digits_and_operators(self):
        # Generate keys '5', '+', '3'
        self._simulate_key("5", "5")
        self._simulate_key("plus", "+")
        self._simulate_key("3", "3")
        
        self.assertEqual(self.app.display.get_text(), "5+3")

    def test_keyboard_backspace(self):
        # Enter "45"
        self._simulate_key("4", "4")
        self._simulate_key("5", "5")
        self.assertEqual(self.app.display.get_text(), "45")
        
        # Press BackSpace
        self._simulate_key("BackSpace")
        self.assertEqual(self.app.display.get_text(), "4")

    def test_keyboard_escape(self):
        # Enter "12"
        self._simulate_key("1", "1")
        self._simulate_key("2", "2")
        self.assertEqual(self.app.display.get_text(), "12")
        
        # Clear it
        self._simulate_key("Escape")
        self.assertEqual(self.app.display.get_text(), "")

    def test_keyboard_return(self):
        # Enter "6*7"
        self._simulate_key("6", "6")
        self._simulate_key("asterisk", "*")
        self._simulate_key("7", "7")
        self.assertEqual(self.app.display.get_text(), "6*7")
        
        # Press Return/Enter
        self._simulate_key("Return")
        self.assertEqual(self.app.display.get_text(), "42")


if __name__ == "__main__":
    unittest.main()
