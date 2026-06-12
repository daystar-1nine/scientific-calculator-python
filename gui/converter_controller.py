"""
Improved Controller for the Unit Converter tab.
Clean, modular, reusable design.
"""

import tkinter as tk


class ConverterController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        # Units definition
        self.units = {
            "Length": ["m", "km", "mi", "ft", "in", "cm"],
            "Area": ["m²", "km²", "mi²", "ft²", "acre", "hectare"],
            "Volume": ["L", "mL", "m³", "gal", "qt", "cup"],
            "Weight/Mass": ["g", "kg", "lb", "oz", "ton"],
            "Temperature": ["°C", "°F", "K"],
            "Speed": ["m/s", "km/h", "mph", "knot"],
            "Data": ["B", "KB", "MB", "GB", "TB"]
        }

        # Conversion factors (base units)
        self.factors = {
            "Length": {
                "m": 1.0, "km": 1000.0, "mi": 1609.344,
                "ft": 0.3048, "in": 0.0254, "cm": 0.01
            },
            "Area": {
                "m²": 1.0, "km²": 1e6, "mi²": 2589988.110336,
                "ft²": 0.09290304, "acre": 4046.8564224, "hectare": 10000.0
            },
            "Volume": {
                "L": 1.0, "mL": 0.001, "m³": 1000.0,
                "gal": 3.785411784, "qt": 0.946352946, "cup": 0.2365882365
            },
            "Weight/Mass": {
                "g": 1.0, "kg": 1000.0, "lb": 453.59237,
                "oz": 28.349523125, "ton": 907184.74
            },
            "Speed": {
                "m/s": 1.0, "km/h": 1 / 3.6,
                "mph": 0.44704, "knot": 0.514444444
            },
            "Data": {
                "B": 1.0, "KB": 1024.0, "MB": 1024**2,
                "GB": 1024**3, "TB": 1024**4
            }
        }

        # State variables
        self.conv_cat = tk.StringVar(value="Length")
        self.conv_from = tk.StringVar(value="m")
        self.conv_to = tk.StringVar(value="km")

        self.setup_ui()

    # ---------------------------
    # UI SETUP
    # ---------------------------
    def setup_ui(self):
        frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Category
        tk.Label(frame, text="Category:", fg="#D1D1D6", bg="#2C2C2E").pack(anchor="w")
        tk.OptionMenu(frame, self.conv_cat, *self.units.keys(),
                      command=self.update_converter_units).pack(fill="x")

        # From
        tk.Label(frame, text="From:", fg="#D1D1D6", bg="#2C2C2E").pack(anchor="w")
        self.menu_from = tk.OptionMenu(frame, self.conv_from, *self.units["Length"],
                                       command=self.run_conversion)
        self.menu_from.pack(fill="x")

        # To
        tk.Label(frame, text="To:", fg="#D1D1D6", bg="#2C2C2E").pack(anchor="w")
        self.menu_to = tk.OptionMenu(frame, self.conv_to, *self.units["Length"],
                                     command=self.run_conversion)
        self.menu_to.pack(fill="x")

        # Input
        tk.Label(frame, text="Value:", fg="#D1D1D6", bg="#2C2C2E").pack(anchor="w")
        self.conv_entry = tk.Entry(frame, bg="#1C1C1E", fg="#FFFFFF")
        self.conv_entry.pack(fill="x")
        self.conv_entry.insert(0, "1")
        self.conv_entry.bind("<KeyRelease>", self.run_conversion)

        # Result
        self.conv_result_label = tk.Label(
            frame, fg="#30D158", bg="#1C1C1E", font=("Segoe UI", 12, "bold")
        )
        self.conv_result_label.pack(fill="x", pady=10)

    # ---------------------------
    # UNIT UPDATE
    # ---------------------------
    def update_converter_units(self, *args):
        cat = self.conv_cat.get()
        units = self.units[cat]

        self.conv_from.set(units[0])
        self.conv_to.set(units[1])

        self.menu_from["menu"].delete(0, "end")
        self.menu_to["menu"].delete(0, "end")

        for u in units:
            self.menu_from["menu"].add_command(
                label=u,
                command=tk._setit(self.conv_from, u, self.run_conversion)
            )
            self.menu_to["menu"].add_command(
                label=u,
                command=tk._setit(self.conv_to, u, self.run_conversion)
            )

        self.run_conversion()

    # ---------------------------
    # CORE CONVERSION ENGINE
    # ---------------------------
    def convert_value(self, value, category, from_u, to_u):
        if category in self.factors:
            base = value * self.factors[category][from_u]
            return base / self.factors[category][to_u]

        if category == "Temperature":
            return self._convert_temperature(value, from_u, to_u)

        return value

    def _convert_temperature(self, val, from_u, to_u):
        # Convert to Celsius
        if from_u == "°F":
            val = (val - 32) * 5 / 9
        elif from_u == "K":
            val -= 273.15

        # Convert to target
        if to_u == "°F":
            return val * 9 / 5 + 32
        elif to_u == "K":
            return val + 273.15

        return val

    # ---------------------------
    # MAIN RUN FUNCTION
    # ---------------------------
    def run_conversion(self, *args):
        cat = self.conv_cat.get()
        from_u = self.conv_from.get()
        to_u = self.conv_to.get()

        raw = self.conv_entry.get().strip()
        if not raw:
            self.conv_result_label.config(text="")
            return

        try:
            value = float(raw)
        except ValueError:
            self.conv_result_label.config(text="Invalid number")
            return

        try:
            result = self.convert_value(value, cat, from_u, to_u)
            formatted = self.app.format_result(result)
            self.conv_result_label.config(text=f"{formatted} {to_u}")
        except Exception:
            self.conv_result_label.config(text="Error")