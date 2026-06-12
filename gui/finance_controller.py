"""
Controller for the Financial Calculator tab.
"""

import math
import tkinter as tk
from utils.error_handler import handle_error, MathOperationError, InvalidExpressionError

class FinanceController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.pmt_type = tk.StringVar(value="END")  # END or BEGIN
        self.entries = {}

        self.setup_ui()

    def setup_ui(self):
        # Scrollable container for the finance panel
        scrollbar = tk.Scrollbar(self.tab_frame)
        scrollbar.pack(side="right", fill="y")

        canvas = tk.Canvas(self.tab_frame, bg="#2C2C2E", bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)

        self.scroll_frame = tk.Frame(canvas, bg="#2C2C2E")
        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Force inner frame width to match canvas width on resize
        canvas.bind('<Configure>', lambda event: canvas.itemconfig(canvas_window, width=event.width))
        canvas_window = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # 1. TVM Solver Frame
        tvm_frame = tk.LabelFrame(
            self.scroll_frame, text="Time Value of Money (TVM)", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), padx=5, pady=5
        )
        tvm_frame.pack(fill="x", padx=10, pady=5)

        fields = [
            ("N (Periods)", "N"),
            ("I/Y (Interest %/Yr)", "I"),
            ("PV (Present Value)", "PV"),
            ("PMT (Payment)", "PMT"),
            ("FV (Future Value)", "FV")
        ]

        self.entries = {}
        for label, key in fields:
            row = tk.Frame(tvm_frame, bg="#2C2C2E")
            row.pack(fill="x", pady=2)
            
            tk.Label(row, text=label, fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 8, "bold"), width=15, anchor="w").pack(side="left")
            
            entry = tk.Entry(row, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat", insertbackground="#FFFFFF")
            entry.pack(side="left", fill="x", expand=True, padx=5)
            entry.insert(0, "0")
            self.entries[key] = entry

            btn = tk.Button(
                row, text="Solve", bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 8, "bold"),
                bd=0, relief="flat", padx=8, pady=2, command=lambda k=key: self.solve_tvm(k)
            )
            btn.pack(side="right")

        # Payment Type Radio Buttons
        type_row = tk.Frame(tvm_frame, bg="#2C2C2E")
        type_row.pack(fill="x", pady=4)
        tk.Label(type_row, text="Payment Type:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 8, "bold"), width=15, anchor="w").pack(side="left")
        
        tk.Radiobutton(type_row, text="End (Ordinary)", variable=self.pmt_type, value="END", bg="#2C2C2E", fg="#FFFFFF", selectcolor="#2C2C2E", font=("Segoe UI", 8)).pack(side="left", padx=5)
        tk.Radiobutton(type_row, text="Begin (Due)", variable=self.pmt_type, value="BEGIN", bg="#2C2C2E", fg="#FFFFFF", selectcolor="#2C2C2E", font=("Segoe UI", 8)).pack(side="left")

        # 2. Amortization Scheduler Frame
        amort_frame = tk.LabelFrame(
            self.scroll_frame, text="Amortization Schedule", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), padx=5, pady=5
        )
        amort_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(
            amort_frame, text="Generate Schedule from PV, I/Y, N", bg="#30D158", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1, command=self.generate_amort
        ).pack(fill="x", pady=2)

        # 3. Results Readout Display
        res_label = tk.Label(
            self.scroll_frame, text="Finance Results / Schedule:", fg="#8E8E93", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), anchor="w"
        )
        res_label.pack(fill="x", padx=10, pady=(5, 2))

        self.result_text = tk.Text(
            self.scroll_frame, bg="#1C1C1E", fg="#30D158",
            font=("Consolas", 9, "bold"), height=10, bd=0, highlightthickness=0,
            padx=10, pady=10
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.result_text.config(state="disabled")

    def show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def get_values(self):
        vals = {}
        mode = self.app.mode_manager.get_mode()
        for k, entry in self.entries.items():
            s = entry.get().strip()
            val = self.app.evaluator.evaluate(s, mode)
            if isinstance(val, complex):
                val = val.real
            vals[k] = val
        return vals

    # --- TVM Math Solver ---
    def solve_tvm(self, solve_var):
        try:
            vals = self.get_values()
            p = 1 if self.pmt_type.get() == "BEGIN" else 0

            N = vals["N"]
            I = vals["I"]
            PV = vals["PV"]
            PMT = vals["PMT"]
            FV = vals["FV"]

            # TVM Equation:
            # If r = 0: PV + PMT * N + FV = 0
            # If r != 0: PV * (1+r)^N + PMT * ((1+r)^N - 1)/r * (1 + r*p) + FV = 0
            # We find the value that matches the solve_var

            if solve_var == "FV":
                r = I / 100.0
                if abs(r) < 1e-12:
                    res = -(PV + PMT * N)
                else:
                    k = 1.0 + r * p
                    res = -(PV * (1.0 + r)**N + PMT * (((1.0 + r)**N - 1.0) / r) * k)
                self.entries["FV"].delete(0, tk.END)
                self.entries["FV"].insert(0, f"{res:.6g}")
                self.show_result(f"Solved FV:\nFV = {self.app.format_result(res)}")

            elif solve_var == "PV":
                r = I / 100.0
                if abs(r) < 1e-12:
                    res = -(FV + PMT * N)
                else:
                    k = 1.0 + r * p
                    res = -(FV + PMT * (((1.0 + r)**N - 1.0) / r) * k) / ((1.0 + r)**N)
                self.entries["PV"].delete(0, tk.END)
                self.entries["PV"].insert(0, f"{res:.6g}")
                self.show_result(f"Solved PV:\nPV = {self.app.format_result(res)}")

            elif solve_var == "PMT":
                r = I / 100.0
                if abs(r) < 1e-12:
                    if abs(N) < 1e-12:
                        raise MathOperationError("Periods N cannot be zero")
                    res = -(PV + FV) / N
                else:
                    k = 1.0 + r * p
                    den = (((1.0 + r)**N - 1.0) / r) * k
                    if abs(den) < 1e-13:
                        raise MathOperationError("Annuity payment factor is zero")
                    res = -(PV * (1.0 + r)**N + FV) / den
                self.entries["PMT"].delete(0, tk.END)
                self.entries["PMT"].insert(0, f"{res:.6g}")
                self.show_result(f"Solved PMT:\nPMT = {self.app.format_result(res)}")

            elif solve_var == "N":
                # Solve N numerically
                r = I / 100.0
                
                # Check target equation: f(n) = LHS - RHS
                def tvm_eq(n):
                    if abs(r) < 1e-12:
                        return PV + PMT * n + FV
                    k = 1.0 + r * p
                    return PV * (1.0 + r)**n + PMT * (((1.0 + r)**n - 1.0) / r) * k + FV

                # Binary search for N
                low, high = 0.0, 1000.0
                success = False
                for _ in range(100):
                    mid = (low + high) / 2.0
                    f_mid = tvm_eq(mid)
                    f_low = tvm_eq(low)
                    
                    if abs(f_mid) < 1e-10:
                        success = True
                        low = mid
                        break
                    
                    if (f_mid > 0) == (f_low > 0):
                        low = mid
                    else:
                        high = mid
                
                res = low
                self.entries["N"].delete(0, tk.END)
                self.entries["N"].insert(0, f"{res:.6g}")
                self.show_result(f"Solved N:\nN = {self.app.format_result(res)}")

            elif solve_var == "I":
                # Solve interest rate r numerically
                # TVM function with respect to r
                def tvm_eq(r_val):
                    if abs(r_val) < 1e-12:
                        return PV + PMT * N + FV
                    k = 1.0 + r_val * p
                    return PV * (1.0 + r_val)**N + PMT * (((1.0 + r_val)**N - 1.0) / r_val) * k + FV

                # Binary search for interest rate r in [-0.99, 10.0]
                low, high = -0.99, 10.0
                success = False
                for _ in range(100):
                    mid = (low + high) / 2.0
                    f_mid = tvm_eq(mid)
                    f_low = tvm_eq(low)
                    
                    if abs(f_mid) < 1e-10:
                        success = True
                        low = mid
                        break
                    
                    if (f_mid > 0) == (f_low > 0):
                        low = mid
                    else:
                        high = mid
                        
                res = low * 100.0
                self.entries["I"].delete(0, tk.END)
                self.entries["I"].insert(0, f"{res:.6g}")
                self.show_result(f"Solved Interest Rate:\nI/Y = {self.app.format_result(res)}%")

        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    # --- Amortization Scheduler ---
    def generate_amort(self):
        try:
            vals = self.get_values()
            PV = vals["PV"]
            I = vals["I"]
            N = int(vals["N"])

            if PV <= 0 or I < 0 or N <= 0:
                raise MathOperationError("Present Value (PV), Interest Rate (I), and Periods (N) must be positive values")

            # Monthly payment compounding (r = annual / 12 / 100)
            r = I / 12.0 / 100.0
            
            if abs(r) < 1e-12:
                pmt = PV / N
            else:
                pmt = PV * (r * (1.0 + r)**N) / (((1.0 + r)**N) - 1.0)

            lines = [
                f"Loan Amount:  ${PV:,.2f}",
                f"Rate:         {I}% / Yr (monthly r: {r*100:.4f}%)",
                f"Term:         {N} months",
                f"Monthly PMT:  ${pmt:,.2f}",
                "-" * 60,
                f"{'Month':<6} | {'Payment':<10} | {'Interest':<10} | {'Principal':<10} | {'Balance':<12}",
                "-" * 60
            ]

            balance = PV
            for m in range(1, N + 1):
                interest = balance * r
                principal = pmt - interest
                balance = balance - principal
                # Force balance to zero at last month to hide rounding remnants
                if m == N or balance < 0:
                    balance = 0.0
                    
                lines.append(
                    f"{m:<6} | ${pmt:10,.2f} | ${interest:10,.2f} | ${principal:10,.2f} | ${balance:12,.2f}"
                )

            self.show_result("\n".join(lines))
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")
