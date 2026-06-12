"""
Controller for the Complex Number Converter.
Provides Rectangular <-> Polar conversion and visual phasor rendering.
"""

import math
import tkinter as tk
from utils.error_handler import handle_error, MathOperationError, InvalidExpressionError

class ComplexConverterController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.setup_ui()

    def setup_ui(self):
        # Main container with two columns: left for inputs/buttons, right for phasor diagram/results
        main_container = tk.Frame(self.tab_frame, bg="#2C2C2E")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_container, bg="#2C2C2E")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = tk.Frame(main_container, bg="#2C2C2E")
        right_frame.pack(side="right", fill="both", expand=True)

        # --- LEFT PANE: Inputs ---
        # 1. Rectangular to Polar Group
        rect_group = tk.LabelFrame(
            left_frame, text="Rectangular to Polar", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 10, "bold"), padx=10, pady=10
        )
        rect_group.pack(fill="x", pady=(0, 10))

        # Real Part
        r_row = tk.Frame(rect_group, bg="#2C2C2E")
        r_row.pack(fill="x", pady=2)
        tk.Label(r_row, text="Real (x):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=10, anchor="w").pack(side="left")
        self.real_entry = tk.Entry(
            r_row, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF"
        )
        self.real_entry.pack(side="left", fill="x", expand=True)
        self.real_entry.insert(0, "3.0")

        # Imaginary Part
        i_row = tk.Frame(rect_group, bg="#2C2C2E")
        i_row.pack(fill="x", pady=2)
        tk.Label(i_row, text="Imag (y):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=10, anchor="w").pack(side="left")
        self.imag_entry = tk.Entry(
            i_row, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF"
        )
        self.imag_entry.pack(side="left", fill="x", expand=True)
        self.imag_entry.insert(0, "4.0")

        # Convert Button
        to_polar_btn = tk.Button(
            rect_group, text="Convert to Polar", bg="#FF9500", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1,
            command=self.convert_to_polar
        )
        to_polar_btn.pack(fill="x", pady=(10, 0))

        # 2. Polar to Rectangular Group
        polar_group = tk.LabelFrame(
            left_frame, text="Polar to Rectangular", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 10, "bold"), padx=10, pady=10
        )
        polar_group.pack(fill="x", pady=(0, 10))

        # Magnitude
        mag_row = tk.Frame(polar_group, bg="#2C2C2E")
        mag_row.pack(fill="x", pady=2)
        tk.Label(mag_row, text="Mag (r):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=10, anchor="w").pack(side="left")
        self.mag_entry = tk.Entry(
            mag_row, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF"
        )
        self.mag_entry.pack(side="left", fill="x", expand=True)
        self.mag_entry.insert(0, "5.0")

        # Angle
        ang_row = tk.Frame(polar_group, bg="#2C2C2E")
        ang_row.pack(fill="x", pady=2)
        tk.Label(ang_row, text="Angle (θ):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=10, anchor="w").pack(side="left")
        self.ang_entry = tk.Entry(
            ang_row, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=3, relief="flat", insertbackground="#FFFFFF"
        )
        self.ang_entry.pack(side="left", fill="x", expand=True)
        self.ang_entry.insert(0, "53.13")

        # Convert Button
        to_rect_btn = tk.Button(
            polar_group, text="Convert to Rectangular", bg="#FF9500", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1,
            command=self.convert_to_rectangular
        )
        to_rect_btn.pack(fill="x", pady=(10, 0))

        # --- RIGHT PANE: Phasor & Results ---
        # Result Display (Text widget)
        res_label = tk.Label(
            right_frame, text="Converted Results:", fg="#8E8E93", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), anchor="w"
        )
        res_label.pack(fill="x", pady=(0, 2))

        self.result_text = tk.Text(
            right_frame, bg="#1C1C1E", fg="#30D158",
            font=("Consolas", 10, "bold"), height=4, bd=0, highlightthickness=0,
            padx=10, pady=5
        )
        self.result_text.pack(fill="x", pady=(0, 10))
        self.result_text.config(state="disabled")

        # Phasor Canvas
        canvas_label = tk.Label(
            right_frame, text="Phasor Diagram:", fg="#8E8E93", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), anchor="w"
        )
        canvas_label.pack(fill="x", pady=(0, 2))

        self.canvas = tk.Canvas(
            right_frame, bg="#1C1C1E", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.draw_phasor())

        # Initialize values
        self.current_real = 3.0
        self.current_imag = 4.0

    def show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def convert_to_polar(self):
        try:
            mode = self.app.mode_manager.get_mode()
            real_val = self.app.evaluator.evaluate(self.real_entry.get().strip(), mode)
            imag_val = self.app.evaluator.evaluate(self.imag_entry.get().strip(), mode)
            
            real = float(real_val.real if isinstance(real_val, complex) else real_val)
            imag = float(imag_val.real if isinstance(imag_val, complex) else imag_val)
            
            r = math.hypot(real, imag)
            theta_rad = math.atan2(imag, real)
            
            if mode == "DEG":
                theta = math.degrees(theta_rad)
                angle_unit = "°"
            else:
                theta = theta_rad
                angle_unit = " rad"

            self.current_real = real
            self.current_imag = imag

            result_str = (
                f"Rectangular: {real} + {imag}i\n"
                f"Polar: {self.app.format_result(r)} ∠ {self.app.format_result(theta)}{angle_unit}\n"
                f"Exponential: {self.app.format_result(r)} * e^(i * {self.app.format_result(theta_rad)} rad)"
            )
            self.show_result(result_str)
            self.draw_phasor()
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    def convert_to_rectangular(self):
        try:
            mode = self.app.mode_manager.get_mode()
            r_val = self.app.evaluator.evaluate(self.mag_entry.get().strip(), mode)
            ang_val = self.app.evaluator.evaluate(self.ang_entry.get().strip(), mode)
            
            r = float(r_val.real if isinstance(r_val, complex) else r_val)
            ang = float(ang_val.real if isinstance(ang_val, complex) else ang_val)
            
            if mode == "DEG":
                theta_rad = math.radians(ang)
                angle_unit = "°"
                theta = ang
            else:
                theta_rad = ang
                angle_unit = " rad"
                theta = ang

            real = r * math.cos(theta_rad)
            imag = r * math.sin(theta_rad)

            self.current_real = real
            self.current_imag = imag

            result_str = (
                f"Polar: {r} ∠ {ang}{angle_unit}\n"
                f"Rectangular: {self.app.format_result(real)} + {self.app.format_result(imag)}i\n"
                f"Exponential: {self.app.format_result(r)} * e^(i * {self.app.format_result(theta_rad)} rad)"
            )
            self.show_result(result_str)
            self.draw_phasor()
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    def draw_phasor(self):
        self.canvas.delete("all")
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        if W < 10 or H < 10:
            return

        cx, cy = W / 2, H / 2
        # Draw axes
        self.canvas.create_line(10, cy, W - 10, cy, fill="#48484A", width=1)
        self.canvas.create_line(cx, 10, cx, H - 10, fill="#48484A", width=1)
        
        # Draw some grid concentric circles
        max_r = min(cx, cy) - 20
        for radius in [max_r * 0.3, max_r * 0.6, max_r]:
            self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, outline="#3A3A3C", width=1, dash=(2, 2))

        # Vector coordinates scaling
        r = math.hypot(self.current_real, self.current_imag)
        if r > 1e-12:
            scale = (max_r * 0.8) / r
            vx = cx + self.current_real * scale
            vy = cy - self.current_imag * scale
            
            # Draw vector arrow
            self.canvas.create_line(cx, cy, vx, vy, fill="#FF9500", width=3, arrow="last", arrowshape=(10, 12, 4))
            self.canvas.create_oval(vx - 4, vy - 4, vx + 4, vy + 4, fill="#30D158", outline="#FFFFFF", width=1)
            
            mode = self.app.mode_manager.get_mode()
            theta_rad = math.atan2(self.current_imag, self.current_real)
            theta_deg = math.degrees(theta_rad)
            ang = theta_deg if mode == "DEG" else theta_rad
            unit = "°" if mode == "DEG" else " rad"
            
            label_text = f"{self.app.format_result(r)} ∠ {self.app.format_result(ang)}{unit}"
            tx = vx + 10 if vx >= cx else vx - 60
            ty = vy - 10 if vy <= cy else vy + 10
            self.canvas.create_text(tx, ty, text=label_text, fill="#FFFFFF", font=("Segoe UI", 8, "bold"), anchor="w")
