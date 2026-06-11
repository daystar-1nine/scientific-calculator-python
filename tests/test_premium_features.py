import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestPremiumFeatures(unittest.TestCase):

    def test_unit_converter_length(self):
        app = CalculatorApp()
        
        # Select Length category
        app.conv_cat.set("Length")
        app.update_converter_units()
        
        # Test 1 km to m
        app.conv_from.set("km")
        app.conv_to.set("m")
        app.conv_entry.delete(0, tk.END)
        app.conv_entry.insert(0, "1")
        app.run_conversion()
        self.assertEqual(app.conv_result_label.cget("text"), "1000 m")
        
        # Test 100 m to km
        app.conv_from.set("m")
        app.conv_to.set("km")
        app.conv_entry.delete(0, tk.END)
        app.conv_entry.insert(0, "100")
        app.run_conversion()
        self.assertEqual(app.conv_result_label.cget("text"), "0.1 km")
        
        app.root.update()
        app.root.destroy()

    def test_unit_converter_data(self):
        app = CalculatorApp()
        
        # Select Data category
        app.conv_cat.set("Data")
        app.update_converter_units()
        
        # Test 1 GB to MB
        app.conv_from.set("GB")
        app.conv_to.set("MB")
        app.conv_entry.delete(0, tk.END)
        app.conv_entry.insert(0, "1")
        app.run_conversion()
        self.assertEqual(app.conv_result_label.cget("text"), "1024 MB")
        
        app.root.update()
        app.root.destroy()

    def test_unit_converter_temperature(self):
        app = CalculatorApp()
        
        # Select Temperature category
        app.conv_cat.set("Temperature")
        app.update_converter_units()
        
        # Test 0 °C to °F
        app.conv_from.set("°C")
        app.conv_to.set("°F")
        app.conv_entry.delete(0, tk.END)
        app.conv_entry.insert(0, "0")
        app.run_conversion()
        self.assertEqual(app.conv_result_label.cget("text"), "32 °F")
        
        # Test 100 °C to K
        app.conv_from.set("°C")
        app.conv_to.set("K")
        app.conv_entry.delete(0, tk.END)
        app.conv_entry.insert(0, "100")
        app.run_conversion()
        self.assertEqual(app.conv_result_label.cget("text"), "373.15 K")
        
        app.root.update()
        app.root.destroy()

    def test_grapher_range_errors(self):
        app = CalculatorApp()
        
        # Set invalid xmin >= xmax
        app.graph_xmin_entry.delete(0, tk.END)
        app.graph_xmin_entry.insert(0, "10")
        app.graph_xmax_entry.delete(0, tk.END)
        app.graph_xmax_entry.insert(0, "-10")
        
        app.plot_function()
        
        # Check if error message text was written to canvas
        canvas_texts = [app.graph_canvas.itemcget(item, "text") for item in app.graph_canvas.find_all() if app.graph_canvas.type(item) == "text"]
        self.assertIn("Invalid X Range (xmin < xmax)", canvas_texts)
        
        app.root.update()
        app.root.destroy()

    def test_grapher_plotting(self):
        app = CalculatorApp()
        
        app.graph_entry.delete(0, tk.END)
        app.graph_entry.insert(0, "sin(x)")
        
        app.graph_xmin_entry.delete(0, tk.END)
        app.graph_xmin_entry.insert(0, "-10")
        app.graph_xmax_entry.delete(0, tk.END)
        app.graph_xmax_entry.insert(0, "10")
        
        app.plot_function()
        
        # Check that canvas has items drawn (lines, text)
        canvas_items = app.graph_canvas.find_all()
        self.assertTrue(len(canvas_items) > 0)
        
        app.root.update()
        app.root.destroy()


if __name__ == "__main__":
    unittest.main()
