import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestPremiumFeatures(unittest.TestCase):

    def test_unit_converter_length(self):
        app = CalculatorApp()
        
        # Select Length category via controller
        app.converter_controller.conv_cat.set("Length")
        app.converter_controller.update_converter_units()
        
        # Test 1 km to m
        app.converter_controller.conv_from.set("km")
        app.converter_controller.conv_to.set("m")
        app.converter_controller.conv_entry.delete(0, tk.END)
        app.converter_controller.conv_entry.insert(0, "1")
        app.converter_controller.run_conversion()
        self.assertEqual(app.converter_controller.conv_result_label.cget("text"), "1000 m")
        
        # Test 100 m to km
        app.converter_controller.conv_from.set("m")
        app.converter_controller.conv_to.set("km")
        app.converter_controller.conv_entry.delete(0, tk.END)
        app.converter_controller.conv_entry.insert(0, "100")
        app.converter_controller.run_conversion()
        self.assertEqual(app.converter_controller.conv_result_label.cget("text"), "0.1 km")
        
        app.root.update()
        app.root.destroy()

    def test_unit_converter_data(self):
        app = CalculatorApp()
        
        # Select Data category via controller
        app.converter_controller.conv_cat.set("Data")
        app.converter_controller.update_converter_units()
        
        # Test 1 GB to MB
        app.converter_controller.conv_from.set("GB")
        app.converter_controller.conv_to.set("MB")
        app.converter_controller.conv_entry.delete(0, tk.END)
        app.converter_controller.conv_entry.insert(0, "1")
        app.converter_controller.run_conversion()
        self.assertEqual(app.converter_controller.conv_result_label.cget("text"), "1024 MB")
        
        app.root.update()
        app.root.destroy()

    def test_unit_converter_temperature(self):
        app = CalculatorApp()
        
        # Select Temperature category via controller
        app.converter_controller.conv_cat.set("Temperature")
        app.converter_controller.update_converter_units()
        
        # Test 0 °C to °F
        app.converter_controller.conv_from.set("°C")
        app.converter_controller.conv_to.set("°F")
        app.converter_controller.conv_entry.delete(0, tk.END)
        app.converter_controller.conv_entry.insert(0, "0")
        app.converter_controller.run_conversion()
        self.assertEqual(app.converter_controller.conv_result_label.cget("text"), "32 °F")
        
        # Test 100 °C to K
        app.converter_controller.conv_from.set("°C")
        app.converter_controller.conv_to.set("K")
        app.converter_controller.conv_entry.delete(0, tk.END)
        app.converter_controller.conv_entry.insert(0, "100")
        app.converter_controller.run_conversion()
        self.assertEqual(app.converter_controller.conv_result_label.cget("text"), "373.15 K")
        
        app.root.update()
        app.root.destroy()

    def test_grapher_range_errors(self):
        app = CalculatorApp()
        
        # Set invalid xmin >= xmax via graph controller
        app.graph_controller.graph_xmin_entry.delete(0, tk.END)
        app.graph_controller.graph_xmin_entry.insert(0, "10")
        app.graph_controller.graph_xmax_entry.delete(0, tk.END)
        app.graph_controller.graph_xmax_entry.insert(0, "-10")
        
        app.graph_controller.plot_function()
        
        # Check if error message text was written to canvas
        canvas_texts = [
            app.graph_controller.graph_canvas.itemcget(item, "text")
            for item in app.graph_controller.graph_canvas.find_all()
            if app.graph_controller.graph_canvas.type(item) == "text"
        ]
        self.assertIn("Invalid X Range (xmin < xmax)", canvas_texts)
        
        app.root.update()
        app.root.destroy()

    def test_grapher_plotting(self):
        app = CalculatorApp()
        
        app.graph_controller.graph_entry.delete(0, tk.END)
        app.graph_controller.graph_entry.insert(0, "sin(x)")
        
        app.graph_controller.graph_xmin_entry.delete(0, tk.END)
        app.graph_controller.graph_xmin_entry.insert(0, "-10")
        app.graph_controller.graph_xmax_entry.delete(0, tk.END)
        app.graph_controller.graph_xmax_entry.insert(0, "10")
        
        app.graph_controller.plot_function()
        
        # Check that canvas has items drawn (lines, text)
        canvas_items = app.graph_controller.graph_canvas.find_all()
        self.assertTrue(len(canvas_items) > 0)
        
        app.root.update()
        app.root.destroy()


if __name__ == "__main__":
    unittest.main()
