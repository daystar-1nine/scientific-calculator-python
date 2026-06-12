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

        self.on_type_change()

    def on_type_change(self, *args):
        # Clear params container
        for w in self.params_container.winfo_children():
            w.destroy()
        self.param_entries = {}

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
