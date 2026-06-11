"""
Main calculator window.
"""

import math
import tkinter as tk

from gui.display import Display
from gui.buttons import ButtonPanel
from core.evaluator import Evaluator
from core.modes import CalculatorMode
from features.memory import Memory
from features.history import History
from utils.error_handler import handle_error


class CalculatorApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Scientific Calculator")
        self.root.geometry("480x550")
        self.root.resizable(False, False)

        # State Managers
        self.evaluator = Evaluator()
        self.mode_manager = CalculatorMode()
        self.memory = Memory()
        self.history = History()

        # GUI Setup
        self.root.configure(bg="#1C1C1E")

        # Main layout container
        self.main_frame = tk.Frame(self.root, bg="#1C1C1E")
        self.main_frame.pack(fill="both", expand=True)

        # Left side: Calculator keys and display
        self.calc_frame = tk.Frame(self.main_frame, bg="#1C1C1E", width=480)
        self.calc_frame.pack(side="left", fill="both", expand=True)

        # Display
        self.display = Display(self.calc_frame)

        # Button frame
        self.button_frame = tk.Frame(self.calc_frame, bg="#1C1C1E")
        self.button_frame.pack(fill="both", expand=True, padx=8, pady=8)

        self.buttons = ButtonPanel(self.button_frame)
        self.buttons.create_buttons(self.on_button_click)

        # Sync the mode button text with default
        self.update_mode_button_text()

        # Right side: Sidebar frame (initially hidden)
        self.sidebar_frame = tk.Frame(self.main_frame, bg="#2C2C2E", width=280)
        self.sidebar_visible = False

        # Tab switch headers
        self.sidebar_tabs_frame = tk.Frame(self.sidebar_frame, bg="#2C2C2E")
        self.sidebar_tabs_frame.pack(fill="x", padx=5, pady=5)

        self.active_tab = "History"

        # Tabs container
        self.sidebar_content_frame = tk.Frame(self.sidebar_frame, bg="#2C2C2E")
        self.sidebar_content_frame.pack(fill="both", expand=True)

        # Create Tab Frames
        self.tab_history = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_graph = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_conv = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")

        # Tab buttons
        self.tab_hist_btn = tk.Button(
            self.sidebar_tabs_frame, text="History", bg="#FF9500", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", padx=10, pady=5,
            command=lambda: self.switch_sidebar_tab("History")
        )
        self.tab_hist_btn.pack(side="left", fill="x", expand=True, padx=2)

        self.tab_graph_btn = tk.Button(
            self.sidebar_tabs_frame, text="Grapher", bg="#48484A", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", padx=10, pady=5,
            command=lambda: self.switch_sidebar_tab("Grapher")
        )
        self.tab_graph_btn.pack(side="left", fill="x", expand=True, padx=2)

        self.tab_conv_btn = tk.Button(
            self.sidebar_tabs_frame, text="Converter", bg="#48484A", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", padx=10, pady=5,
            command=lambda: self.switch_sidebar_tab("Converter")
        )
        self.tab_conv_btn.pack(side="left", fill="x", expand=True, padx=2)

        # --- 1. History Tab Widgets ---
        list_frame = tk.Frame(self.tab_history, bg="#2C2C2E")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.history_scrollbar = tk.Scrollbar(list_frame)
        self.history_scrollbar.pack(side="right", fill="y")

        self.history_listbox = tk.Listbox(
            list_frame,
            bg="#1C1C1E",
            fg="#FFFFFF",
            selectbackground="#FF9500",
            selectforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            highlightthickness=0,
            yscrollcommand=self.history_scrollbar.set
        )
        self.history_listbox.pack(side="left", fill="both", expand=True)
        self.history_scrollbar.config(command=self.history_listbox.yview)

        # Bind listbox selection event
        self.history_listbox.bind("<<ListboxSelect>>", self.on_history_select)

        # Clear history button
        clear_hist_btn = tk.Button(
            self.tab_history,
            text="Clear History",
            bg="#FF3B30",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            relief="flat",
            activebackground="#FF453A",
            activeforeground="#FFFFFF",
            height=2,
            command=self.clear_history
        )
        clear_hist_btn.pack(fill="x", padx=10, pady=10)

        # --- 2. Grapher Tab Widgets ---
        graph_header_frame = tk.Frame(self.tab_graph, bg="#2C2C2E")
        graph_header_frame.pack(fill="x", padx=10, pady=5)

        graph_title = tk.Label(
            graph_header_frame,
            text="y = ",
            fg="#FFFFFF",
            bg="#2C2C2E",
            font=("Segoe UI", 11, "bold")
        )
        graph_title.pack(side="left")

        self.graph_entry = tk.Entry(
            graph_header_frame,
            bg="#1C1C1E",
            fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            bd=5,
            relief="flat",
            insertbackground="#FFFFFF"
        )
        self.graph_entry.pack(side="left", fill="x", expand=True)
        self.graph_entry.insert(0, "sin(x)")

        # Range inputs frame
        graph_range_frame = tk.Frame(self.tab_graph, bg="#2C2C2E")
        graph_range_frame.pack(fill="x", padx=10, pady=2)

        xmin_label = tk.Label(graph_range_frame, text="x min:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        xmin_label.pack(side="left", padx=(0, 2))

        self.graph_xmin_entry = tk.Entry(
            graph_range_frame,
            bg="#1C1C1E",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            bd=3,
            relief="flat",
            insertbackground="#FFFFFF",
            width=6
        )
        self.graph_xmin_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.graph_xmin_entry.insert(0, "-10")

        xmax_label = tk.Label(graph_range_frame, text="x max:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        xmax_label.pack(side="left", padx=(0, 2))

        self.graph_xmax_entry = tk.Entry(
            graph_range_frame,
            bg="#1C1C1E",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            bd=3,
            relief="flat",
            insertbackground="#FFFFFF",
            width=6
        )
        self.graph_xmax_entry.pack(side="left", fill="x", expand=True)
        self.graph_xmax_entry.insert(0, "10")

        # Plot button
        plot_btn = tk.Button(
            self.tab_graph,
            text="Plot Function",
            bg="#30D158",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            relief="flat",
            activebackground="#34C759",
            activeforeground="#FFFFFF",
            height=2,
            command=self.plot_function
        )
        plot_btn.pack(fill="x", padx=10, pady=5)

        # Canvas
        self.graph_canvas = tk.Canvas(
            self.tab_graph,
            width=250,
            height=280,
            bg="#1C1C1E",
            bd=0,
            highlightthickness=0
        )
        self.graph_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # --- 3. Converter Tab Widgets ---
        conv_frame = tk.Frame(self.tab_conv, bg="#2C2C2E")
        conv_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Category selection
        cat_label = tk.Label(conv_frame, text="Category:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        cat_label.pack(anchor="w", pady=(5, 2))

        self.conv_cat = tk.StringVar(value="Length")
        self.units = {
            "Length": ["m", "km", "mi", "ft", "in", "cm"],
            "Area": ["m²", "km²", "mi²", "ft²", "acre", "hectare"],
            "Volume": ["L", "mL", "m³", "gal", "qt", "cup"],
            "Weight/Mass": ["g", "kg", "lb", "oz", "ton"],
            "Temperature": ["°C", "°F", "K"],
            "Speed": ["m/s", "km/h", "mph", "knot"],
            "Data": ["B", "KB", "MB", "GB", "TB"]
        }
        self.conv_from = tk.StringVar(value="m")
        self.conv_to = tk.StringVar(value="km")

        cat_menu = tk.OptionMenu(
            conv_frame,
            self.conv_cat,
            *self.units.keys(),
            command=self.update_converter_units
        )
        cat_menu.config(bg="#3A3A3C", fg="#FFFFFF", font=("Segoe UI", 10), bd=0, relief="flat", highlightthickness=0)
        cat_menu["menu"].config(bg="#3A3A3C", fg="#FFFFFF", font=("Segoe UI", 10))
        cat_menu.pack(fill="x", pady=(0, 10))

        # From Unit selection
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

        # To Unit selection
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

        # Input value Entry
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

        # Result output display
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

        # Bind physical keyboard events
        self.root.bind("<Key>", self.on_key_press)

    def on_button_click(self, char):
        current_text = self.display.get_text()

        # Handle clear
        if char == "C":
            self.display.clear()

        # Handle backspace
        elif char == "DEL":
            self.display.set_text(current_text[:-1])

        # Handle Mode Toggle
        elif char == "DEG":
            mode = self.mode_manager.get_mode()
            if mode == CalculatorMode.DEGREE:
                self.mode_manager.set_radian()
            else:
                self.mode_manager.set_degree()
            self.update_mode_button_text()

        # Handle Memory operations
        elif char == "MC":
            self.memory.clear()
            self.update_memory_indicator()
        elif char == "MR":
            val = self.memory.recall()
            self.display.append(self.format_result(val))
        elif char == "M+":
            if current_text:
                try:
                    res = self.evaluator.evaluate(current_text, self.mode_manager.get_mode())
                    self.memory.add(res)
                    self.update_memory_indicator()
                except Exception as e:
                    self.display.set_text(handle_error(e))
        elif char == "M-":
            if current_text:
                try:
                    res = self.evaluator.evaluate(current_text, self.mode_manager.get_mode())
                    self.memory.subtract(res)
                    self.update_memory_indicator()
                except Exception as e:
                    self.display.set_text(handle_error(e))

        # Handle History toggle
        elif char == "HIST":
            self.toggle_history()

        # Handle Equal evaluation
        elif char == "=":
            if not current_text:
                return
            try:
                raw_res = self.evaluator.evaluate(current_text, self.mode_manager.get_mode())
                formatted_res = self.format_result(raw_res)
                self.display.set_text(formatted_res)
                self.history.add_entry(current_text, formatted_res)
                if self.sidebar_visible and self.active_tab == "History":
                    self.update_history_display()
            except Exception as e:
                self.display.set_text(handle_error(e))

        # Handle Scientific functions (append opening parenthesis)
        elif char in ["sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp", "log", "ln", "sqrt"]:
            self.display.append(f"{char}(")

        # Handle advanced power keys
        elif char == "x^2":
            self.display.append("^2")
        elif char == "x^3":
            self.display.append("^3")
        elif char == "1/x":
            self.display.append("1/(")
        elif char == "e^x":
            self.display.append("e^")

        # Standard append
        else:
            self.display.append(char)

    def update_mode_button_text(self):
        mode = self.mode_manager.get_mode()
        # Find the mode button and update its text
        if hasattr(self.buttons, "widgets") and "DEG" in self.buttons.widgets:
            self.buttons.widgets["DEG"].config(text=mode)
        # Update display screen mode indicator
        self.display.set_mode_indicator(mode)

    def update_memory_indicator(self):
        has_value = self.memory.recall() != 0.0
        self.display.set_memory_indicator(has_value)

    def toggle_history(self):
        if self.sidebar_visible:
            self.sidebar_frame.pack_forget()
            self.root.geometry("480x550")
            self.sidebar_visible = False
        else:
            self.root.geometry("760x550")
            self.sidebar_frame.pack(side="right", fill="both", expand=True)
            self.switch_sidebar_tab(self.active_tab)
            self.sidebar_visible = True

    def switch_sidebar_tab(self, tab_name):
        self.active_tab = tab_name

        # Reset button colors
        self.tab_hist_btn.config(bg="#48484A")
        self.tab_graph_btn.config(bg="#48484A")
        self.tab_conv_btn.config(bg="#48484A")

        # Unpack all frames
        self.tab_history.pack_forget()
        self.tab_graph.pack_forget()
        self.tab_conv.pack_forget()

        # Switch and highlight
        if tab_name == "History":
            self.tab_hist_btn.config(bg="#FF9500")
            self.tab_history.pack(fill="both", expand=True)
            self.update_history_display()
        elif tab_name == "Grapher":
            self.tab_graph_btn.config(bg="#FF9500")
            self.tab_graph.pack(fill="both", expand=True)
            self.plot_function()
        elif tab_name == "Converter":
            self.tab_conv_btn.config(bg="#FF9500")
            self.tab_conv.pack(fill="both", expand=True)
            self.run_conversion()

    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        for entry in self.history.get_history():
            self.history_listbox.insert(tk.END, entry)
        self.history_listbox.yview_moveto(1.0)

    def clear_history(self):
        self.history.clear_history()
        self.update_history_display()

    def on_history_select(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            idx = selection[0]
            entry_text = self.history_listbox.get(idx)
            if " = " in entry_text:
                expr = entry_text.split(" = ")[0]
                self.display.set_text(expr)

    def plot_function(self):
        expr = self.graph_entry.get().strip()
        if not expr:
            return

        self.graph_canvas.delete("all")

        W, H = 250, 280

        # Parse custom range
        try:
            xmin = float(self.graph_xmin_entry.get().strip())
            xmax = float(self.graph_xmax_entry.get().strip())
            if xmin >= xmax:
                raise ValueError("xmin >= xmax")
        except Exception:
            self.graph_canvas.create_text(
                W / 2, H / 2,
                text="Invalid X Range (xmin < xmax)",
                fill="#FF3B30",
                font=("Segoe UI", 10, "bold")
            )
            return

        # Evaluate 100 points across the range
        pts = []
        x_vals = [xmin + (xmax - xmin) * i / 99 for i in range(100)]
        mode = self.mode_manager.get_mode()

        for x in x_vals:
            try:
                y = self.evaluator.evaluate(expr, mode, variables={"x": x})
                if isinstance(y, (int, float)) and not math.isnan(y) and not math.isinf(y):
                    pts.append((x, y))
                else:
                    pts.append((x, None))
            except Exception:
                pts.append((x, None))

        valid_y = [y for _, y in pts if y is not None]
        if not valid_y:
            self.graph_canvas.create_text(
                W / 2, H / 2,
                text="Error evaluating function",
                fill="#FF3B30",
                font=("Segoe UI", 10, "bold")
            )
            return

        # Outlier rejection using percentiles to gracefully handle asymptotes (e.g. 1/x, tan(x))
        sorted_y = sorted(valid_y)
        n = len(sorted_y)
        if n > 10:
            p5 = sorted_y[int(n * 0.05)]
            p95 = sorted_y[int(n * 0.95)]
            margin = (p95 - p5) * 0.1 if p95 > p5 else 1.0
            ymin = p5 - margin
            ymax = p95 + margin
        else:
            ymin, ymax = min(valid_y), max(valid_y)

        # Handle flat lines
        if abs(ymax - ymin) < 1e-9:
            ymin -= 1.0
            ymax += 1.0

        # Helper functions to convert coordinates to pixel positions
        def to_px(x_val):
            return (x_val - xmin) / (xmax - xmin) * W

        def to_py(y_val):
            return H - (y_val - ymin) / (ymax - ymin) * H

        # Nice tick step calculator
        def get_nice_step(range_val):
            raw_step = range_val / 5.0
            if raw_step <= 0:
                return 1.0
            power = math.floor(math.log10(raw_step))
            ratio = raw_step / (10**power)
            if ratio < 1.5:
                nice_ratio = 1.0
            elif ratio < 3.0:
                nice_ratio = 2.0
            elif ratio < 7.0:
                nice_ratio = 5.0
            else:
                nice_ratio = 10.0
            return nice_ratio * (10**power)

        x_step = get_nice_step(xmax - xmin)
        y_step = get_nice_step(ymax - ymin)

        # Draw grid lines and labels
        # 1. Vertical grid lines
        start_x = math.ceil(xmin / x_step) * x_step
        curr_x = start_x
        while curr_x <= xmax:
            px = to_px(curr_x)
            self.graph_canvas.create_line(px, 0, px, H, fill="#2C2C2E", width=1)
            label_text = f"{curr_x:.4g}"
            if abs(curr_x) > 1e-9:
                self.graph_canvas.create_text(
                    px, H - 10,
                    text=label_text,
                    fill="#8E8E93",
                    font=("Segoe UI", 7)
                )
            curr_x += x_step

        # 2. Horizontal grid lines
        start_y = math.ceil(ymin / y_step) * y_step
        curr_y = start_y
        while curr_y <= ymax:
            py = to_py(curr_y)
            self.graph_canvas.create_line(0, py, W, py, fill="#2C2C2E", width=1)
            label_text = f"{curr_y:.4g}"
            if abs(curr_y) > 1e-9:
                self.graph_canvas.create_text(
                    15, py,
                    text=label_text,
                    fill="#8E8E93",
                    font=("Segoe UI", 7),
                    anchor="w"
                )
            curr_y += y_step

        # Draw Axes
        if ymin <= 0 <= ymax:
            py_zero = to_py(0)
            self.graph_canvas.create_line(0, py_zero, W, py_zero, fill="#555555", width=2)
            if xmin <= 0 <= xmax:
                px_zero = to_px(0)
                self.graph_canvas.create_text(
                    px_zero - 5, py_zero + 10,
                    text="0",
                    fill="#8E8E93",
                    font=("Segoe UI", 7)
                )
        if xmin <= 0 <= xmax:
            px_zero = to_px(0)
            self.graph_canvas.create_line(px_zero, 0, px_zero, H, fill="#555555", width=2)

        # Plot curve (draw continuous line segments)
        coords = []
        for x, y in pts:
            if y is not None:
                px = to_px(x)
                py = to_py(y)
                py_clipped = max(-2 * H, min(3 * H, py))
                coords.append((px, py_clipped))
            else:
                if len(coords) > 1:
                    flat_coords = [c for pt in coords for c in pt]
                    self.graph_canvas.create_line(flat_coords, fill="#FF9500", width=2)
                coords = []

        if len(coords) > 1:
            flat_coords = [c for pt in coords for c in pt]
            self.graph_canvas.create_line(flat_coords, fill="#FF9500", width=2)

        # Outermost bounds indicator
        self.graph_canvas.create_text(
            W - 10, 15,
            text=f"y max: {self.format_result(ymax)[:6]}",
            fill="#FF9500",
            font=("Segoe UI", 8, "bold"),
            anchor="e"
        )
        self.graph_canvas.create_text(
            W - 10, H - 15,
            text=f"y min: {self.format_result(ymin)[:6]}",
            fill="#FF9500",
            font=("Segoe UI", 8, "bold"),
            anchor="e"
        )

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

        # Conversion Factors (all keys match self.units categories)
        factors = {
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

        if cat in factors:
            val_in_base = val * factors[cat][from_u]
            result = val_in_base / factors[cat][to_u]
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

        self.conv_result_label.config(text=f"{self.format_result(result)} {to_u}")

    def on_key_press(self, event):
        char = event.char
        keysym = event.keysym

        if not char and keysym:
            if keysym.isdigit():
                char = keysym
            elif keysym == "plus":
                char = "+"
            elif keysym == "minus":
                char = "-"
            elif keysym == "asterisk":
                char = "*"
            elif keysym == "slash":
                char = "/"
            elif keysym == "parenleft":
                char = "("
            elif keysym == "parenright":
                char = ")"
            elif keysym == "exclam":
                char = "!"
            elif keysym == "asciicircum":
                char = "^"
            elif keysym == "period":
                char = "."

        if keysym in ["Return", "KP_Enter"]:
            self.on_button_click("=")
            return "break"
        elif keysym == "BackSpace":
            self.on_button_click("DEL")
            return "break"
        elif keysym == "Escape":
            self.on_button_click("C")
            return "break"
        elif char in "0123456789.+-*/^!()":
            self.on_button_click(char)
            return "break"

    def format_result(self, value):
        if isinstance(value, int) and not isinstance(value, bool):
            if abs(value) > 1e12:
                s = str(value)
                sign = "-" if s[0] == "-" else ""
                digits = s.lstrip("-")
                exponent = len(digits) - 1
                mantissa = digits[0] + "." + digits[1:7]
                mantissa = mantissa.rstrip('0').rstrip('.')
                return f"{sign}{mantissa}e+{exponent}"
            return str(value)

        if isinstance(value, float):
            if value.is_integer():
                return self.format_result(int(value))
            res = f"{value:.10f}".rstrip('0').rstrip('.')
            if abs(value) > 1e12 or (abs(value) < 1e-10 and value != 0):
                return f"{value:.6e}"
            return res
        return str(value)

    def run(self):
        self.root.mainloop()