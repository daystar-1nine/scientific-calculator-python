import unittest
from gui.app import CalculatorApp


class TestGUIInitialization(unittest.TestCase):

    def test_gui_init(self):
        app = CalculatorApp()
        self.assertIsNotNone(app.root)
        self.assertIsNotNone(app.display)
        self.assertIsNotNone(app.buttons)
        
        # Test widget creation
        self.assertEqual(app.root.title(), "Scientific Calculator")
        
        # Safely update and destroy tk root to finish test
        app.root.update()
        app.root.destroy()

    def test_display_font_scaling(self):
        app = CalculatorApp()
        
        # Length <= 15 -> size 22
        app.display.set_text("12345")
        font_config = app.display.entry.cget("font")
        self.assertIn("22", font_config)
        
        # Length 20 -> size 18
        app.display.set_text("12345678901234567890")
        font_config = app.display.entry.cget("font")
        self.assertIn("18", font_config)
        
        # Length 25 -> size 14
        app.display.set_text("1234567890123456789012345")
        font_config = app.display.entry.cget("font")
        self.assertIn("14", font_config)
        
        # Length 35 -> size 11
        app.display.set_text("12345678901234567890123456789012345")
        font_config = app.display.entry.cget("font")
        self.assertIn("11", font_config)
        
        app.root.update()
        app.root.destroy()

    def test_display_bracket_highlighting(self):
        app = CalculatorApp()
        
        # No brackets -> white (#FFFFFF)
        app.display.set_text("2 + 3")
        fg = app.display.entry.cget("fg").upper()
        # On some platforms cget('fg') might return system names, but since we set it to #FFFFFF:
        self.assertTrue(fg == "#FFFFFF" or fg == "WHITE")
        
        # Balanced brackets -> white
        app.display.set_text("(2 + 3)")
        fg = app.display.entry.cget("fg").upper()
        self.assertTrue(fg == "#FFFFFF" or fg == "WHITE")
        
        # Unbalanced brackets -> amber (#FFCC00)
        app.display.set_text("(2 + 3")
        fg = app.display.entry.cget("fg").upper()
        self.assertEqual(fg, "#FFCC00")
        
        app.root.update()
        app.root.destroy()

    def test_format_result_giant_numbers(self):
        app = CalculatorApp()
        
        # Test standard numbers
        self.assertEqual(app.format_result(123), "123")
        self.assertEqual(app.format_result(123.45), "123.45")
        self.assertEqual(app.format_result(120.0), "120")
        
        # Test giant integer (> 1e12) -> scientific notation via string formatting
        self.assertEqual(app.format_result(10000000000000), "1e+13")
        self.assertEqual(app.format_result(1234567890123456), "1.234567e+15")
        self.assertEqual(app.format_result(-1234567890123456), "-1.234567e+15")
        
        # Test float formatting rules
        self.assertEqual(app.format_result(1e15), "1e+15")
        self.assertEqual(app.format_result(1e-11), "1.000000e-11")
        
        app.root.update()
        app.root.destroy()


if __name__ == "__main__":
    unittest.main()
