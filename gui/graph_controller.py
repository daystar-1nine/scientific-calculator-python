"""
Controller for the 2D Function Grapher tab with multi-function support, hover tracing, and PNG export.
"""

import math
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw

class GraphController:
    def __init__(self, app, tab_frame):
        self.app = app  # Reference to main CalculatorApp
        self.tab_frame = tab_frame

        self.graph_entries = []
        self.colors = ["#FF9500", "#0A84FF", "#30D158"]  # Orange, Blue, Green
        self.colors_name = ["Orange", "Blue", "Green"]

        self.setup_ui()

    def setup_ui(self):
        # 1. Header Frame (y = ...)
        graph_header_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        graph_header_frame.pack(fill="x", padx=10, pady=5)

        self.graph_entries = []
        for i in range(3):
            row_frame = tk.Frame(graph_header_frame, bg="#2C2C2E")
            row_frame.pack(fill="x", pady=2)

            lbl = tk.Label(
                row_frame,
                text=f"y{i+1} = ",
                fg=self.colors[i],
                bg="#2C2C2E",
                font=("Segoe UI", 10, "bold")
            )
            lbl.pack(side="left")

            entry = tk.Entry(
                row_frame,
                bg="#1C1C1E",
                fg="#FFFFFF",
                font=("Segoe UI", 9, "bold"),
                bd=3,
                relief="flat",
                insertbackground="#FFFFFF"
            )
            entry.pack(side="left", fill="x", expand=True)
            if i == 0:
                entry.insert(0, "sin(x)")
            self.graph_entries.append(entry)

        # 2. X Range inputs frame
        graph_range_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        graph_range_frame.pack(fill="x", padx=10, pady=2)

        xmin_label = tk.Label(graph_range_frame, text="x min:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        xmin_label.pack(side="left", padx=(0, 2))

        self.graph_xmin_entry = tk.Entry(
            graph_range_frame,
            bg="#1C1C1E",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            bd=3,
            relief="flat",
            insertbackground="#FFFFFF",
            width=6
        )
        self.graph_xmin_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.graph_xmin_entry.insert(0, "-10")

        xmax_label = tk.Label(graph_range_frame, text="x max:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        xmax_label.pack(side="left", padx=(0, 2))

        self.graph_xmax_entry = tk.Entry(
            graph_range_frame,
            bg="#1C1C1E",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            bd=3,
            relief="flat",
            insertbackground="#FFFFFF",
            width=6
        )
        self.graph_xmax_entry.pack(side="left", fill="x", expand=True)
        self.graph_xmax_entry.insert(0, "10")

        # 3. Zoom Controls & Export Frame
        control_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        control_frame.pack(fill="x", padx=10, pady=2)

        zoom_in_btn = tk.Button(
            control_frame, text="Zoom In (+)", bg="#48484A", fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"), bd=0, relief="flat", height=1,
            command=self.zoom_in
        )
        zoom_in_btn.pack(side="left", fill="x", expand=True, padx=(0, 2))

        zoom_out_btn = tk.Button(
            control_frame, text="Zoom Out (-)", bg="#48484A", fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"), bd=0, relief="flat", height=1,
            command=self.zoom_out
        )
        zoom_out_btn.pack(side="left", fill="x", expand=True, padx=2)

        export_btn = tk.Button(
            control_frame, text="Export PNG", bg="#48484A", fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"), bd=0, relief="flat", height=1,
            command=self.export_png
        )
        export_btn.pack(side="right", fill="x", expand=True, padx=(2, 0))

        # 4. Plot button
        plot_btn = tk.Button(
            self.tab_frame,
            text="Plot Functions",
            bg="#30D158",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            relief="flat",
            activebackground="#34C759",
            activeforeground="#FFFFFF",
            height=2,
            command=self.plot_function
        )
        plot_btn.pack(fill="x", padx=10, pady=5)

        # 5. Canvas plotting screen
        self.graph_canvas = tk.Canvas(
            self.tab_frame,
            width=250,
            height=240,
            bg="#1C1C1E",
            bd=0,
            highlightthickness=0
        )
        self.graph_canvas.pack(fill="both", expand=True, padx=10, pady=5)

        # Event bindings for drag-to-pan, scroll-to-zoom, and tracing
        self.graph_canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.graph_canvas.bind("<B1-Motion>", self.on_drag_move)
        self.graph_canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.graph_canvas.bind("<Button-4>", lambda e: self.zoom_in())
        self.graph_canvas.bind("<Button-5>", lambda e: self.zoom_out())
        self.graph_canvas.bind("<Motion>", self.on_mouse_hover)
        self.graph_canvas.bind("<Leave>", self.on_mouse_leave)

    def plot_function(self):
        self.graph_canvas.delete("all")
        W = self.graph_canvas.winfo_width()
        H = self.graph_canvas.winfo_height()
        if W <= 1 or H <= 1:
            W, H = 250, 240

        # Parse custom range
        try:
            xmin = float(self.graph_xmin_entry.get().strip())
            xmax = float(self.graph_xmax_entry.get().strip())
            if xmin >= xmax:
                raise ValueError("xmin >= xmax")
        except Exception:
            self.graph_canvas.create_text(
                W / 2, H / 2,
                text="Invalid X Range (xmin < xmax)",
                fill="#FF3B30",
                font=("Segoe UI", 10, "bold")
            )
            return

        mode = self.app.mode_manager.get_mode()
        x_vals = [xmin + (xmax - xmin) * i / 99 for i in range(100)]

        all_curves_pts = []
        all_valid_y = []

        for entry in self.graph_entries:
            expr = entry.get().strip()
            if not expr:
                all_curves_pts.append([])
                continue

            pts = []
            for x in x_vals:
                try:
                    y = self.app.evaluator.evaluate(expr, mode, variables={"x": x})
                    if isinstance(y, (int, float)) and not math.isnan(y) and not math.isinf(y):
                        pts.append((x, y))
                        all_valid_y.append(y)
                    else:
                        pts.append((x, None))
                except Exception:
                    pts.append((x, None))
            all_curves_pts.append(pts)

        if not all_valid_y:
            self.graph_canvas.create_text(
                W / 2, H / 2,
                text="No functions to plot",
                fill="#8E8E93",
                font=("Segoe UI", 10, "bold")
            )
            return

        # Outlier rejection using percentiles to gracefully handle asymptotes
        sorted_y = sorted(all_valid_y)
        n = len(sorted_y)
        if n > 10:
            p5 = sorted_y[int(n * 0.05)]
            p95 = sorted_y[int(n * 0.95)]
            margin = (p95 - p5) * 0.1 if p95 > p5 else 1.0
            ymin = p5 - margin
            ymax = p95 + margin
        else:
            ymin, ymax = min(all_valid_y), max(all_valid_y)

        # Handle flat lines
        if abs(ymax - ymin) < 1e-9:
            ymin -= 1.0
            ymax += 1.0

        # Save ranges for mouse hover tracing
        self.last_xmin = xmin
        self.last_xmax = xmax
        self.last_ymin = ymin
        self.last_ymax = ymax

        # Helper functions to convert coordinates to pixel positions
        def to_px(x_val):
            return (x_val - xmin) / (xmax - xmin) * W

        def to_py(y_val):
            return H - (y_val - ymin) / (ymax - ymin) * H

        # Nice tick step calculator
        def get_nice_step(range_val):
            raw_step = range_val / 5.0
            if raw_step <= 0:
                return 1.0
            power = math.floor(math.log10(raw_step))
            ratio = raw_step / (10**power)
            if ratio < 1.5:
                nice_ratio = 1.0
            elif ratio < 3.0:
                nice_ratio = 2.0
            elif ratio < 7.0:
                nice_ratio = 5.0
            else:
                nice_ratio = 10.0
            return nice_ratio * (10**power)

        x_step = get_nice_step(xmax - xmin)
        y_step = get_nice_step(ymax - ymin)

        # Draw Grid Lines
        # 1. Vertical grid lines
        start_x = math.ceil(xmin / x_step) * x_step
        curr_x = start_x
        while curr_x <= xmax:
            px = to_px(curr_x)
            self.graph_canvas.create_line(px, 0, px, H, fill="#2C2C2E", width=1)
            label_text = f"{curr_x:.4g}"
            if abs(curr_x) > 1e-9:
                self.graph_canvas.create_text(
                    px, H - 10,
                    text=label_text,
                    fill="#8E8E93",
                    font=("Segoe UI", 7)
                )
            curr_x += x_step

        # 2. Horizontal grid lines
        start_y = math.ceil(ymin / y_step) * y_step
        curr_y = start_y
        while curr_y <= ymax:
            py = to_py(curr_y)
            self.graph_canvas.create_line(0, py, W, py, fill="#2C2C2E", width=1)
            label_text = f"{curr_y:.4g}"
            if abs(curr_y) > 1e-9:
                self.graph_canvas.create_text(
                    15, py,
                    text=label_text,
                    fill="#8E8E93",
                    font=("Segoe UI", 7),
                    anchor="w"
                )
            curr_y += y_step

        # Draw Main Axes
        if ymin <= 0 <= ymax:
            py_zero = to_py(0)
            self.graph_canvas.create_line(0, py_zero, W, py_zero, fill="#555555", width=2)
            if xmin <= 0 <= xmax:
                px_zero = to_px(0)
                self.graph_canvas.create_text(
                    px_zero - 5, py_zero + 10,
                    text="0",
                    fill="#8E8E93",
                    font=("Segoe UI", 7)
                )
        if xmin <= 0 <= xmax:
            px_zero = to_px(0)
            self.graph_canvas.create_line(px_zero, 0, px_zero, H, fill="#555555", width=2)

        # Plot Curves
        for i, pts in enumerate(all_curves_pts):
            if not pts:
                continue
            coords = []
            for x, y in pts:
                if y is not None:
                    px = to_px(x)
                    py = to_py(y)
                    py_clipped = max(-2 * H, min(3 * H, py))
                    coords.append((px, py_clipped))
                else:
                    if len(coords) > 1:
                        flat_coords = [c for pt in coords for c in pt]
                        self.graph_canvas.create_line(flat_coords, fill=self.colors[i], width=2)
                    coords = []

            if len(coords) > 1:
                flat_coords = [c for pt in coords for c in pt]
                self.graph_canvas.create_line(flat_coords, fill=self.colors[i], width=2)

        # Outermost bounds indicators
        self.graph_canvas.create_text(
            W - 10, 15,
            text=f"y max: {self.app.format_result(ymax)[:6]}",
            fill="#FF9500",
            font=("Segoe UI", 8, "bold"),
            anchor="e"
        )
        self.graph_canvas.create_text(
            W - 10, H - 15,
            text=f"y min: {self.app.format_result(ymin)[:6]}",
            fill="#FF9500",
            font=("Segoe UI", 8, "bold"),
            anchor="e"
        )

    # --- Mouse Drag Event Handlers ---
    def on_drag_start(self, event):
        self.drag_start_x = event.x
        try:
            self.drag_xmin = float(self.graph_xmin_entry.get().strip())
            self.drag_xmax = float(self.graph_xmax_entry.get().strip())
        except ValueError:
            pass

    def on_drag_move(self, event):
        if not hasattr(self, 'drag_start_x') or not hasattr(self, 'drag_xmin'):
            return
        dx = event.x - self.drag_start_x
        W = self.graph_canvas.winfo_width()
        if W <= 1:
            W = 250
        dx_coords = dx * (self.drag_xmax - self.drag_xmin) / W

        new_xmin = self.drag_xmin - dx_coords
        new_xmax = self.drag_xmax - dx_coords

        self.graph_xmin_entry.delete(0, tk.END)
        self.graph_xmin_entry.insert(0, f"{new_xmin:.4g}")
        self.graph_xmax_entry.delete(0, tk.END)
        self.graph_xmax_entry.insert(0, f"{new_xmax:.4g}")
        self.plot_function()

    def zoom_in(self):
        try:
            xmin = float(self.graph_xmin_entry.get().strip())
            xmax = float(self.graph_xmax_entry.get().strip())
            center = (xmin + xmax) / 2
            half_range = (xmax - xmin) / 2
            new_half_range = half_range * 0.8
            new_xmin = center - new_half_range
            new_xmax = center + new_half_range

            self.graph_xmin_entry.delete(0, tk.END)
            self.graph_xmin_entry.insert(0, f"{new_xmin:.4g}")
            self.graph_xmax_entry.delete(0, tk.END)
            self.graph_xmax_entry.insert(0, f"{new_xmax:.4g}")
            self.plot_function()
        except ValueError:
            pass

    def zoom_out(self):
        try:
            xmin = float(self.graph_xmin_entry.get().strip())
            xmax = float(self.graph_xmax_entry.get().strip())
            center = (xmin + xmax) / 2
            half_range = (xmax - xmin) / 2
            new_half_range = half_range * 1.25
            new_xmin = center - new_half_range
            new_xmax = center + new_half_range

            self.graph_xmin_entry.delete(0, tk.END)
            self.graph_xmin_entry.insert(0, f"{new_xmin:.4g}")
            self.graph_xmax_entry.delete(0, tk.END)
            self.graph_xmax_entry.insert(0, f"{new_xmax:.4g}")
            self.plot_function()
        except ValueError:
            pass

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.zoom_in()
        elif event.delta < 0:
            self.zoom_out()

    # --- Tracing & Tooltips ---
    def on_mouse_hover(self, event):
        if not hasattr(self, "last_xmin") or not hasattr(self, "last_ymin"):
            return
        
        W = self.graph_canvas.winfo_width()
        H = self.graph_canvas.winfo_height()
        if W <= 1 or H <= 1:
            W, H = 250, 240

        px = event.x
        if px < 0 or px > W:
            return

        self.graph_canvas.delete("crosshair")

        # Draw vertical crosshair guide
        self.graph_canvas.create_line(px, 0, px, H, fill="#555555", dash=(3, 3), tags="crosshair")

        # Convert px to x coordinate
        xmin, xmax = self.last_xmin, self.last_xmax
        ymin, ymax = self.last_ymin, self.last_ymax
        x = xmin + (px / W) * (xmax - xmin)

        def to_py(y_val):
            return H - (y_val - ymin) / (ymax - ymin) * H

        tooltip_lines = [f"x: {x:.3f}"]
        mode = self.app.mode_manager.get_mode()
        
        has_curve = False
        for i, entry in enumerate(self.graph_entries):
            expr = entry.get().strip()
            if not expr:
                continue
            try:
                y = self.app.evaluator.evaluate(expr, mode, variables={"x": x})
                if isinstance(y, (int, float)) and not math.isnan(y) and not math.isinf(y):
                    py = to_py(y)
                    if 0 <= py <= H:
                        # Draw circle on intersection point
                        self.graph_canvas.create_oval(
                            px - 4, py - 4, px + 4, py + 4,
                            fill=self.colors[i], outline="#FFFFFF", width=1, tags="crosshair"
                        )
                        has_curve = True
                    tooltip_lines.append(f"y{i+1}: {y:.3f}")
            except Exception:
                pass

        if not has_curve:
            return

        # Renders the floating tooltip box
        tooltip_text = "\n".join(tooltip_lines)
        tx = px + 10
        ty = event.y + 10
        box_w = 90
        box_h = 15 + len(tooltip_lines) * 12

        if tx + box_w > W:
            tx = px - box_w - 10
        if ty + box_h > H:
            ty = event.y - box_h - 10

        self.graph_canvas.create_rectangle(
            tx, ty, tx + box_w, ty + box_h,
            fill="#2C2C2E", outline="#FF9500", width=1, tags="crosshair"
        )
        self.graph_canvas.create_text(
            tx + 5, ty + 5, text=tooltip_text,
            fill="#FFFFFF", font=("Consolas", 8), anchor="nw", tags="crosshair"
        )

    def on_mouse_leave(self, event):
        self.graph_canvas.delete("crosshair")

    # --- PNG Export ---
    def export_png(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            title="Export Graph as PNG"
        )
        if not filepath:
            return

        # Draw offscreen image (W=500, H=480 for higher fidelity export)
        W, H = 500, 480
        img = Image.new("RGB", (W, H), "#1C1C1E")
        draw = ImageDraw.Draw(img)

        try:
            xmin = float(self.graph_xmin_entry.get().strip())
            xmax = float(self.graph_xmax_entry.get().strip())
            if xmin >= xmax:
                return
        except ValueError:
            return

        mode = self.app.mode_manager.get_mode()
        x_vals = [xmin + (xmax - xmin) * i / 199 for i in range(200)]  # Higher resolution curve

        all_curves_pts = []
        all_valid_y = []

        for entry in self.graph_entries:
            expr = entry.get().strip()
            if not expr:
                all_curves_pts.append([])
                continue

            pts = []
            for x in x_vals:
                try:
                    y = self.app.evaluator.evaluate(expr, mode, variables={"x": x})
                    if isinstance(y, (int, float)) and not math.isnan(y) and not math.isinf(y):
                        pts.append((x, y))
                        all_valid_y.append(y)
                    else:
                        pts.append((x, None))
                except Exception:
                    pts.append((x, None))
            all_curves_pts.append(pts)

        if not all_valid_y:
            return

        sorted_y = sorted(all_valid_y)
        n = len(sorted_y)
        if n > 10:
            p5 = sorted_y[int(n * 0.05)]
            p95 = sorted_y[int(n * 0.95)]
            margin = (p95 - p5) * 0.1 if p95 > p5 else 1.0
            ymin = p5 - margin
            ymax = p95 + margin
        else:
            ymin, ymax = min(all_valid_y), max(all_valid_y)

        if abs(ymax - ymin) < 1e-9:
            ymin -= 1.0
            ymax += 1.0

        def to_px(x_val):
            return (x_val - xmin) / (xmax - xmin) * W

        def to_py(y_val):
            return H - (y_val - ymin) / (ymax - ymin) * H

        # Nice tick step calculator
        def get_nice_step(range_val):
            raw_step = range_val / 5.0
            if raw_step <= 0:
                return 1.0
            power = math.floor(math.log10(raw_step))
            ratio = raw_step / (10**power)
            if ratio < 1.5:
                nice_ratio = 1.0
            elif ratio < 3.0:
                nice_ratio = 2.0
            elif ratio < 7.0:
                nice_ratio = 5.0
            else:
                nice_ratio = 10.0
            return nice_ratio * (10**power)

        x_step = get_nice_step(xmax - xmin)
        y_step = get_nice_step(ymax - ymin)

        # Draw grid
        start_x = math.ceil(xmin / x_step) * x_step
        curr_x = start_x
        while curr_x <= xmax:
            px = to_px(curr_x)
            draw.line([(px, 0), (px, H)], fill="#2C2C2E", width=1)
            curr_x += x_step

        start_y = math.ceil(ymin / y_step) * y_step
        curr_y = start_y
        while curr_y <= ymax:
            py = to_py(curr_y)
            draw.line([(0, py), (W, py)], fill="#2C2C2E", width=1)
            curr_y += y_step

        # Draw Axes
        if ymin <= 0 <= ymax:
            py_zero = to_py(0)
            draw.line([(0, py_zero), (W, py_zero)], fill="#555555", width=2)
        if xmin <= 0 <= xmax:
            px_zero = to_px(0)
            draw.line([(px_zero, 0), (px_zero, H)], fill="#555555", width=2)

        # Plot curves
        for i, pts in enumerate(all_curves_pts):
            if not pts:
                continue
            coords = []
            for x, y in pts:
                if y is not None:
                    px = to_px(x)
                    py = to_py(y)
                    py_clipped = max(-2 * H, min(3 * H, py))
                    coords.append((px, py_clipped))
                else:
                    if len(coords) > 1:
                        draw.line(coords, fill=self.colors[i], width=3)
                    coords = []
            if len(coords) > 1:
                draw.line(coords, fill=self.colors[i], width=3)

        # Save PNG file
        img.save(filepath, "PNG")
