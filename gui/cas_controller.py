"""
Controller for the CAS (Computer Algebra System) tab.
Provides symbolic differentiation and algebraic expression simplification.
"""

import tkinter as tk
from core.symbolic import differentiate
from utils.error_handler import handle_error

class CASController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.setup_ui()

    def setup_ui(self):
        # Main container with padding
        container = tk.Frame(self.tab_frame, bg="#2C2C2E")
        container.pack(fill="both", expand=True, padx=15, pady=15)

        # Title/Description
        desc_label = tk.Label(
            container, text="Symbolic Differentiation Tool:",
            fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 10, "bold"), anchor="w"
        )
        desc_label.pack(fill="x", pady=(0, 10))

        # Expression input
        expr_frame = tk.Frame(container, bg="#2C2C2E")
        expr_frame.pack(fill="x", pady=5)
        
        tk.Label(
            expr_frame, text="f(x) = ", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")
        
        self.expr_entry = tk.Entry(
            expr_frame, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 10, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF"
        )
        self.expr_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.expr_entry.insert(0, "x^3 + 3*x^2 + 5")

        # Variable input
        var_frame = tk.Frame(container, bg="#2C2C2E")
        var_frame.pack(fill="x", pady=5)
        
        tk.Label(
            var_frame, text="With respect to variable: ", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")
        
        self.var_entry = tk.Entry(
            var_frame, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF", width=6, justify="center"
        )
        self.var_entry.pack(side="left", padx=(5, 0))
        self.var_entry.insert(0, "x")

        # Differentiate button
        diff_btn = tk.Button(
            container, text="Differentiate Symbolically", bg="#FF9500", fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"), bd=0, relief="flat", height=2,
            command=self.run_differentiation
        )
        diff_btn.pack(fill="x", pady=10)

        # Output displays
        out_lbl = tk.Label(
            container, text="Resulting Derivative f'(x):", fg="#8E8E93", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), anchor="w"
        )
        out_lbl.pack(fill="x", pady=(10, 2))

        self.result_text = tk.Text(
            container, bg="#1C1C1E", fg="#30D158",
            font=("Consolas", 10, "bold"), height=8, bd=0, highlightthickness=0,
            padx=10, pady=10
        )
        self.result_text.pack(fill="both", expand=True)
        self.result_text.config(state="disabled")

    def show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def run_differentiation(self):
        expr = self.expr_entry.get().strip()
        var = self.var_entry.get().strip()
        
        if not expr:
            self.show_result("Error: Expression cannot be empty")
            return
        if not var:
            self.show_result("Error: Variable name cannot be empty")
            return
            
        try:
            # We first expand custom variables/functions if registered
            parsed_expr = expr
            if hasattr(self.app, "evaluator") and hasattr(self.app.evaluator, "parser"):
                # Preprocess using existing calculator parser rules
                custom_functions = getattr(self.app, "custom_functions", None)
                parsed_expr = self.app.evaluator.parser.parse(expr, custom_functions)
                
            res_str = differentiate(parsed_expr, var)
            self.show_result(f"d/d{var} ({expr}) =\n\n{res_str}")
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")
