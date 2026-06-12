"""
Controller for the Equation Solver tab.
"""

import math
import tkinter as tk
from utils.error_handler import handle_error, MathOperationError, InvalidExpressionError

class SolverController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.solver_type = tk.StringVar(value="Root Finder")
        self.sub_type = tk.StringVar(value="2 Variables")  # Used for linear size or polynomial degree
        self.param_entries = {}

        self.setup_ui()

    def setup_ui(self):
        # 1. Main Solver type selector
        select_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        select_frame.pack(fill="x", padx=10, pady=5)

        type_label = tk.Label(
            select_frame, text="Type:", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 10, "bold")
        )
        type_label.pack(side="left", padx=(0, 10))

        type_menu = tk.OptionMenu(
            select_frame,
            self.solver_type,
            "Root Finder", "Linear Systems", "Polynomials",
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

        # 3. Solve Button
        solve_btn = tk.Button(
            self.tab_frame, text="Solve Equation", bg="#30D158", fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"), bd=0, relief="flat", height=2,
            command=self.solve
        )
        solve_btn.pack(fill="x", padx=10, pady=5)

        # 4. Result label display
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

        self.on_type_change()

    def on_type_change(self, *args):
        # Clear params container
        for w in self.params_container.winfo_children():
            w.destroy()
        self.param_entries = {}

        t = self.solver_type.get()
        if t == "Root Finder":
            self.setup_root_finder_ui()
        elif t == "Linear Systems":
            self.setup_linear_ui()
        elif t == "Polynomials":
            self.setup_polynomial_ui()

    def show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    # --- UI Builders ---
    def setup_root_finder_ui(self):
        # f(x) = 0
        f_frame = tk.Frame(self.params_container, bg="#2C2C2E")
        f_frame.pack(fill="x", pady=3)
        tk.Label(f_frame, text="f(x) = ", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 10, "bold")).pack(side="left")
        
        self.param_entries["expr"] = tk.Entry(
            f_frame, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 10, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF"
        )
        self.param_entries["expr"].pack(side="left", fill="x", expand=True)
        self.param_entries["expr"].insert(0, "x^2 - 4")

        # Guess x0
        guess_frame = tk.Frame(self.params_container, bg="#2C2C2E")
        guess_frame.pack(fill="x", pady=3)
        tk.Label(guess_frame, text="Initial Guess x0 = ", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold")).pack(side="left")
        
        self.param_entries["guess"] = tk.Entry(
            guess_frame, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF", width=8
        )
        self.param_entries["guess"].pack(side="left")
        self.param_entries["guess"].insert(0, "1.0")

    def setup_linear_ui(self):
        # Size menu selector
        self.sub_type.set("2 Variables")
        size_frame = tk.Frame(self.params_container, bg="#2C2C2E")
        size_frame.pack(fill="x", pady=2)

        size_menu = tk.OptionMenu(
            size_frame, self.sub_type,
            "2 Variables", "3 Variables",
            command=self.on_linear_size_change
        )
        size_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 8, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        size_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 8, "bold"))
        size_menu.pack(side="left")

        self.linear_grid_frame = tk.Frame(self.params_container, bg="#2C2C2E")
        self.linear_grid_frame.pack(fill="x", pady=5)
        self.on_linear_size_change()

    def on_linear_size_change(self, *args):
        for w in self.linear_grid_frame.winfo_children():
            w.destroy()
        self.param_entries["grid"] = []

        is_3d = self.sub_type.get() == "3 Variables"
        rows = 3 if is_3d else 2
        cols = 4 if is_3d else 3

        # Grid column labels
        labels_row = tk.Frame(self.linear_grid_frame, bg="#2C2C2E")
        labels_row.pack(fill="x")
        if is_3d:
            headers = ["x coeff", "y coeff", "z coeff", "const"]
        else:
            headers = ["x coeff", "y coeff", "const"]
            
        for h in headers:
            tk.Label(
                labels_row, text=h, fg="#8E8E93", bg="#2C2C2E",
                font=("Segoe UI", 7, "bold"), width=7, anchor="center"
            ).pack(side="left", fill="x", expand=True)

        for r in range(rows):
            row_frame = tk.Frame(self.linear_grid_frame, bg="#2C2C2E")
            row_frame.pack(fill="x", pady=2)
            row_entries = []
            for c in range(cols):
                entry = tk.Entry(
                    row_frame, bg="#1C1C1E", fg="#FFFFFF", width=6,
                    font=("Segoe UI", 9, "bold"), bd=2, relief="flat",
                    justify="center", insertbackground="#FFFFFF"
                )
                entry.pack(side="left", fill="x", expand=True, padx=2)
                entry.insert(0, "0")
                row_entries.append(entry)
            self.param_entries["grid"].append(row_entries)

    def setup_polynomial_ui(self):
        self.sub_type.set("Quadratic (2nd)")
        deg_frame = tk.Frame(self.params_container, bg="#2C2C2E")
        deg_frame.pack(fill="x", pady=2)

        deg_menu = tk.OptionMenu(
            deg_frame, self.sub_type,
            "Quadratic (2nd)", "Cubic (3rd)",
            command=self.on_poly_degree_change
        )
        deg_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 8, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        deg_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 8, "bold"))
        deg_menu.pack(side="left")

        self.poly_coeffs_frame = tk.Frame(self.params_container, bg="#2C2C2E")
        self.poly_coeffs_frame.pack(fill="x", pady=5)
        self.on_poly_degree_change()

    def on_poly_degree_change(self, *args):
        for w in self.poly_coeffs_frame.winfo_children():
            w.destroy()
        self.param_entries["poly"] = {}

        is_cubic = self.sub_type.get() == "Cubic (3rd)"
        coeffs = ["a", "b", "c", "d"] if is_cubic else ["a", "b", "c"]

        for c in coeffs:
            c_frame = tk.Frame(self.poly_coeffs_frame, bg="#2C2C2E")
            c_frame.pack(fill="x", pady=2)
            lbl = f"{c} * x^{len(coeffs)-1 - coeffs.index(c)} :" if c != coeffs[-1] else f"{c} :"
            tk.Label(c_frame, text=lbl, fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=10, anchor="w").pack(side="left")
            entry = tk.Entry(
                c_frame, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
                bd=3, relief="flat", insertbackground="#FFFFFF", width=8
            )
            entry.pack(side="left", fill="x", expand=True)
            entry.insert(0, "1" if c == "a" else "0")
            self.param_entries["poly"][c] = entry

    # --- Solver Core Logic ---
    def solve(self):
        t = self.solver_type.get()
        mode = self.app.mode_manager.get_mode()
        
        try:
            if t == "Root Finder":
                expr = self.param_entries["expr"].get().strip()
                guess_str = self.param_entries["guess"].get().strip()
                if not expr:
                    raise InvalidExpressionError("Expression cannot be empty")
                x0 = self.app.evaluator.evaluate(guess_str, mode)
                if isinstance(x0, complex):
                    x0 = x0.real
                
                # Newton-Raphson Solver
                root = self.newton_root_solve(expr, x0, mode)
                self.show_result(f"Root found:\nx = {self.app.format_result(root)}")

            elif t == "Linear Systems":
                grid = []
                for row_entries in self.param_entries["grid"]:
                    row = [self.app.evaluator.evaluate(e.get().strip(), mode) for e in row_entries]
                    grid.append(row)
                
                if self.sub_type.get() == "2 Variables":
                    # 2x2 solver using Cramer's Rule
                    a1, b1, c1 = grid[0]
                    a2, b2, c2 = grid[1]
                    D = a1 * b2 - b1 * a2
                    if abs(D) < 1e-13:
                        raise MathOperationError("System coefficient matrix is singular (no unique solution)")
                    Dx = c1 * b2 - b1 * c2
                    Dy = a1 * c2 - c1 * a2
                    x = Dx / D
                    y = Dy / D
                    self.show_result(f"Solution:\nx = {self.app.format_result(x)}\ny = {self.app.format_result(y)}")
                else:
                    # 3x3 solver using Cramer's Rule
                    a1, b1, c1, d1 = grid[0]
                    a2, b2, c2, d2 = grid[1]
                    a3, b3, c3, d3 = grid[2]
                    
                    # Determinant helper
                    def det3x3(m):
                        return (m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1]) -
                                m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0]) +
                                m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0]))
                    
                    D = det3x3([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]])
                    if abs(D) < 1e-13:
                        raise MathOperationError("System coefficient matrix is singular (no unique solution)")
                        
                    Dx = det3x3([[d1, b1, c1], [d2, b2, c2], [d3, b3, c3]])
                    Dy = det3x3([[a1, d1, c1], [a2, d2, c2], [a3, d3, c3]])
                    Dz = det3x3([[a1, b1, d1], [a2, b2, d2], [a3, b3, d3]])
                    
                    x = Dx / D
                    y = Dy / D
                    z = Dz / D
                    self.show_result(f"Solution:\nx = {self.app.format_result(x)}\ny = {self.app.format_result(y)}\nz = {self.app.format_result(z)}")

            elif t == "Polynomials":
                coeffs = self.param_entries["poly"]
                a = self.app.evaluator.evaluate(coeffs["a"].get().strip(), mode)
                b = self.app.evaluator.evaluate(coeffs["b"].get().strip(), mode)
                c = self.app.evaluator.evaluate(coeffs["c"].get().strip(), mode)
                
                if abs(a) < 1e-13:
                    raise MathOperationError("Leading coefficient 'a' cannot be zero")

                if self.sub_type.get() == "Quadratic (2nd)":
                    disc = b**2 - 4*a*c
                    # Use complex sqrt
                    import cmath
                    root1 = (-b + cmath.sqrt(disc)) / (2*a)
                    root2 = (-b - cmath.sqrt(disc)) / (2*a)
                    
                    # Convert to float if imaginary is zero
                    if abs(root1.imag) < 1e-13: root1 = root1.real
                    if abs(root2.imag) < 1e-13: root2 = root2.real

                    self.show_result(f"Roots:\nx1 = {self.app.format_result(root1)}\nx2 = {self.app.format_result(root2)}")
                else:
                    d = self.app.evaluator.evaluate(coeffs["d"].get().strip(), mode)
                    # Solve cubic analytically/numerically
                    roots = self.solve_cubic(a, b, c, d, mode)
                    res_lines = [f"x{i+1} = {self.app.format_result(r)}" for i, r in enumerate(roots)]
                    self.show_result("Roots:\n" + "\n".join(res_lines))
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    def newton_root_solve(self, expr, x0, mode):
        x = x0
        h = 1e-6
        for _ in range(100):
            try:
                # f(x)
                y = self.app.evaluator.evaluate(expr, mode, variables={"x": x})
                # f(x + h)
                y_h = self.app.evaluator.evaluate(expr, mode, variables={"x": x + h})
                # f(x - h)
                y_mh = self.app.evaluator.evaluate(expr, mode, variables={"x": x - h})
                
                dy = (y_h - y_mh) / (2 * h)
                if abs(dy) < 1e-14:
                    break
                
                dx = y / dy
                x = x - dx
                if abs(dx) < 1e-12:
                    return x
            except Exception:
                raise MathOperationError("Root finder evaluation failed or hit undefined region")
        return x

    def solve_cubic(self, a, b, c, d, mode):
        # We find one real root using Newton's method
        def f(t):
            return a*t**3 + b*t**2 + c*t + d
        def df(t):
            return 3*a*t**2 + 2*b*t + c
        
        # Simple starting point search
        x = 0.0
        for _ in range(100):
            fx = f(x)
            dfx = df(x)
            if abs(dfx) < 1e-13:
                dfx = 1e-13
            dx = fx / dfx
            x -= dx
            if abs(dx) < 1e-12:
                break
        
        real_root = x
        
        # Synthetic division to get quadratic: a x^2 + b' x + c' = 0
        # a * x^3 + b * x^2 + c * x + d = (x - r)(a * x^2 + b' * x + c')
        # where:
        bp = b + a * real_root
        cp = c + bp * real_root
        
        # Solve quadratic: a * x^2 + bp * x + cp = 0
        disc = bp**2 - 4*a*cp
        import cmath
        r2 = (-bp + cmath.sqrt(disc)) / (2*a)
        r3 = (-bp - cmath.sqrt(disc)) / (2*a)
        
        if abs(r2.imag) < 1e-13: r2 = r2.real
        if abs(r3.imag) < 1e-13: r3 = r3.real
        
        return [real_root, r2, r3]
