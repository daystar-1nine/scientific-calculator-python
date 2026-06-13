"""
Controller for the Hypothesis Testing tab.
Supports Z-Tests, T-Tests, Two-Sample T-Tests, and Chi-Square Goodness-of-Fit tests.
"""

import math
import tkinter as tk
from utils.error_handler import handle_error, MathOperationError

# --- Numerical distribution helpers ---
def erf(x):
    # Abramowitz and Stegun formula 7.1.26
    sign = 1 if x >= 0 else -1
    x = abs(x)
    p = 0.3275911
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y
    
def std_normal_cdf(z):
    return 0.5 * (1.0 + erf(z / math.sqrt(2.0)))

def std_normal_ppf(p):
    # Inverse CDF approximation using Winitzki formula
    if p <= 0.0 or p >= 1.0:
        return 0.0
    # Transform p to symmetric range [-0.5, 0.5]
    x = p - 0.5
    if abs(x) < 1e-12:
        return 0.0
    sign = 1 if x >= 0 else -1
    # Simple Winitzki approximation of erf^-1
    a = 0.147
    term1 = 2.0 / (math.pi * a) + math.log(1.0 - 4.0 * x * x) / 2.0
    inner = term1 * term1 - math.log(1.0 - 4.0 * x * x) / a
    erf_inv = sign * math.sqrt(math.sqrt(inner) - term1)
    return erf_inv * math.sqrt(2.0)

def student_t_cdf(t, df):
    # Hill's approximation of Student-t CDF using standard Normal CDF
    if df <= 0:
        return 0.5
    z = t * (1.0 - 1.0 / (4.0 * df)) / math.sqrt(1.0 + t * t / (2.0 * df))
    return std_normal_cdf(z)

def student_t_ppf(p, df):
    # Approximate student-t critical values using Normal critical value adjustment
    z = std_normal_ppf(p)
    if df <= 0:
        return z
    # Cornish-Fisher style correction
    return z + (z**3 + z) / (4.0 * df)

def chi_square_cdf(chi_sq, df):
    # Wilson-Hilferty transformation
    if chi_sq <= 0 or df <= 0:
        return 0.0
    z = (((chi_sq / df) ** (1.0/3.0)) - (1.0 - 2.0 / (9.0 * df))) / math.sqrt(2.0 / (9.0 * df))
    return std_normal_cdf(z)

def chi_square_ppf(p, df):
    # Wilson-Hilferty inverse approximation
    z = std_normal_ppf(p)
    if df <= 0:
        return 0.0
    inner = 1.0 - 2.0 / (9.0 * df) + z * math.sqrt(2.0 / (9.0 * df))
    if inner < 0:
        return 0.0
    return df * (inner ** 3)


class HypothesisTestingController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.test_type = tk.StringVar(value="1-Sample Z-Test")
        self.tail_type = tk.StringVar(value="Two-Tailed (≠)")
        self.param_entries = {}

        self.setup_ui()

    def setup_ui(self):
        # 1. Main Controls Frame
        select_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        select_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(select_frame, text="Test:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold")).pack(side="left")
        test_menu = tk.OptionMenu(
            select_frame, self.test_type,
            "1-Sample Z-Test", "1-Sample T-Test", "2-Sample T-Test", "Chi-Square Test",
            command=self.on_test_change
        )
        test_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        test_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        test_menu.pack(side="left", padx=5)

        tk.Label(select_frame, text="Tail:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(10, 0))
        tail_menu = tk.OptionMenu(select_frame, self.tail_type, "Two-Tailed (≠)", "Greater Than (>)", "Less Than (<)")
        tail_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        tail_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        tail_menu.pack(side="left", padx=5)

        # Alpha (Significance level)
        tk.Label(select_frame, text="α:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(10, 0))
        self.alpha_entry = tk.Entry(
            select_frame, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=2, relief="flat", width=5, justify="center", insertbackground="#FFFFFF"
        )
        self.alpha_entry.pack(side="left", padx=5)
        self.alpha_entry.insert(0, "0.05")

        # 2. Parameters Container Frame
        self.params_container = tk.Frame(self.tab_frame, bg="#2C2C2E")
        self.params_container.pack(fill="x", padx=10, pady=5)

        # 3. Calculate Button
        calc_btn = tk.Button(
            self.tab_frame, text="Perform Hypothesis Test", bg="#FF9500", fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"), bd=0, relief="flat", height=2,
            command=self.run_test
        )
        calc_btn.pack(fill="x", padx=10, pady=5)

        # 4. Result text display
        res_lbl = tk.Label(
            self.tab_frame, text="Analysis Report:", fg="#8E8E93", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), anchor="w"
        )
        res_lbl.pack(fill="x", padx=10, pady=(10, 2))

        self.result_text = tk.Text(
            self.tab_frame, bg="#1C1C1E", fg="#30D158",
            font=("Consolas", 10, "bold"), height=8, bd=0, highlightthickness=0,
            padx=10, pady=10
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.result_text.config(state="disabled")

        self.on_test_change()

    def on_test_change(self, *args):
        # Clear params container
        for w in self.params_container.winfo_children():
            w.destroy()
        self.param_entries = {}

        t = self.test_type.get()
        if t in ["1-Sample Z-Test", "1-Sample T-Test"]:
            # Single sample parameters
            row1 = tk.Frame(self.params_container, bg="#2C2C2E")
            row1.pack(fill="x", pady=2)
            
            tk.Label(row1, text="Mean (x̄):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=10, anchor="w").pack(side="left")
            self.param_entries["mean"] = tk.Entry(row1, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat")
            self.param_entries["mean"].pack(side="left", fill="x", expand=True, padx=(0, 10))
            self.param_entries["mean"].insert(0, "5.2")

            tk.Label(row1, text="Std Dev (s):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=10, anchor="w").pack(side="left")
            self.param_entries["stddev"] = tk.Entry(row1, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat")
            self.param_entries["stddev"].pack(side="left", fill="x", expand=True)
            self.param_entries["stddev"].insert(0, "0.5")

            row2 = tk.Frame(self.params_container, bg="#2C2C2E")
            row2.pack(fill="x", pady=2)
            
            tk.Label(row2, text="Size (n):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=10, anchor="w").pack(side="left")
            self.param_entries["size"] = tk.Entry(row2, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat")
            self.param_entries["size"].pack(side="left", fill="x", expand=True, padx=(0, 10))
            self.param_entries["size"].insert(0, "25")

            tk.Label(row2, text="Null μ0:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=10, anchor="w").pack(side="left")
            self.param_entries["null"] = tk.Entry(row2, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat")
            self.param_entries["null"].pack(side="left", fill="x", expand=True)
            self.param_entries["null"].insert(0, "5.0")

        elif t == "2-Sample T-Test":
            # Two sample parameters
            row1 = tk.Frame(self.params_container, bg="#2C2C2E")
            row1.pack(fill="x", pady=2)
            tk.Label(row1, text="Mean 1:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 8, "bold"), width=8, anchor="w").pack(side="left")
            self.param_entries["mean1"] = tk.Entry(row1, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 8, "bold"), bd=2, relief="flat", width=6)
            self.param_entries["mean1"].pack(side="left", fill="x", expand=True, padx=2)
            self.param_entries["mean1"].insert(0, "12.1")

            tk.Label(row1, text="Std Dev 1:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 8, "bold"), width=10, anchor="w").pack(side="left")
            self.param_entries["sd1"] = tk.Entry(row1, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 8, "bold"), bd=2, relief="flat", width=6)
            self.param_entries["sd1"].pack(side="left", fill="x", expand=True, padx=2)
            self.param_entries["sd1"].insert(0, "1.2")

            tk.Label(row1, text="Size 1 (n1):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 8, "bold"), width=10, anchor="w").pack(side="left")
            self.param_entries["n1"] = tk.Entry(row1, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 8, "bold"), bd=2, relief="flat", width=6)
            self.param_entries["n1"].pack(side="left", fill="x", expand=True, padx=2)
            self.param_entries["n1"].insert(0, "20")

            row2 = tk.Frame(self.params_container, bg="#2C2C2E")
            row2.pack(fill="x", pady=2)
            tk.Label(row2, text="Mean 2:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 8, "bold"), width=8, anchor="w").pack(side="left")
            self.param_entries["mean2"] = tk.Entry(row2, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 8, "bold"), bd=2, relief="flat", width=6)
            self.param_entries["mean2"].pack(side="left", fill="x", expand=True, padx=2)
            self.param_entries["mean2"].insert(0, "11.5")

            tk.Label(row2, text="Std Dev 2:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 8, "bold"), width=10, anchor="w").pack(side="left")
            self.param_entries["sd2"] = tk.Entry(row2, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 8, "bold"), bd=2, relief="flat", width=6)
            self.param_entries["sd2"].pack(side="left", fill="x", expand=True, padx=2)
            self.param_entries["sd2"].insert(0, "1.5")

            tk.Label(row2, text="Size 2 (n2):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 8, "bold"), width=10, anchor="w").pack(side="left")
            self.param_entries["n2"] = tk.Entry(row2, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 8, "bold"), bd=2, relief="flat", width=6)
            self.param_entries["n2"].pack(side="left", fill="x", expand=True, padx=2)
            self.param_entries["n2"].insert(0, "22")

        elif t == "Chi-Square Test":
            row1 = tk.Frame(self.params_container, bg="#2C2C2E")
            row1.pack(fill="x", pady=2)
            tk.Label(row1, text="Observed Freqs:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=15, anchor="w").pack(side="left")
            self.param_entries["obs"] = tk.Entry(row1, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat")
            self.param_entries["obs"].pack(side="left", fill="x", expand=True)
            self.param_entries["obs"].insert(0, "10, 20, 30")

            row2 = tk.Frame(self.params_container, bg="#2C2C2E")
            row2.pack(fill="x", pady=2)
            tk.Label(row2, text="Expected Freqs:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=15, anchor="w").pack(side="left")
            self.param_entries["exp"] = tk.Entry(row2, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat")
            self.param_entries["exp"].pack(side="left", fill="x", expand=True)
            self.param_entries["exp"].insert(0, "15, 15, 30")

    def show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def run_test(self):
        t = self.test_type.get()
        mode = self.app.mode_manager.get_mode()
        
        try:
            alpha = float(self.app.evaluator.evaluate(self.alpha_entry.get().strip(), mode))
            if not (0 < alpha < 1):
                raise ValueError("Significance level α must be in range (0, 1)")
                
            tail = self.tail_type.get()
            
            if t == "1-Sample Z-Test":
                xbar = float(self.app.evaluator.evaluate(self.param_entries["mean"].get().strip(), mode))
                s = float(self.app.evaluator.evaluate(self.param_entries["stddev"].get().strip(), mode))
                n = int(self.app.evaluator.evaluate(self.param_entries["size"].get().strip(), mode))
                mu0 = float(self.app.evaluator.evaluate(self.param_entries["null"].get().strip(), mode))
                
                if s <= 0 or n <= 1:
                    raise MathOperationError("s must be > 0 and n must be > 1")
                    
                z = (xbar - mu0) / (s / math.sqrt(n))
                
                # Critical values & p-values
                if tail == "Two-Tailed (≠)":
                    cv = std_normal_ppf(1.0 - alpha / 2.0)
                    p_val = 2.0 * (1.0 - std_normal_cdf(abs(z)))
                    cv_str = f"±{self.app.format_result(cv)}"
                    reject = abs(z) > cv
                elif tail == "Greater Than (>)":
                    cv = std_normal_ppf(1.0 - alpha)
                    p_val = 1.0 - std_normal_cdf(z)
                    cv_str = f"{self.app.format_result(cv)}"
                    reject = z > cv
                else: # Less Than (<)
                    cv = -std_normal_ppf(1.0 - alpha)
                    p_val = std_normal_cdf(z)
                    cv_str = f"{self.app.format_result(cv)}"
                    reject = z < cv
                    
                conclusion = "REJECT Null Hypothesis (H0)" if reject else "FAIL TO REJECT Null Hypothesis (H0)"
                
                report = (
                    f"--- 1-Sample Z-Test Report ---\n"
                    f"Null Hypothesis H0: μ = {mu0}\n"
                    f"Alt Hypothesis H1: μ {tail.split(' ')[1]} {mu0}\n\n"
                    f"Calculated Stats:\n"
                    f"  Test Statistic z = {self.app.format_result(z)}\n"
                    f"  Critical Value   = {cv_str}\n"
                    f"  p-value          = {self.app.format_result(p_val)}\n"
                    f"  Significance α   = {alpha}\n\n"
                    f"Conclusion:\n"
                    f"  {conclusion}"
                )
                self.show_result(report)

            elif t == "1-Sample T-Test":
                xbar = float(self.app.evaluator.evaluate(self.param_entries["mean"].get().strip(), mode))
                s = float(self.app.evaluator.evaluate(self.param_entries["stddev"].get().strip(), mode))
                n = int(self.app.evaluator.evaluate(self.param_entries["size"].get().strip(), mode))
                mu0 = float(self.app.evaluator.evaluate(self.param_entries["null"].get().strip(), mode))
                
                if s <= 0 or n <= 1:
                    raise MathOperationError("s must be > 0 and n must be > 1")
                    
                df = n - 1
                t_stat = (xbar - mu0) / (s / math.sqrt(n))
                
                if tail == "Two-Tailed (≠)":
                    cv = student_t_ppf(1.0 - alpha / 2.0, df)
                    p_val = 2.0 * (1.0 - student_t_cdf(abs(t_stat), df))
                    cv_str = f"±{self.app.format_result(cv)}"
                    reject = abs(t_stat) > cv
                elif tail == "Greater Than (>)":
                    cv = student_t_ppf(1.0 - alpha, df)
                    p_val = 1.0 - student_t_cdf(t_stat, df)
                    cv_str = f"{self.app.format_result(cv)}"
                    reject = t_stat > cv
                else: # Less Than (<)
                    cv = -student_t_ppf(1.0 - alpha, df)
                    p_val = student_t_cdf(t_stat, df)
                    cv_str = f"{self.app.format_result(cv)}"
                    reject = t_stat < cv
                    
                conclusion = "REJECT Null Hypothesis (H0)" if reject else "FAIL TO REJECT Null Hypothesis (H0)"
                
                report = (
                    f"--- 1-Sample T-Test Report ---\n"
                    f"Null Hypothesis H0: μ = {mu0}\n"
                    f"Alt Hypothesis H1: μ {tail.split(' ')[1]} {mu0}\n\n"
                    f"Calculated Stats (df = {df}):\n"
                    f"  Test Statistic t = {self.app.format_result(t_stat)}\n"
                    f"  Critical Value   = {cv_str}\n"
                    f"  p-value          = {self.app.format_result(p_val)}\n"
                    f"  Significance α   = {alpha}\n\n"
                    f"Conclusion:\n"
                    f"  {conclusion}"
                )
                self.show_result(report)

            elif t == "2-Sample T-Test":
                x1 = float(self.app.evaluator.evaluate(self.param_entries["mean1"].get().strip(), mode))
                s1 = float(self.app.evaluator.evaluate(self.param_entries["sd1"].get().strip(), mode))
                n1 = int(self.app.evaluator.evaluate(self.param_entries["n1"].get().strip(), mode))
                
                x2 = float(self.app.evaluator.evaluate(self.param_entries["mean2"].get().strip(), mode))
                s2 = float(self.app.evaluator.evaluate(self.param_entries["sd2"].get().strip(), mode))
                n2 = int(self.app.evaluator.evaluate(self.param_entries["n2"].get().strip(), mode))
                
                if s1 <= 0 or s2 <= 0 or n1 <= 1 or n2 <= 1:
                    raise MathOperationError("Std Devs must be > 0 and Sample Sizes must be > 1")
                    
                # Welch's T-Test
                denom = math.sqrt((s1**2 / n1) + (s2**2 / n2))
                t_stat = (x1 - x2) / denom
                
                numerator_df = ((s1**2 / n1) + (s2**2 / n2)) ** 2
                denom_df = ((s1**2 / n1)**2 / (n1 - 1)) + ((s2**2 / n2)**2 / (n2 - 1))
                df = int(numerator_df / denom_df)
                if df < 1:
                    df = 1
                    
                if tail == "Two-Tailed (≠)":
                    cv = student_t_ppf(1.0 - alpha / 2.0, df)
                    p_val = 2.0 * (1.0 - student_t_cdf(abs(t_stat), df))
                    cv_str = f"±{self.app.format_result(cv)}"
                    reject = abs(t_stat) > cv
                elif tail == "Greater Than (>)":
                    cv = student_t_ppf(1.0 - alpha, df)
                    p_val = 1.0 - student_t_cdf(t_stat, df)
                    cv_str = f"{self.app.format_result(cv)}"
                    reject = t_stat > cv
                else: # Less Than (<)
                    cv = -student_t_ppf(1.0 - alpha, df)
                    p_val = student_t_cdf(t_stat, df)
                    cv_str = f"{self.app.format_result(cv)}"
                    reject = t_stat < cv
                    
                conclusion = "REJECT Null Hypothesis (H0)" if reject else "FAIL TO REJECT Null Hypothesis (H0)"
                
                report = (
                    f"--- 2-Sample T-Test (Welch's T-Test) ---\n"
                    f"Null Hypothesis H0: μ1 = μ2\n"
                    f"Alt Hypothesis H1: μ1 {tail.split(' ')[1]} μ2\n\n"
                    f"Calculated Stats (df = {df}):\n"
                    f"  Test Statistic t = {self.app.format_result(t_stat)}\n"
                    f"  Critical Value   = {cv_str}\n"
                    f"  p-value          = {self.app.format_result(p_val)}\n"
                    f"  Significance α   = {alpha}\n\n"
                    f"Conclusion:\n"
                    f"  {conclusion}"
                )
                self.show_result(report)

            elif t == "Chi-Square Test":
                obs_str = self.param_entries["obs"].get().strip()
                exp_str = self.param_entries["exp"].get().strip()
                
                obs = [float(self.app.evaluator.evaluate(o.strip(), mode)) for o in obs_str.split(",") if o.strip()]
                expected = [float(self.app.evaluator.evaluate(e.strip(), mode)) for e in exp_str.split(",") if e.strip()]
                
                if len(obs) != len(expected) or len(obs) <= 1:
                    raise MathOperationError("Observed and Expected lists must have same size and contain at least 2 items")
                    
                if any(e <= 0 for e in expected):
                    raise MathOperationError("All expected frequencies must be > 0")
                    
                chi_sq = sum((o - e)**2 / e for o, e in zip(obs, expected))
                df = len(obs) - 1
                
                # Chi-Square test is always one-tailed (greater than)
                cv = chi_square_ppf(1.0 - alpha, df)
                p_val = 1.0 - chi_square_cdf(chi_sq, df)
                reject = chi_sq > cv
                conclusion = "REJECT Null Hypothesis (H0)" if reject else "FAIL TO REJECT Null Hypothesis (H0)"
                
                report = (
                    f"--- Chi-Square Goodness-of-Fit Test ---\n"
                    f"Null Hypothesis H0: Observed frequencies match expected\n"
                    f"Alt Hypothesis H1: Observed frequencies do NOT match expected\n\n"
                    f"Calculated Stats (df = {df}):\n"
                    f"  Chi-Square χ²    = {self.app.format_result(chi_sq)}\n"
                    f"  Critical Value   = {self.app.format_result(cv)}\n"
                    f"  p-value          = {self.app.format_result(p_val)}\n"
                    f"  Significance α   = {alpha}\n\n"
                    f"Conclusion:\n"
                    f"  {conclusion}"
                )
                self.show_result(report)
                
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")
