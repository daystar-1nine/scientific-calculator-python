import unittest
import tkinter as tk
import math
from gui.app import CalculatorApp
from gui.simulations_controller import SimulationsController

class TestSimulationsSuite(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()
        self.frame = tk.Frame(self.app.root)
        self.controller = SimulationsController(self.app, self.frame)

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def test_projectile_parameter_validation(self):
        self.controller.proj_v0.set("50")
        self.controller.proj_theta.set("45")
        self.controller.proj_g.set("9.81")
        
        v0, theta, g = self.controller.get_projectile_params()
        self.assertAlmostEqual(v0, 50.0)
        self.assertAlmostEqual(theta, math.radians(45.0))
        self.assertAlmostEqual(g, 9.81)

        # Invalid entries
        self.controller.proj_v0.set("-10")
        with self.assertRaises(ValueError):
            self.controller.get_projectile_params()

        self.controller.proj_v0.set("50")
        self.controller.proj_g.set("-9.81")
        with self.assertRaises(ValueError):
            self.controller.get_projectile_params()

    def test_projectile_motion_math(self):
        self.controller.proj_v0.set("50")
        self.controller.proj_theta.set("45")
        self.controller.proj_g.set("9.81")
        
        v0, theta, g = self.controller.get_projectile_params()
        t_flight = (2.0 * v0 * math.sin(theta)) / g
        x_max = (v0**2 * math.sin(2.0 * theta)) / g
        y_max = (v0 * math.sin(theta))**2 / (2.0 * g)
        
        self.assertAlmostEqual(t_flight, 7.208, places=2)
        self.assertAlmostEqual(x_max, 254.84, places=2)
        self.assertAlmostEqual(y_max, 63.71, places=2)

    def test_fourier_wave_builder(self):
        self.controller.sim_mode.set("Fourier Wave Builder")
        self.controller.fourier_shape.set("Square")
        self.controller.fourier_terms.set(5)
        self.controller.on_mode_change()
        
        # Canvas should have drawn line items
        items = self.controller.canvas.find_all()
        self.assertTrue(len(items) > 0)

        # Switch to Sawtooth
        self.controller.fourier_shape.set("Sawtooth")
        self.controller.redraw()
        items = self.controller.canvas.find_all()
        self.assertTrue(len(items) > 0)

        # Switch to Triangle
        self.controller.fourier_shape.set("Triangle")
        self.controller.redraw()
        items = self.controller.canvas.find_all()
        self.assertTrue(len(items) > 0)

if __name__ == "__main__":
    unittest.main()
