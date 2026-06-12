"""
Controller for the Statistics & Probability tab.
"""

import math
import tkinter as tk
from utils.error_handler import handle_error, MathOperationError, InvalidExpressionError

class StatsController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.stats_type = tk.StringVar(value="Descriptive Stats")
        self.prob_op = tk.StringVar(value="nCr")
        self.param_entries = {}

        self.setup_ui()

    def setup_ui(self):
        # 1. Main Stats type selector
        select_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        select_frame.pack(fill="x", padx=10, pady=5)

        type_label = tk.Label(
            select_frame, text="Type:", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 10, "bold")
        )
        type_label.pack(side="left", padx=(0, 10))

        type_menu = tk.OptionMenu(
            select_frame,
            self.stats_type,
            "Descriptive Stats", "Linear Regression", "Probability Helpers",
            command=self.on_type_change
        )
        type_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        type_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        type_menu.pack(side="left")

        # 2. Parameters container frame
        self.params_container = tk.Frame(self.tab_frame, bg="#2C2C2E")
        self.params_container.pack(fill="x", padx=10, pady=5)

        # 3. Calculate Button
        calc_btn = tk.Button(
            self.tab_frame, text="Calculate Statistics", bg="#30D158", fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"), bd=0, relief="flat", height=2,
            command=self.calculate
        )
        calc_btn.pack(fill="x", padx=10, pady=5)

        # 4. Result label display
        res_label = tk.Label(
            self.tab_frame, text="Results:", fg="#8E8E93", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), anchor="w"
        )
        res_label.pack(fill="x", padx=10, pady=(10, 2))

        self.result_text = tk.Text(
            self.tab_frame, bg="#1C1C1E", fg="#30D158",
            font=("Consolas", 10, "bold"), height=8, bd=0, highlightthickness=0,
            padx=10, pady=10
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.result_text.config(state="disabled")

        # Visual Chart Canvas (Premium Feature: Histogram / Scatter Plot)
        self.chart_canvas = tk.Canvas(
            self.tab_frame, bg="#1C1C1E", height=140, bd=0, highlightthickness=0
        )
        self.chart_canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.on_type_change()

    def on_type_change(self, *args):
        # Clear params container
        for w in self.params_container.winfo_children():
            w.destroy()
        self.param_entries = {}

        if hasattr(self, "chart_canvas"):
            self.chart_canvas.delete("all")

        t = self.stats_type.get()
        if t == "Descriptive Stats":
            self.setup_desc_ui()
        elif t == "Linear Regression":
            self.setup_regression_ui()
        elif t == "Probability Helpers":
            self.setup_probability_ui()

    def show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    # --- UI Builders ---
    def setup_desc_ui(self):
        tk.Label(
            self.params_container, text="Enter values (comma separated):",
            fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold")
        ).pack(fill="x", anchor="w", pady=(2, 5))
        
        self.param_entries["values"] = tk.Entry(
            self.params_container, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF"
        )
        self.param_entries["values"].pack(fill="x", pady=2)
        self.param_entries["values"].insert(0, "10, 15.5, 23, 14.2, 8.8")

    def setup_regression_ui(self):
        # X dataset
        tk.Label(
            self.params_container, text="X Values (comma separated):",
            fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold")
        ).pack(fill="x", anchor="w", pady=(2, 2))
        self.param_entries["x_vals"] = tk.Entry(
            self.params_container, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF"
        )
        self.param_entries["x_vals"].pack(fill="x", pady=(0, 5))
        self.param_entries["x_vals"].insert(0, "1, 2, 3, 4, 5")

        # Y dataset
        tk.Label(
            self.params_container, text="Y Values (comma separated):",
            fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold")
        ).pack(fill="x", anchor="w", pady=(2, 2))
        self.param_entries["y_vals"] = tk.Entry(
            self.params_container, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF"
        )
        self.param_entries["y_vals"].pack(fill="x", pady=(0, 5))
        self.param_entries["y_vals"].insert(0, "2, 4, 5, 4, 5")

    def setup_probability_ui(self):
        # Choose operation
        self.prob_op.set("nCr")
        op_frame = tk.Frame(self.params_container, bg="#2C2C2E")
        op_frame.pack(fill="x", pady=2)

        op_menu = tk.OptionMenu(
            op_frame, self.prob_op,
            "nCr", "nPr", "Normal CDF (z)",
            command=self.on_prob_op_change
        )
        op_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 8, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        op_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 8, "bold"))
        op_menu.pack(side="left")

        self.prob_fields_frame = tk.Frame(self.params_container, bg="#2C2C2E")
        self.prob_fields_frame.pack(fill="x", pady=5)
        self.on_prob_op_change()

    def on_prob_op_change(self, *args):
        for w in self.prob_fields_frame.winfo_children():
            w.destroy()
        self.param_entries["prob"] = {}

        op = self.prob_op.get()
        if op in ["nCr", "nPr"]:
            # n and r inputs
            n_frame = tk.Frame(self.prob_fields_frame, bg="#2C2C2E")
            n_frame.pack(fill="x", pady=2)
            tk.Label(n_frame, text="n :", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=5, anchor="w").pack(side="left")
            n_entry = tk.Entry(n_frame, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat", width=8, insertbackground="#FFFFFF")
            n_entry.pack(side="left")
            n_entry.insert(0, "5")
            self.param_entries["prob"]["n"] = n_entry

            r_frame = tk.Frame(self.prob_fields_frame, bg="#2C2C2E")
            r_frame.pack(fill="x", pady=2)
            tk.Label(r_frame, text="r :", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=5, anchor="w").pack(side="left")
            r_entry = tk.Entry(r_frame, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat", width=8, insertbackground="#FFFFFF")
            r_entry.pack(side="left")
            r_entry.insert(0, "2")
            self.param_entries["prob"]["r"] = r_entry
        else:
            # Standard normal z input
            z_frame = tk.Frame(self.prob_fields_frame, bg="#2C2C2E")
            z_frame.pack(fill="x", pady=2)
            tk.Label(z_frame, text="z :", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=5, anchor="w").pack(side="left")
            z_entry = tk.Entry(z_frame, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat", width=8, insertbackground="#FFFFFF")
            z_entry.pack(side="left")
            z_entry.insert(0, "0.0")
            self.param_entries["prob"]["z"] = z_entry

    # --- Core Logic ---
    def calculate(self):
        t = self.stats_type.get()
        mode = self.app.mode_manager.get_mode()
        
        try:
            if t == "Descriptive Stats":
                raw_str = self.param_entries["values"].get().strip()
                if not raw_str:
                    raise InvalidExpressionError("Values list cannot be empty")
                
                # Parse list using evaluator
                vals = [self.app.evaluator.evaluate(v.strip(), mode) for v in raw_str.split(",") if v.strip()]
                # Verify all are numeric
                if not all(isinstance(v, (int, float)) for v in vals):
                    raise MathOperationError("All values must be real numbers")
                
                n = len(vals)
                if n == 0:
                    raise MathOperationError("No values to calculate")
                
                total_sum = sum(vals)
                mean = total_sum / n
                
                sorted_vals = sorted(vals)
                if n % 2 == 1:
                    median = sorted_vals[n // 2]
                else:
                    median = (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2.0
                
                min_val = sorted_vals[0]
                max_val = sorted_vals[-1]
                
                if n > 1:
                    variance = sum((x - mean)**2 for x in vals) / (n - 1)
                    std_dev = math.sqrt(variance)
                else:
                    variance = 0.0
                    std_dev = 0.0
                
                res_str = (
                    f"Count (n):    {n}\n"
                    f"Sum (Σx):     {self.app.format_result(total_sum)}\n"
                    f"Mean (x̄):     {self.app.format_result(mean)}\n"
                    f"Median:       {self.app.format_result(median)}\n"
                    f"Min:          {self.app.format_result(min_val)}\n"
                    f"Max:          {self.app.format_result(max_val)}\n"
                    f"Variance:     {self.app.format_result(variance)}\n"
                    f"Std Dev (s):  {self.app.format_result(std_dev)}"
                )
                self.show_result(res_str)
                self.draw_histogram(vals, min_val, max_val)

            elif t == "Linear Regression":
                x_str = self.param_entries["x_vals"].get().strip()
                y_str = self.param_entries["y_vals"].get().strip()
                if not x_str or not y_str:
                    raise InvalidExpressionError("Datasets cannot be empty")
                
                x_vals = [self.app.evaluator.evaluate(v.strip(), mode) for v in x_str.split(",") if v.strip()]
                y_vals = [self.app.evaluator.evaluate(v.strip(), mode) for v in y_str.split(",") if v.strip()]
                
                if len(x_vals) != len(y_vals):
                    raise MathOperationError("X and Y datasets must be of equal size")
                
                n = len(x_vals)
                if n < 2:
                    raise MathOperationError("At least 2 points are required for regression")

                if not all(isinstance(v, (int, float)) for v in x_vals) or not all(isinstance(v, (int, float)) for v in y_vals):
                    raise MathOperationError("All coordinates must be real numbers")

                x_mean = sum(x_vals) / n
                y_mean = sum(y_vals) / n

                num = sum((x_vals[i] - x_mean) * (y_vals[i] - y_mean) for i in range(n))
                den = sum((x_vals[i] - x_mean)**2 for i in range(n))
                
                if abs(den) < 1e-13:
                    raise MathOperationError("X values are constant; slope is vertical (undefined)")
                
                slope = num / den
                intercept = y_mean - slope * x_mean

                # Correlation r
                ss_xx = den
                ss_yy = sum((y_vals[i] - y_mean)**2 for i in range(n))
                if ss_xx * ss_yy > 0:
                    r = num / math.sqrt(ss_xx * ss_yy)
                else:
                    r = 0.0

                sign = "+" if intercept >= 0 else "-"
                abs_int = abs(intercept)
                res_str = (
                    f"Slope (m):      {self.app.format_result(slope)}\n"
                    f"Intercept (c):  {self.app.format_result(intercept)}\n"
                    f"Equation:       y = {self.app.format_result(slope)}*x {sign} {self.app.format_result(abs_int)}\n"
                    f"Correlation r:  {self.app.format_result(r)}"
                )
                self.show_result(res_str)
                self.draw_scatter(x_vals, y_vals, slope, intercept)

            elif t == "Probability Helpers":
                op = self.prob_op.get()
                if op in ["nCr", "nPr"]:
                    n = int(self.app.evaluator.evaluate(self.param_entries["prob"]["n"].get().strip(), mode))
                    r = int(self.app.evaluator.evaluate(self.param_entries["prob"]["r"].get().strip(), mode))
                    
                    if n < 0 or r < 0:
                        raise MathOperationError("n and r must be non-negative integers")
                    if r > n:
                        raise MathOperationError("r cannot be greater than n")
                    
                    if op == "nCr":
                        # n! / (r! (n-r)!)
                        res = math.comb(n, r)
                        self.show_result(f"Combinations ({n} C {r}) =\n\n{res}")
                    else:
                        # n! / (n-r)!
                        res = math.perm(n, r)
                        self.show_result(f"Permutations ({n} P {r}) =\n\n{res}")
                else:
                    z = self.app.evaluator.evaluate(self.param_entries["prob"]["z"].get().strip(), mode)
                    if isinstance(z, complex):
                        z = z.real
                    # Normal CDF
                    res = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
                    self.show_result(f"Normal CDF ({z}) =\n\n{self.app.format_result(res)}")
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    # -------------------------------------------------------------------------
    # Visual Chart Drawing Helpers
    # -------------------------------------------------------------------------
    def draw_histogram(self, vals, min_val, max_val):
        self.chart_canvas.delete("all")
        W = self.chart_canvas.winfo_width()
        H = self.chart_canvas.winfo_height()
        if W <= 1: W = 260
        if H <= 1: H = 140

        # Title
        self.chart_canvas.create_text(
            W // 2, 12, text="Value Distribution Histogram", fill="#8E8E93",
            font=("Segoe UI", 9, "bold")
        )

        n = len(vals)
        if n == 0:
            return

        # Divide into 5 bins
        num_bins = 5
        if max_val == min_val:
            bins = [n]
            bin_edges = [min_val, min_val + 1.0]
        else:
            bin_width = (max_val - min_val) / num_bins
            bins = [0] * num_bins
            bin_edges = [min_val + i * bin_width for i in range(num_bins + 1)]
            for v in vals:
                idx = int((v - min_val) / bin_width)
                if idx >= num_bins:
                    idx = num_bins - 1
                bins[idx] += 1

        max_count = max(bins) if bins else 1

        # Layout boundaries
        x0, y0 = 35, 25
        x1, y1 = W - 15, H - 25

        # Draw axis lines
        self.chart_canvas.create_line(x0, y0, x0, y1, fill="#555558", width=1)
        self.chart_canvas.create_line(x0, y1, x1, y1, fill="#555558", width=1)

        # Draw bars
        num_bars = len(bins)
        bar_w = (x1 - x0) / num_bars
        for i in range(num_bars):
            count = bins[i]
            bar_h = (y1 - y0) * (count / max_count)
            bx0 = x0 + i * bar_w + 3
            bx1 = x0 + (i + 1) * bar_w - 3
            by0 = y1 - bar_h
            by1 = y1

            if count > 0:
                self.chart_canvas.create_rectangle(
                    bx0, by0, bx1, by1, fill="#30D158", outline="#FFFFFF", width=1
                )
                # Count text on top of bar
                self.chart_canvas.create_text(
                    (bx0 + bx1) // 2, max(y0, by0 - 8), text=str(count), fill="#D1D1D6",
                    font=("Segoe UI", 7, "bold")
                )

            # Bin labels
            lbl = f"{bin_edges[i]:.2g}"
            self.chart_canvas.create_text(
                bx0 + 2, y1 + 10, text=lbl, fill="#8E8E93",
                font=("Consolas", 7), anchor="nw"
            )

        # Last label edge
        self.chart_canvas.create_text(
            x1 - 10, y1 + 10, text=f"{bin_edges[-1]:.2g}", fill="#8E8E93",
            font=("Consolas", 7), anchor="n"
        )

    def draw_scatter(self, x_vals, y_vals, slope, intercept):
        self.chart_canvas.delete("all")
        W = self.chart_canvas.winfo_width()
        H = self.chart_canvas.winfo_height()
        if W <= 1: W = 260
        if H <= 1: H = 140

        # Title
        self.chart_canvas.create_text(
            W // 2, 12, text="Regression Scatter Plot", fill="#8E8E93",
            font=("Segoe UI", 9, "bold")
        )

        xmin, xmax = min(x_vals), max(x_vals)
        ymin, ymax = min(y_vals), max(y_vals)

        # Pad bounds to prevent division by zero / edge overlap
        x_margin = (xmax - xmin) * 0.15 or 1.0
        y_margin = (ymax - ymin) * 0.15 or 1.0
        xmin, xmax = xmin - x_margin, xmax + x_margin
        ymin, ymax = ymin - y_margin, ymax + y_margin

        # Layout boundaries
        x0, y0 = 35, 25
        x1, y1 = W - 15, H - 25

        def to_px(x):
            return x0 + (x - xmin) / (xmax - xmin) * (x1 - x0)
        def to_py(y):
            return y1 - (y - ymin) / (ymax - ymin) * (y1 - y0)

        # Draw axis lines
        self.chart_canvas.create_line(x0, y0, x0, y1, fill="#555558", width=1)
        self.chart_canvas.create_line(x0, y1, x1, y1, fill="#555558", width=1)

        # Ticks & Labels
        # X label min/max
        self.chart_canvas.create_text(x0, y1 + 10, text=f"{xmin:.2g}", fill="#8E8E93", font=("Consolas", 7), anchor="n")
        self.chart_canvas.create_text(x1, y1 + 10, text=f"{xmax:.2g}", fill="#8E8E93", font=("Consolas", 7), anchor="n")
        # Y label min/max
        self.chart_canvas.create_text(x0 - 5, y1, text=f"{ymin:.2g}", fill="#8E8E93", font=("Consolas", 7), anchor="e")
        self.chart_canvas.create_text(x0 - 5, y0, text=f"{ymax:.2g}", fill="#8E8E93", font=("Consolas", 7), anchor="e")

        # Plot regression line
        px_start, py_start = to_px(xmin), to_py(slope * xmin + intercept)
        px_end, py_end = to_px(xmax), to_py(slope * xmax + intercept)
        # Clip Y values to grid boundary
        py_start_clip = max(y0, min(y1, py_start))
        py_end_clip = max(y0, min(y1, py_end))

        self.chart_canvas.create_line(
            px_start, py_start_clip, px_end, py_end_clip, fill="#FF9500", width=2
        )

        # Plot data points
        for i in range(len(x_vals)):
            px = to_px(x_vals[i])
            py = to_py(y_vals[i])
            self.chart_canvas.create_oval(
                px - 4, py - 4, px + 4, py + 4, fill="#30D158", outline="#FFFFFF", width=1
            )
