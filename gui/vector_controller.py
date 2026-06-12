"""
Controller for the Vector Mathematics tab.
"""

import math
import tkinter as tk
from utils.error_handler import handle_error, MathOperationError, InvalidExpressionError

class VectorController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.vector_dim = tk.StringVar(value="3D Vector")
        self.entries_a = {}
        self.entries_b = {}

        self.setup_ui()

    def setup_ui(self):
        # 1. Dimension selector
        dim_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        dim_frame.pack(fill="x", padx=10, pady=5)

        dim_label = tk.Label(
            dim_frame, text="Dimension:", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 10, "bold")
        )
        dim_label.pack(side="left", padx=(0, 10))

        dim_menu = tk.OptionMenu(
            dim_frame,
            self.vector_dim,
            "2D Vector", "3D Vector",
            command=self.update_dimension
        )
        dim_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        dim_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        dim_menu.pack(side="left")

        # 2. Vector Grids Frame
        self.grids_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        self.grids_frame.pack(fill="x", padx=10, pady=5)

        # 3. Operations Buttons Frame
        ops_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        ops_frame.pack(fill="x", padx=10, pady=5)

        # Row 1 ops
        r1 = tk.Frame(ops_frame, bg="#2C2C2E")
        r1.pack(fill="x", pady=2)
        tk.Button(r1, text="Magnitude", bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1, command=self.run_magnitude).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(r1, text="Dot Product", bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1, command=self.run_dot).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(r1, text="Cross Product", bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1, command=self.run_cross).pack(side="left", fill="x", expand=True, padx=2)

        # Row 2 ops
        r2 = tk.Frame(ops_frame, bg="#2C2C2E")
        r2.pack(fill="x", pady=2)
        tk.Button(r2, text="A + B", bg="#30D158", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1, command=lambda: self.run_arithmetic("add")).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(r2, text="A - B", bg="#30D158", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1, command=lambda: self.run_arithmetic("sub")).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(r2, text="Angle (A, B)", bg="#30D158", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1, command=self.run_angle).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(r2, text="Proj (A onto B)", bg="#30D158", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1, command=self.run_projection).pack(side="left", fill="x", expand=True, padx=2)

        # 4. Result display
        res_label = tk.Label(
            self.tab_frame, text="Result:", fg="#8E8E93", bg="#2C2C2E",
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

        self.update_dimension()

    def update_dimension(self, *args):
        # Clear grids frame
        for w in self.grids_frame.winfo_children():
            w.destroy()

        self.entries_a = {}
        self.entries_b = {}

        is_3d = self.vector_dim.get() == "3D Vector"
        axes = ["x", "y", "z"] if is_3d else ["x", "y"]

        # Vector A Frame
        frame_a = tk.LabelFrame(
            self.grids_frame, text="Vector A", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 8, "bold"), labelanchor="n"
        )
        frame_a.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Vector B Frame
        frame_b = tk.LabelFrame(
            self.grids_frame, text="Vector B", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 8, "bold"), labelanchor="n"
        )
        frame_b.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        for i, axis in enumerate(axes):
            # A element
            fa = tk.Frame(frame_a, bg="#2C2C2E")
            fa.pack(fill="x", padx=5, pady=3)
            tk.Label(fa, text=f"{axis}:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 8, "bold"), width=2).pack(side="left")
            entry_a = tk.Entry(fa, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat", justify="center", insertbackground="#FFFFFF")
            entry_a.pack(side="left", fill="x", expand=True)
            entry_a.insert(0, "0")
            self.entries_a[axis] = entry_a

            # B element
            fb = tk.Frame(frame_b, bg="#2C2C2E")
            fb.pack(fill="x", padx=5, pady=3)
            tk.Label(fb, text=f"{axis}:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 8, "bold"), width=2).pack(side="left")
            entry_b = tk.Entry(fb, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat", justify="center", insertbackground="#FFFFFF")
            entry_b.pack(side="left", fill="x", expand=True)
            entry_b.insert(0, "0")
            self.entries_b[axis] = entry_b

    def show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def parse_vector(self, entries):
        vec = []
        mode = self.app.mode_manager.get_mode()
        # Fallback to 0 if z doesn't exist
        for axis in ["x", "y", "z"]:
            if axis in entries:
                val_str = entries[axis].get().strip()
                if not val_str:
                    val_str = "0"
                val = self.app.evaluator.evaluate(val_str, mode)
                if isinstance(val, complex):
                    val = val.real
                vec.append(val)
            else:
                vec.append(0.0)
        return vec

    def format_vector(self, vec):
        is_3d = self.vector_dim.get() == "3D Vector"
        lim = 3 if is_3d else 2
        content = ", ".join(self.app.format_result(x) for x in vec[:lim])
        return f"[ {content} ]"

    def magnitude_val(self, vec):
        return math.sqrt(sum(x**2 for x in vec))

    # --- Operation Runs ---
    def run_magnitude(self):
        try:
            A = self.parse_vector(self.entries_a)
            B = self.parse_vector(self.entries_b)
            
            mag_a = self.magnitude_val(A)
            mag_b = self.magnitude_val(B)
            
            res_str = (
                f"|A| = {self.app.format_result(mag_a)}\n"
                f"|B| = {self.app.format_result(mag_b)}"
            )
            self.show_result(res_str)
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    def run_dot(self):
        try:
            A = self.parse_vector(self.entries_a)
            B = self.parse_vector(self.entries_b)
            
            dot = sum(A[i] * B[i] for i in range(3))
            self.show_result(f"A . B = {self.app.format_result(dot)}")
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    def run_cross(self):
        try:
            A = self.parse_vector(self.entries_a)
            B = self.parse_vector(self.entries_b)
            
            # Cross Product: [y1*z2 - z1*y2, z1*x2 - x1*z2, x1*y2 - y1*x2]
            cross = [
                A[1]*B[2] - A[2]*B[1],
                A[2]*B[0] - A[0]*B[2],
                A[0]*B[1] - A[1]*B[0]
            ]
            self.show_result(f"A x B = {self.format_vector(cross)}")
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    def run_arithmetic(self, op):
        try:
            A = self.parse_vector(self.entries_a)
            B = self.parse_vector(self.entries_b)
            
            if op == "add":
                res = [A[i] + B[i] for i in range(3)]
                self.show_result(f"A + B = {self.format_vector(res)}")
            else:
                res = [A[i] - B[i] for i in range(3)]
                self.show_result(f"A - B = {self.format_vector(res)}")
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    def run_angle(self):
        try:
            A = self.parse_vector(self.entries_a)
            B = self.parse_vector(self.entries_b)
            
            mag_a = self.magnitude_val(A)
            mag_b = self.magnitude_val(B)
            
            if abs(mag_a) < 1e-13 or abs(mag_b) < 1e-13:
                raise MathOperationError("Cannot calculate angle with zero vector")
                
            dot = sum(A[i] * B[i] for i in range(3))
            cos_theta = max(-1.0, min(1.0, dot / (mag_a * mag_b)))
            theta_rad = math.acos(cos_theta)
            
            mode = self.app.mode_manager.get_mode()
            if mode == "DEG":
                theta = math.degrees(theta_rad)
                self.show_result(f"Angle(A, B) =\n{self.app.format_result(theta)}°")
            else:
                self.show_result(f"Angle(A, B) =\n{self.app.format_result(theta_rad)} rad")
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    def run_projection(self):
        try:
            A = self.parse_vector(self.entries_a)
            B = self.parse_vector(self.entries_b)
            
            mag_b = self.magnitude_val(B)
            if abs(mag_b) < 1e-13:
                raise MathOperationError("Cannot project onto zero vector B")
                
            dot = sum(A[i] * B[i] for i in range(3))
            scalar_proj = dot / mag_b
            vec_proj = [(dot / (mag_b**2)) * B[i] for i in range(3)]
            
            res_str = (
                f"Scalar Proj: {self.app.format_result(scalar_proj)}\n"
                f"Vector Proj: {self.format_vector(vec_proj)}"
            )
            self.show_result(res_str)
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")
