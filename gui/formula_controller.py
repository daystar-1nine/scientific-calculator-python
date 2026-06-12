"""
Controller for the Formula Library & Custom Solver tab.
"""

import re
import tkinter as tk
from utils.error_handler import handle_error, MathOperationError, InvalidExpressionError

class FormulaController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.formula_preset = tk.StringVar(value="Kinetic Energy")
        self.target_var = tk.StringVar()
        self.var_entries = {}
        
        self.presets = {
            "Kinetic Energy": "KE = 0.5 * m * v^2",
            "Ohm's Law": "V = I * R",
            "Einstein Relation": "E = m * c^2",
            "Ideal Gas Law": "P * V = n * R * T",
            "Custom Formula": "F = m * a"
        }

        self.setup_ui()

    def setup_ui(self):
        # 1. Preset Selector
        preset_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        preset_frame.pack(fill="x", padx=10, pady=5)

        preset_lbl = tk.Label(
            preset_frame, text="Formula:", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 10, "bold")
        )
        preset_lbl.pack(side="left", padx=(0, 10))

        preset_menu = tk.OptionMenu(
            preset_frame,
            self.formula_preset,
            *self.presets.keys(),
            command=self.on_preset_change
        )
        preset_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        preset_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        preset_menu.pack(side="left", fill="x", expand=True)

        # 2. Equation text entry
        eq_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        eq_frame.pack(fill="x", padx=10, pady=5)

        self.eq_entry = tk.Entry(
            eq_frame, bg="#1C1C1E", fg="#FFFFFF", font=("Consolas", 10, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF"
        )
        self.eq_entry.pack(fill="x")
        
        # Bind key release on equation entry to parse variables for Custom Formula
        self.eq_entry.bind("<KeyRelease>", self.on_equation_edit)

        # 3. Target Variable Selector
        target_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        target_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            target_frame, text="Solve For:", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(0, 10))

        self.target_menu = tk.OptionMenu(target_frame, self.target_var, "")
        self.target_menu.config(
            bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        self.target_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        self.target_menu.pack(side="left")

        # 4. Variables Inputs Grid Container
        self.vars_container = tk.Frame(self.tab_frame, bg="#2C2C2E")
        self.vars_container.pack(fill="x", padx=10, pady=5)

        # 5. Solve button
        solve_btn = tk.Button(
            self.tab_frame, text="Solve Variable", bg="#30D158", fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"), bd=0, relief="flat", height=2,
            command=self.solve
        )
        solve_btn.pack(fill="x", padx=10, pady=5)

        # 6. Result display
        res_label = tk.Label(
            self.tab_frame, text="Solution:", fg="#8E8E93", bg="#2C2C2E",
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

        self.on_preset_change()

    def show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def on_preset_change(self, *args):
        preset = self.formula_preset.get()
        eq = self.presets[preset]
        
        self.eq_entry.config(state="normal")
        self.eq_entry.delete(0, tk.END)
        self.eq_entry.insert(0, eq)
        
        if preset != "Custom Formula":
            self.eq_entry.config(state="disabled")
        
        self.rebuild_variables_ui()

    def on_equation_edit(self, event):
        if self.formula_preset.get() == "Custom Formula":
            self.rebuild_variables_ui()

    def extract_variables(self, eq_str):
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', eq_str)
        # Filter out standard math functions, constants, and operators
        reserved = {
            'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
            'exp', 'log', 'ln', 'sqrt', 'factorial', 'diff', 'integrate', 'pi', 'e',
            'PI', 'E'
        }
        return sorted(list({w for w in words if w not in reserved}))

    def rebuild_variables_ui(self):
        eq_str = self.eq_entry.get().strip()
        vars_list = self.extract_variables(eq_str)

        # Update Target Variable Option Menu
        self.target_menu["menu"].delete(0, tk.END)
        for var in vars_list:
            self.target_menu["menu"].add_command(
                label=var,
                command=lambda v=var: self.on_target_var_change(v)
            )

        if vars_list:
            if self.target_var.get() not in vars_list:
                self.target_var.set(vars_list[0])
            self.build_inputs_grid(vars_list)
        else:
            self.target_var.set("")
            for w in self.vars_container.winfo_children():
                w.destroy()

    def on_target_var_change(self, var):
        self.target_var.set(var)
        eq_str = self.eq_entry.get().strip()
        vars_list = self.extract_variables(eq_str)
        self.build_inputs_grid(vars_list)

    def build_inputs_grid(self, vars_list):
        for w in self.vars_container.winfo_children():
            w.destroy()

        self.var_entries = {}
        target = self.target_var.get()
        
        for var in vars_list:
            if var == target:
                continue

            f = tk.Frame(self.vars_container, bg="#2C2C2E")
            f.pack(fill="x", pady=2)

            tk.Label(
                f, text=f"{var} :", fg="#FFFFFF", bg="#2C2C2E",
                font=("Segoe UI", 9, "bold"), width=8, anchor="w"
            ).pack(side="left")

            entry = tk.Entry(
                f, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
                bd=2, relief="flat", insertbackground="#FFFFFF"
            )
            entry.pack(side="left", fill="x", expand=True)
            entry.insert(0, "0")
            self.var_entries[var] = entry

    # --- Core Solver logic ---
    def solve(self):
        eq_str = self.eq_entry.get().strip()
        if "=" not in eq_str:
            self.show_result("Error: Equation must contain '='")
            return

        target = self.target_var.get()
        if not target:
            self.show_result("Error: No target variable selected")
            return

        mode = self.app.mode_manager.get_mode()
        lhs_str, rhs_str = eq_str.split("=", 1)

        # Parse other variables values
        other_vars = {}
        try:
            for var, entry in self.var_entries.items():
                val_str = entry.get().strip()
                val = self.app.evaluator.evaluate(val_str, mode)
                if isinstance(val, complex):
                    val = val.real
                other_vars[var] = val
        except Exception as e:
            self.show_result(f"Error parsing variables:\n{handle_error(e)}")
            return

        # Newton-Raphson Solver
        def f(t):
            vars_dict = {**other_vars, target: t}
            # Also support lowercase/uppercase variant for safety
            vars_dict[target.lower()] = t
            vars_dict[target.upper()] = t
            
            lhs_val = self.app.evaluator.evaluate(lhs_str, mode, variables=vars_dict)
            rhs_val = self.app.evaluator.evaluate(rhs_str, mode, variables=vars_dict)
            
            if isinstance(lhs_val, complex): lhs_val = lhs_val.real
            if isinstance(rhs_val, complex): rhs_val = rhs_val.real
            return lhs_val - rhs_val

        # Solve f(t) = 0
        t = 1.0  # Initial guess
        h = 1e-5
        success = False

        for _ in range(100):
            try:
                y = f(t)
                if abs(y) < 1e-12:
                    success = True
                    break
                
                # Numeric derivative
                dy = (f(t + h) - f(t - h)) / (2 * h)
                if abs(dy) < 1e-14:
                    t += 0.5  # shift guess
                    continue
                
                dt = y / dy
                t -= dt
                if abs(dt) < 1e-12:
                    success = True
                    break
            except Exception:
                # If evaluation fails, shift guess and retry
                t += 1.0

        if success:
            self.show_result(f"Solved for {target}:\n{target} = {self.app.format_result(t)}")
        else:
            self.show_result("Error:\nFailed to converge to a solution.")
