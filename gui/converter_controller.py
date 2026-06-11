"""
Controller for the Unit Converter tab.
"""

import tkinter as tk

class ConverterController:
    def __init__(self, app, tab_frame):
        self.app = app  # Reference to main CalculatorApp for format_result callback
        self.tab_frame = tab_frame

        # Complete set of unit categories and their units
        self.units = {
            "Length": ["m", "km", "mi", "ft", "in", "cm"],
            "Area": ["m²", "km²", "mi²", "ft²", "acre", "hectare"],
            "Volume": ["L", "mL", "m³", "gal", "qt", "cup"],
            "Weight/Mass": ["g", "kg", "lb", "oz", "ton"],
            "Temperature": ["°C", "°F", "K"],
            "Speed": ["m/s", "km/h", "mph", "knot"],
            "Data": ["B", "KB", "MB", "GB", "TB"]
        }

        # Conversion Factors (all relative to base unit)
        self.factors = {
            "Length": {
                "m": 1.0,
                "km": 1000.0,
                "mi": 1609.344,
                "ft": 0.3048,
                "in": 0.0254,
                "cm": 0.01
            },
            "Area": {
                "m²": 1.0,
                "km²": 1000000.0,
                "mi²": 2589988.110336,
                "ft²": 0.09290304,
                "acre": 4046.8564224,
                "hectare": 10000.0
            },
            "Volume": {
                "L": 1.0,
                "mL": 0.001,
                "m³": 1000.0,
                "gal": 3.785411784,
                "qt": 0.946352946,
                "cup": 0.2365882365
            },
            "Weight/Mass": {
                "g": 1.0,
                "kg": 1000.0,
                "lb": 453.59237,
                "oz": 28.349523125,
                "ton": 907184.74
            },
            "Speed": {
                "m/s": 1.0,
                "km/h": 1.0 / 3.6,
                "mph": 0.44704,
                "knot": 0.514444444
            },
            "Data": {
                "B": 1.0,
                "KB": 1024.0,
                "MB": 1048576.0,
                "GB": 1073741824.0,
                "TB": 1099511627776.0
            }
        }

        # State Variables
        self.conv_cat = tk.StringVar(value="Length")
        self.conv_from = tk.StringVar(value="m")
        self.conv_to = tk.StringVar(value="km")

        self.setup_ui()

    def setup_ui(self):
        # 1. Main inner container
        conv_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        conv_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 2. Category selection dropdown
        cat_label = tk.Label(conv_frame, text="Category:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        cat_label.pack(anchor="w", pady=(5, 2))

        cat_menu = tk.OptionMenu(
            conv_frame,
            self.conv_cat,
            *self.units.keys(),
            command=self.update_converter_units
        )
        cat_menu.config(bg="#3A3A3C", fg="#FFFFFF", font=("Segoe UI", 10), bd=0, relief="flat", highlightthickness=0)
        cat_menu["menu"].config(bg="#3A3A3C", fg="#FFFFFF", font=("Segoe UI", 10))
        cat_menu.pack(fill="x", pady=(0, 10))

        # 3. From Unit selection dropdown
        from_label = tk.Label(conv_frame, text="From:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        from_label.pack(anchor="w", pady=(5, 2))

        self.menu_from = tk.OptionMenu(
            conv_frame,
            self.conv_from,
            *self.units["Length"],
            command=self.run_conversion
        )
        self.menu_from.config(bg="#3A3A3C", fg="#FFFFFF", font=("Segoe UI", 10), bd=0, relief="flat", highlightthickness=0)
        self.menu_from["menu"].config(bg="#3A3A3C", fg="#FFFFFF", font=("Segoe UI", 10))
        self.menu_from.pack(fill="x", pady=(0, 10))

        # 4. To Unit selection dropdown
        to_label = tk.Label(conv_frame, text="To:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        to_label.pack(anchor="w", pady=(5, 2))

        self.menu_to = tk.OptionMenu(
            conv_frame,
            self.conv_to,
            *self.units["Length"],
            command=self.run_conversion
        )
        self.menu_to.config(bg="#3A3A3C", fg="#FFFFFF", font=("Segoe UI", 10), bd=0, relief="flat", highlightthickness=0)
        self.menu_to["menu"].config(bg="#3A3A3C", fg="#FFFFFF", font=("Segoe UI", 10))
        self.menu_to.pack(fill="x", pady=(0, 10))

        # 5. Input value Entry
        value_label = tk.Label(conv_frame, text="Value:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        value_label.pack(anchor="w", pady=(5, 2))

        self.conv_entry = tk.Entry(
            conv_frame,
            bg="#1C1C1E",
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            bd=5,
            relief="flat",
            insertbackground="#FFFFFF"
        )
        self.conv_entry.pack(fill="x", pady=(0, 10))
        self.conv_entry.insert(0, "1")
        self.conv_entry.bind("<KeyRelease>", self.run_conversion)

        # 6. Result output display label
        result_title_label = tk.Label(conv_frame, text="Result:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        result_title_label.pack(anchor="w", pady=(5, 2))

        self.conv_result_label = tk.Label(
            conv_frame,
            text="",
            fg="#30D158",
            bg="#1C1C1E",
            font=("Segoe UI", 12, "bold"),
            anchor="center",
            pady=10
        )
        self.conv_result_label.pack(fill="x", pady=5)

    def update_converter_units(self, *args):
        cat = self.conv_cat.get()
        unit_list = self.units[cat]

        self.conv_from.set(unit_list[0])
        self.conv_to.set(unit_list[1])

        if hasattr(self, "menu_from") and hasattr(self, "menu_to"):
            self.menu_from['menu'].delete(0, 'end')
            self.menu_to['menu'].delete(0, 'end')

            for u in unit_list:
                self.menu_from['menu'].add_command(label=u, command=tk._setit(self.conv_from, u, self.run_conversion))
                self.menu_to['menu'].add_command(label=u, command=tk._setit(self.conv_to, u, self.run_conversion))

        self.run_conversion()

    def run_conversion(self, *args):
        cat = self.conv_cat.get()
        from_u = self.conv_from.get()
        to_u = self.conv_to.get()

        raw_val = self.conv_entry.get().strip()
        if not raw_val:
            self.conv_result_label.config(text="")
            return

        try:
            val = float(raw_val)
        except ValueError:
            self.conv_result_label.config(text="Invalid number")
            return

        if cat in self.factors:
            val_in_base = val * self.factors[cat][from_u]
            result = val_in_base / self.factors[cat][to_u]
        elif cat == "Temperature":
            if from_u == to_u:
                result = val
            elif from_u == "°C" and to_u == "°F":
                result = val * 9 / 5 + 32
            elif from_u == "°C" and to_u == "K":
                result = val + 273.15
            elif from_u == "°F" and to_u == "°C":
                result = (val - 32) * 5 / 9
            elif from_u == "°F" and to_u == "K":
                result = (val - 32) * 5 / 9 + 273.15
            elif from_u == "K" and to_u == "°C":
                result = val - 273.15
            elif from_u == "K" and to_u == "°F":
                result = (val - 273.15) * 9 / 5 + 32
            else:
                result = val
        else:
            result = val

        # Format using app's format_result helper method
        formatted = self.app.format_result(result)
        self.conv_result_label.config(text=f"{formatted} {to_u}")
