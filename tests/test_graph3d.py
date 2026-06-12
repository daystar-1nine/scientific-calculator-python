import unittest
import tkinter as tk
from gui.app import CalculatorApp

class TestGraph3D(unittest.TestCase):
    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.destroy()

    def test_graph3d_plot_runs(self):
        controller = self.app.graph3d_controller
        controller.expr_var.set("sin(x)*cos(y)")
        
        # Test rendering runs without error
        controller.plot_3d()
        
        lines = controller.canvas.find_all()
        self.assertGreater(len(lines), 0)

    def test_graph3d_rotation(self):
        controller = self.app.graph3d_controller
        initial_yaw = controller.yaw
        initial_pitch = controller.pitch
        
        class MockEvent:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        # Simulate drag
        controller.on_click(MockEvent(100, 100))
        controller.on_drag(MockEvent(120, 90))
        
        self.assertNotEqual(controller.yaw, initial_yaw)
        self.assertNotEqual(controller.pitch, initial_pitch)
