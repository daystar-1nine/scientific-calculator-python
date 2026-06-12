"""
Controller for the Matrix Algebra tab.
"""

import tkinter as tk
from utils.error_handler import handle_error, MathOperationError

class MatrixController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.matrix_size = tk.StringVar(value="2x2")
        self.grid_a_entries = []
        self.grid_b_entries = []

        self.setup_ui()

    def setup_ui(self):
        # 1. Dimension selector
        dim_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        dim_frame.pack(fill="x", padx=10, pady=5)

        dim_label = tk.Label(
            dim_frame,
            text="Dimension:",
            fg="#FFFFFF",
            bg="#2C2C2E",
            font=("Segoe UI", 10, "bold")
        )
        dim_label.pack(side="left", padx=(0, 10))

        dim_menu = tk.OptionMenu(
            dim_frame,
            self.matrix_size,
            "2x2", "3x3",
            command=self.update_dimensions
        )
        dim_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        dim_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        dim_menu.pack(side="left")

        # 2. Grids Container Frame
        self.grids_container = tk.Frame(self.tab_frame, bg="#2C2C2E")
        self.grids_container.pack(fill="x", padx=10, pady=5)

        # 3. Operations Buttons Frame
        ops_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        ops_frame.pack(fill="x", padx=10, pady=5)

        # Row 1 ops
        r1_frame = tk.Frame(ops_frame, bg="#2C2C2E")
        r1_frame.pack(fill="x", pady=2)
        
        tk.Button(
            r1_frame, text="Det(A)", bg="#FF9500", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1,
            command=lambda: self.run_unary_op("det")
        ).pack(side="left", fill="x", expand=True, padx=2)

        tk.Button(
            r1_frame, text="Inv(A)", bg="#FF9500", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1,
            command=lambda: self.run_unary_op("inv")
        ).pack(side="left", fill="x", expand=True, padx=2)

        tk.Button(
            r1_frame, text="Trans(A)", bg="#FF9500", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1,
            command=lambda: self.run_unary_op("trans")
        ).pack(side="left", fill="x", expand=True, padx=2)

        # Row 2 ops
        r2_frame = tk.Frame(ops_frame, bg="#2C2C2E")
        r2_frame.pack(fill="x", pady=2)

        tk.Button(
            r2_frame, text="A + B", bg="#30D158", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1,
            command=lambda: self.run_binary_op("add")
        ).pack(side="left", fill="x", expand=True, padx=2)

        tk.Button(
            r2_frame, text="A - B", bg="#30D158", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1,
            command=lambda: self.run_binary_op("sub")
        ).pack(side="left", fill="x", expand=True, padx=2)

        tk.Button(
            r2_frame, text="A * B", bg="#30D158", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1,
            command=lambda: self.run_binary_op("mul")
        ).pack(side="left", fill="x", expand=True, padx=2)

        # 4. Result label display
        res_header = tk.Label(
            self.tab_frame, text="Result:", fg="#8E8E93", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), anchor="w"
        )
        res_header.pack(fill="x", padx=10, pady=(10, 2))

        self.result_text = tk.Text(
            self.tab_frame, bg="#1C1C1E", fg="#30D158",
            font=("Consolas", 10, "bold"), height=8, bd=0, highlightthickness=0,
            padx=10, pady=10
        )
        self.result_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.result_text.config(state="disabled")

        self.update_dimensions()

    def update_dimensions(self, *args):
        # Clear entries
        for w in self.grids_container.winfo_children():
            w.destroy()

        self.grid_a_entries = []
        self.grid_b_entries = []

        size = 2 if self.matrix_size.get() == "2x2" else 3

        # Grid A Frame
        frame_a = tk.LabelFrame(
            self.grids_container, text="Matrix A", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 8, "bold"), labelanchor="n"
        )
        frame_a.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Grid B Frame
        frame_b = tk.LabelFrame(
            self.grids_container, text="Matrix B", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 8, "bold"), labelanchor="n"
        )
        frame_b.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        for r in range(size):
            row_a = []
            row_b = []
            for c in range(size):
                entry_a = tk.Entry(
                    frame_a, bg="#1C1C1E", fg="#FFFFFF", width=5,
                    font=("Segoe UI", 9, "bold"), bd=2, relief="flat",
                    justify="center", insertbackground="#FFFFFF"
                )
                entry_a.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
                entry_a.insert(0, "0")
                row_a.append(entry_a)

                entry_b = tk.Entry(
                    frame_b, bg="#1C1C1E", fg="#FFFFFF", width=5,
                    font=("Segoe UI", 9, "bold"), bd=2, relief="flat",
                    justify="center", insertbackground="#FFFFFF"
                )
                entry_b.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
                entry_b.insert(0, "0")
                row_b.append(entry_b)
            self.grid_a_entries.append(row_a)
            self.grid_b_entries.append(row_b)

        # Configure weights for equal grid columns/rows
        for i in range(size):
            frame_a.grid_columnconfigure(i, weight=1)
            frame_a.grid_rowconfigure(i, weight=1)
            frame_b.grid_columnconfigure(i, weight=1)
            frame_b.grid_rowconfigure(i, weight=1)

    def parse_matrix(self, entries):
        matrix = []
        mode = self.app.mode_manager.get_mode()
        for r_entries in entries:
            row = []
            for entry in r_entries:
                val_str = entry.get().strip()
                if not val_str:
                    val_str = "0"
                # Evaluate using app evaluator
                val = self.app.evaluator.evaluate(val_str, mode)
                row.append(val)
            matrix.append(row)
        return matrix

    def show_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def format_matrix(self, matrix):
        lines = []
        for row in matrix:
            row_str = "  ".join(self.app.format_result(val) for val in row)
            lines.append(f"[ {row_str} ]")
        return "\n".join(lines)

    def run_unary_op(self, op):
        try:
            A = self.parse_matrix(self.grid_a_entries)
            size = len(A)
            
            if op == "det":
                res = self.determinant(A)
                self.show_result(f"Determinant(A) =\n\n{self.app.format_result(res)}")
            elif op == "trans":
                res = self.transpose(A)
                self.show_result(f"Transpose(A) =\n\n{self.format_matrix(res)}")
            elif op == "inv":
                res = self.inverse(A)
                self.show_result(f"Inverse(A) =\n\n{self.format_matrix(res)}")
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    def run_binary_op(self, op):
        try:
            A = self.parse_matrix(self.grid_a_entries)
            B = self.parse_matrix(self.grid_b_entries)
            size = len(A)

            if op == "add":
                res = [[A[r][c] + B[r][c] for c in range(size)] for r in range(size)]
                self.show_result(f"A + B =\n\n{self.format_matrix(res)}")
            elif op == "sub":
                res = [[A[r][c] - B[r][c] for c in range(size)] for r in range(size)]
                self.show_result(f"A - B =\n\n{self.format_matrix(res)}")
            elif op == "mul":
                res = []
                for r in range(size):
                    row = []
                    for c in range(size):
                        val = sum(A[r][k] * B[k][c] for k in range(size))
                        row.append(val)
                    res.append(row)
                self.show_result(f"A * B =\n\n{self.format_matrix(res)}")
        except Exception as e:
            self.show_result(f"Error:\n{handle_error(e)}")

    # Matrix Math Helpers
    def determinant(self, M):
        size = len(M)
        if size == 2:
            return M[0][0] * M[1][1] - M[0][1] * M[1][0]
        # 3x3 determinant
        a, b, c = M[0][0], M[0][1], M[0][2]
        d, e, f = M[1][0], M[1][1], M[1][2]
        g, h, i = M[2][0], M[2][1], M[2][2]
        return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

    def transpose(self, M):
        size = len(M)
        return [[M[c][r] for c in range(size)] for r in range(size)]

    def inverse(self, M):
        det = self.determinant(M)
        if abs(det) < 1e-13:
            raise MathOperationError("Matrix is singular (det = 0), cannot invert")
        
        size = len(M)
        if size == 2:
            # 2x2 inverse
            a, b = M[0][0], M[0][1]
            c, d = M[1][0], M[1][1]
            return [
                [d / det, -b / det],
                [-c / det, a / det]
            ]
        
        # 3x3 inverse using cofactor/adjugate
        # Cofactor elements
        c11 = M[1][1]*M[2][2] - M[1][2]*M[2][1]
        c12 = -(M[1][0]*M[2][2] - M[1][2]*M[2][0])
        c13 = M[1][0]*M[2][1] - M[1][1]*M[2][0]

        c21 = -(M[0][1]*M[2][2] - M[0][2]*M[2][1])
        c22 = M[0][0]*M[2][2] - M[0][2]*M[2][0]
        c23 = -(M[0][0]*M[2][1] - M[0][1]*M[2][0])

        c31 = M[0][1]*M[1][2] - M[0][2]*M[1][1]
        c32 = -(M[0][0]*M[1][2] - M[0][2]*M[1][0])
        c33 = M[0][0]*M[1][1] - M[0][1]*M[1][0]

        adj = [
            [c11, c21, c31],
            [c12, c22, c32],
            [c13, c23, c33]
        ]

        return [[adj[r][c] / det for c in range(3)] for r in range(3)]
