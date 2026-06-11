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


if __name__ == "__main__":
    unittest.main()
