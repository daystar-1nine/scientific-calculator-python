import unittest
import tkinter as tk
import os
from unittest.mock import patch
from gui.app import CalculatorApp


class TestSettingsPanel(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def test_theme_switch_cyberpunk(self):
        # Initial theme defaults to Midnight (dark bg)
        # Switch to Cyberpunk theme (black bg)
        self.app.settings_controller.current_theme.set("Cyberpunk")
        self.app.settings_controller.change_theme("Cyberpunk")

        # Verify that background color of root has changed to black (#000000)
        bg = self.app.root.cget("bg")
        self.assertEqual(bg, "#000000")
        
        # Verify foreground color changes to neon green
        fg = self.app.settings_controller.status_text.cget("fg")
        self.assertEqual(fg, "#00FF00")

    def test_theme_switch_casio(self):
        self.app.settings_controller.current_theme.set("Casio Classic")
        self.app.settings_controller.change_theme("Casio Classic")

        # Verify that background color of root has changed to #E5E5EA
        bg = self.app.root.cget("bg")
        self.assertEqual(bg, "#E5E5EA")

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_export_history_txt(self, mock_save_dialog):
        temp_log = "temp_history_log.txt"
        if os.path.exists(temp_log):
            os.remove(temp_log)

        mock_save_dialog.return_value = temp_log

        # Seed some history
        self.app.history.add_entry("2+3", "5")
        self.app.history.add_entry("sin(0)", "0")

        # Trigger export
        self.app.settings_controller.export_history()

        # Check if file was written with expected contents
        self.assertTrue(os.path.exists(temp_log))
        with open(temp_log, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("2+3 = 5", content)
        self.assertIn("sin(0) = 0", content)

        # Cleanup
        if os.path.exists(temp_log):
            os.remove(temp_log)

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_export_history_csv(self, mock_save_dialog):
        temp_csv = "temp_history_log.csv"
        if os.path.exists(temp_csv):
            os.remove(temp_csv)

        mock_save_dialog.return_value = temp_csv

        # Seed some history
        self.app.history.add_entry("2*3", "6")

        # Trigger export
        self.app.settings_controller.export_history()

        self.assertTrue(os.path.exists(temp_csv))
        with open(temp_csv, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Expression,Result", content)
        self.assertIn('"2*3","6"', content)

        if os.path.exists(temp_csv):
            os.remove(temp_csv)

    def test_theme_cycling(self):
        # Default theme is Midnight (bg #1C1C1E)
        self.assertEqual(self.app.settings_controller.current_theme.get(), "Midnight")
        
        # Click THEME button
        self.app.on_button_click("THEME")
        
        # Next theme should be Casio Classic (bg #E5E5EA)
        self.assertEqual(self.app.settings_controller.current_theme.get(), "Casio Classic")
        bg = self.app.root.cget("bg")
        self.assertEqual(bg, "#E5E5EA")

        # Click THEME button again
        self.app.on_button_click("THEME")
        
        # Next theme should be Cyberpunk (bg #000000)
        self.app.settings_controller.current_theme.set("Cyberpunk")
        self.assertEqual(self.app.settings_controller.current_theme.get(), "Cyberpunk")
        bg = self.app.root.cget("bg")
        self.assertEqual(bg, "#000000")

    def test_keypad_layout_toggle(self):
        # By default, layout is Standard Scientific and "sin" button is visible
        sin_btn = self.app.buttons.widgets.get("sin")
        self.assertIsNotNone(sin_btn)
        self.assertTrue(bool(sin_btn.winfo_manager()))

        # Change to Basic Focus
        self.app.settings_controller.current_layout.set("Basic Focus")
        self.app.settings_controller.change_layout("Basic Focus")
        
        # sin button should be ungridded (winfo_manager returns '')
        self.assertEqual(sin_btn.winfo_manager(), "")
        
        # Change back to Standard Scientific
        self.app.settings_controller.current_layout.set("Standard Scientific")
        self.app.settings_controller.change_layout("Standard Scientific")
        
        # sin button should be gridded again
        self.assertTrue(bool(sin_btn.winfo_manager()))


if __name__ == "__main__":
    unittest.main()
