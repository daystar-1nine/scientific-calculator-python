"""
Controller for the 3D Grapher tab.
Pure Tkinter implementation of interactive 3D wireframe plot.
"""

import math
import tkinter as tk
from utils.error_handler import handle_error

class Graph3DController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        # Rotation angles (degrees)
        self.yaw = 30.0
        self.pitch = 60.0

        # UI variables
        self.expr_var = tk.StringVar(value="sin(x) * cos(y)")
        self.xmin_var = tk.StringVar(value="-5")
        self.xmax_var = tk.StringVar(value="5")
        self.ymin_var = tk.StringVar(value="-5")
        self.ymax_var = tk.StringVar(value="5")

        self.setup_ui()

    def setup_ui(self):
        # 1. Inputs Frame
        inputs_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        inputs_frame.pack(fill="x", padx=10, pady=5)

        # Formula input
        formula_row = tk.Frame(inputs_frame, bg="#2C2C2E")
        formula_row.pack(fill="x", pady=2)
        tk.Label(formula_row, text="z = f(x,y):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold")).pack(side="left")
        self.expr_entry = tk.Entry(formula_row, textvariable=self.expr_var, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat")
        self.expr_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.expr_entry.bind("<Return>", lambda e: self.plot_3d())

        # Ranges Row
        ranges_row = tk.Frame(inputs_frame, bg="#2C2C2E")
        ranges_row.pack(fill="x", pady=2)
        
        tk.Label(ranges_row, text="x bounds:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 8)).pack(side="left")
        self.xmin_entry = tk.Entry(ranges_row, textvariable=self.xmin_var, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 8), bd=1, relief="flat", width=5)
        self.xmin_entry.pack(side="left", padx=2)
        self.xmax_entry = tk.Entry(ranges_row, textvariable=self.xmax_var, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 8), bd=1, relief="flat", width=5)
        self.xmax_entry.pack(side="left", padx=(2, 10))

        tk.Label(ranges_row, text="y bounds:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 8)).pack(side="left")
        self.ymin_entry = tk.Entry(ranges_row, textvariable=self.ymin_var, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 8), bd=1, relief="flat", width=5)
        self.ymin_entry.pack(side="left", padx=2)
        self.ymax_entry = tk.Entry(ranges_row, textvariable=self.ymax_var, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 8), bd=1, relief="flat", width=5)
        self.ymax_entry.pack(side="left", padx=2)

        # Plot Button
        calc_btn = tk.Button(
            self.tab_frame, text="Render 3D Graph", bg="#FF9500", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=1,
            command=self.plot_3d
        )
        calc_btn.pack(fill="x", padx=10, pady=(0, 5))

        # Canvas
        self.canvas = tk.Canvas(self.tab_frame, bg="#1C1C1E", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        # Help footer label
        self.footer = tk.Label(
            self.tab_frame, text="Drag mouse on canvas to rotate plot",
            fg="#8E8E93", bg="#2C2C2E", font=("Segoe UI", 8, "italic")
        )
        self.footer.pack(fill="x", pady=(0, 5))

        # Bindings for mouse interaction rotation
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def on_click(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        
        self.yaw += dx * 0.5
        self.pitch -= dy * 0.5  # Invert vertical pitch change
        
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        
        self.plot_3d()

    def plot_3d(self):
        self.canvas.delete("all")
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        if W <= 1: W = 280
        if H <= 1: H = 220

        expr = self.expr_var.get().strip()
        if not expr:
            return

        try:
            xmin = float(self.xmin_var.get().strip())
            xmax = float(self.xmax_var.get().strip())
            ymin = float(self.ymin_var.get().strip())
            ymax = float(self.ymax_var.get().strip())
        except ValueError:
            return

        # Calculate grid values
        grid_size = 20
        x_step = (xmax - xmin) / (grid_size - 1)
        y_step = (ymax - ymin) / (grid_size - 1)

        mode = self.app.mode_manager.get_mode()
        
        # Calculate matrix of coordinates
        points = []
        min_z = float('inf')
        max_z = float('-inf')

        for i in range(grid_size):
            row_points = []
            x_val = xmin + i * x_step
            for j in range(grid_size):
                y_val = ymin + j * y_step
                try:
                    # Evaluate z coordinate
                    z_val = self.app.evaluator.evaluate(expr, mode, variables={"x": x_val, "y": y_val})
                    if isinstance(z_val, complex):
                        z_val = z_val.real
                    if not math.isfinite(z_val):
                        z_val = 0.0
                except Exception:
                    z_val = 0.0
                
                min_z = min(min_z, z_val)
                max_z = max(max_z, z_val)
                row_points.append((x_val, y_val, z_val))
            points.append(row_points)

        z_range = max_z - min_z
        if abs(z_range) < 1e-9:
            z_range = 1.0

        # Rotate and project all vertices
        projected = []
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        # Scale coordinates to fits canvas boundaries
        # Normalize x, y in [-1, 1], z in [-0.6, 0.6]
        norm_scale_x = 2.0 / (xmax - xmin) if xmax != xmin else 1.0
        norm_scale_y = 2.0 / (ymax - ymin) if ymax != ymin else 1.0
        norm_scale_z = 1.2 / z_range

        cx = W / 2
        cy = H / 2
        view_scale = min(W, H) * 0.35

        for i in range(grid_size):
            row_projected = []
            for j in range(grid_size):
                x, y, z = points[i][j]
                
                # Normalize values
                nx = (x - (xmin + xmax)/2.0) * norm_scale_x
                ny = (y - (ymin + ymax)/2.0) * norm_scale_y
                nz = (z - (min_z + max_z)/2.0) * norm_scale_z

                # Rotate around Z axis (yaw)
                rx1 = nx * math.cos(yaw_rad) - ny * math.sin(yaw_rad)
                ry1 = nx * math.sin(yaw_rad) + ny * math.cos(yaw_rad)
                rz1 = nz

                # Rotate around X axis (pitch)
                rx2 = rx1
                ry2 = ry1 * math.cos(pitch_rad) - rz1 * math.sin(pitch_rad)
                rz2 = ry1 * math.sin(pitch_rad) + rz1 * math.cos(pitch_rad)

                # Parallel orthographic projection
                screen_x = cx + rx2 * view_scale
                screen_y = cy - ry2 * view_scale
                row_projected.append((screen_x, screen_y))
            projected.append(row_projected)

        # Draw mesh lines
        for i in range(grid_size):
            for j in range(grid_size):
                # Connect row lines
                if j < grid_size - 1:
                    x0, y0 = projected[i][j]
                    x1, y1 = projected[i][j+1]
                    self.canvas.create_line(x0, y0, x1, y1, fill="#30D158", width=1)
                
                # Connect column lines
                if i < grid_size - 1:
                    x0, y0 = projected[i][j]
                    x1, y1 = projected[i+1][j]
                    self.canvas.create_line(x0, y0, x1, y1, fill="#FF9500", width=1)
