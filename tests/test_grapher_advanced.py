import unittest
import tkinter as tk
import os
from unittest.mock import patch
from gui.app import CalculatorApp
from gui.graph_controller import PIL_AVAILABLE


class TestGrapherAdvanced(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def test_multi_function_plotting(self):
        # Insert sin(x) in y1 and cos(x) in y2
        self.app.graph_controller.graph_entries[0].delete(0, tk.END)
        self.app.graph_controller.graph_entries[0].insert(0, "sin(x)")
        self.app.graph_controller.graph_entries[1].delete(0, tk.END)
        self.app.graph_controller.graph_entries[1].insert(0, "cos(x)")
        self.app.graph_controller.graph_entries[2].delete(0, tk.END) # empty

        self.app.graph_controller.plot_function()
        
        # Check that items are drawn
        canvas_items = self.app.graph_controller.graph_canvas.find_all()
        self.assertTrue(len(canvas_items) > 0)

    def test_coordinate_tracing_hover(self):
        self.app.graph_controller.graph_entries[0].delete(0, tk.END)
        self.app.graph_controller.graph_entries[0].insert(0, "x^2")
        self.app.graph_controller.plot_function()

        # Mock Motion event at pixel x = 125, y = 120 (center)
        class MockEvent:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        self.app.graph_controller.on_mouse_hover(MockEvent(125, 120))
        
        # Verify that crosshair overlay elements were created
        crosshairs = self.app.graph_controller.graph_canvas.find_withtag("crosshair")
        self.assertTrue(len(crosshairs) > 0)

        # Tracing leave removes crosshair
        self.app.graph_controller.on_mouse_leave(None)
        crosshairs = self.app.graph_controller.graph_canvas.find_withtag("crosshair")
        self.assertEqual(len(crosshairs), 0)

    @unittest.skipIf(not PIL_AVAILABLE, "Pillow (PIL) is required for PNG export tests")
    @patch('tkinter.filedialog.asksaveasfilename')
    def test_export_png_image(self, mock_save_dialog):
        temp_png = "temp_test_graph.png"
        if os.path.exists(temp_png):
            os.remove(temp_png)

        mock_save_dialog.return_value = temp_png

        self.app.graph_controller.graph_entries[0].delete(0, tk.END)
        self.app.graph_controller.graph_entries[0].insert(0, "sin(x)")
        self.app.graph_controller.plot_function()

        # Trigger export
        self.app.graph_controller.export_png()

        # Check if file was written
        self.assertTrue(os.path.exists(temp_png))
        self.assertTrue(os.path.getsize(temp_png) > 0)

        # Cleanup
        if os.path.exists(temp_png):
            os.remove(temp_png)


    def test_polar_graphing(self):
        # Switch to Polar mode
        self.app.graph_controller.graph_mode.set("Polar")
        self.app.graph_controller.on_mode_change()
        
        # Verify theta range and default equation are set
        self.assertEqual(self.app.graph_controller.xmin_label.cget("text"), "θ min:")
        self.assertEqual(self.app.graph_controller.graph_entries[0].get(), "2 * cos(4 * theta)")
        
        # Plot function
        self.app.graph_controller.plot_function()
        canvas_items = self.app.graph_controller.graph_canvas.find_all()
        self.assertTrue(len(canvas_items) > 0)

    def test_parametric_graphing(self):
        # Switch to Parametric mode
        self.app.graph_controller.graph_mode.set("Parametric")
        self.app.graph_controller.on_mode_change()
        
        # Verify t range is set
        self.assertEqual(self.app.graph_controller.xmin_label.cget("text"), "t min:")
        
        # Plot
        self.app.graph_controller.plot_function()
        canvas_items = self.app.graph_controller.graph_canvas.find_all()
        self.assertTrue(len(canvas_items) > 0)

    def test_cartesian_key_points(self):
        # Switch to Cartesian and enable key points
        self.app.graph_controller.graph_mode.set("Cartesian")
        self.app.graph_controller.on_mode_change()
        self.app.graph_controller.show_key_points.set(True)
        
        # f(x) = x^2 - 4
        self.app.graph_controller.graph_entries[0].delete(0, tk.END)
        self.app.graph_controller.graph_entries[0].insert(0, "x^2 - 4")
        
        self.app.graph_controller.plot_function()
        canvas_items = self.app.graph_controller.graph_canvas.find_all()
        self.assertTrue(len(canvas_items) > 0)


if __name__ == "__main__":
    unittest.main()
