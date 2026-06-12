"""
Controller for the 2D Function Grapher tab with multi-function support, hover tracing, and PNG export.
"""

import math
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class GraphController:
    def __init__(self, app, tab_frame):
        self.app = app  # Reference to main CalculatorApp
        self.tab_frame = tab_frame

        self.graph_entries = []
        self.colors = ["#FF9500", "#0A84FF", "#30D158"]  # Orange, Blue, Green
        self.colors_name = ["Orange", "Blue", "Green"]

        # Viewport state
        self.last_xmin = -10.0
        self.last_xmax = 10.0
        self.last_ymin = -2.0
        self.last_ymax = 2.0

        self._plot_scheduled = False

        self.setup_ui()

    def setup_ui(self):
        # 1. Header Frame (y = ...)
        graph_header_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        graph_header_frame.pack(fill="x", padx=10, pady=(8, 2))

        self.graph_entries = []
        for i in range(3):
            row_frame = tk.Frame(graph_header_frame, bg="#2C2C2E")
            row_frame.pack(fill="x", pady=2)

            lbl = tk.Label(
                row_frame,
                text=f"y{i+1} = ",
                fg=self.colors[i],
                bg="#2C2C2E",
                font=("Segoe UI", 10, "bold"),
                width=5,
                anchor="e"
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
            # Re-plot when user edits any entry
            entry.bind("<Return>", lambda e: self.plot_function())

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
            control_frame, text="⊕ Zoom In", bg="#48484A", fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"), bd=0, relief="flat", height=1,
            activebackground="#636366", activeforeground="#FFFFFF",
            command=self.zoom_in
        )
        zoom_in_btn.pack(side="left", fill="x", expand=True, padx=(0, 2))

        zoom_out_btn = tk.Button(
            control_frame, text="⊖ Zoom Out", bg="#48484A", fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"), bd=0, relief="flat", height=1,
            activebackground="#636366", activeforeground="#FFFFFF",
            command=self.zoom_out
        )
        zoom_out_btn.pack(side="left", fill="x", expand=True, padx=2)

        reset_btn = tk.Button(
            control_frame, text="↺ Reset", bg="#48484A", fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"), bd=0, relief="flat", height=1,
            activebackground="#636366", activeforeground="#FFFFFF",
            command=self.reset_view
        )
        reset_btn.pack(side="left", fill="x", expand=True, padx=2)

        export_btn = tk.Button(
            control_frame, text="⬇ PNG", bg="#48484A", fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"), bd=0, relief="flat", height=1,
            activebackground="#636366", activeforeground="#FFFFFF",
            command=self.export_png
        )
        export_btn.pack(side="right", fill="x", expand=True, padx=(2, 0))

        # 4. Plot button
        plot_btn = tk.Button(
            self.tab_frame,
            text="▶  Plot Functions",
            bg="#30D158",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            relief="flat",
            activebackground="#34C759",
            activeforeground="#FFFFFF",
            height=1,
            command=self.plot_function
        )
        plot_btn.pack(fill="x", padx=10, pady=4)

        # 5. Canvas plotting screen
        self.graph_canvas = tk.Canvas(
            self.tab_frame,
            bg="#111111",
            bd=0,
            highlightthickness=1,
            highlightbackground="#48484A"
        )
        self.graph_canvas.pack(fill="both", expand=True, padx=10, pady=(2, 8))

        # 6. Status bar
        self.status_var = tk.StringVar(value="Ready — Enter a function and click Plot")
        self.status_bar = tk.Label(
            self.tab_frame,
            textvariable=self.status_var,
            fg="#8E8E93",
            bg="#2C2C2E",
            font=("Segoe UI", 8),
            anchor="w",
            padx=10
        )
        self.status_bar.pack(fill="x", pady=(0, 4))

        # Event bindings for drag-to-pan, scroll-to-zoom, and tracing
        self.graph_canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.graph_canvas.bind("<B1-Motion>", self.on_drag_move)
        self.graph_canvas.bind("<ButtonRelease-1>", self.on_drag_end)
        self.graph_canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.graph_canvas.bind("<Button-4>", lambda e: self.zoom_in())
        self.graph_canvas.bind("<Button-5>", lambda e: self.zoom_out())
        self.graph_canvas.bind("<Motion>", self.on_mouse_hover)
        self.graph_canvas.bind("<Leave>", self.on_mouse_leave)

        self._is_dragging = False
        self._drag_start_canvas_x = 0

    # -------------------------------------------------------------------------
    #  Core plotting
    # -------------------------------------------------------------------------
    def plot_function(self):
        """Compute and draw all functions on the canvas."""
        self.graph_canvas.delete("all")
        W = self.graph_canvas.winfo_width()
        H = self.graph_canvas.winfo_height()
        # Use sensible fallback if canvas not yet rendered
        if W <= 1:
            W = 300
        if H <= 1:
            H = 280

        # Parse custom range
        try:
            xmin = float(self.graph_xmin_entry.get().strip())
            xmax = float(self.graph_xmax_entry.get().strip())
            if xmin >= xmax:
                raise ValueError("xmin >= xmax")
        except Exception:
            self._draw_error(W, H, "Invalid X range (xmin must be < xmax)")
            return

        mode = self.app.mode_manager.get_mode()
        N = max(W, 300)  # Resolution: at least one point per pixel
        x_vals = [xmin + (xmax - xmin) * i / (N - 1) for i in range(N)]

        all_curves_pts = []
        all_valid_y = []
        plotted_count = 0

        for entry in self.graph_entries:
            expr = entry.get().strip()
            if not expr:
                all_curves_pts.append([])
                continue

            plotted_count += 1
            pts = []
            for x in x_vals:
                try:
                    y = self.app.evaluator.evaluate(expr, mode, variables={"x": x})
                    if isinstance(y, complex):
                        if abs(y.imag) < 1e-10:
                            y = y.real
                        else:
                            pts.append((x, None))
                            continue
                    if isinstance(y, (int, float)) and math.isfinite(y):
                        pts.append((x, float(y)))
                        all_valid_y.append(float(y))
                    else:
                        pts.append((x, None))
                except Exception:
                    pts.append((x, None))
            all_curves_pts.append(pts)

        if not all_valid_y:
            if plotted_count == 0:
                self._draw_placeholder(W, H)
            else:
                self._draw_error(W, H, "No plottable values found")
            return

        # Auto Y-range using interquartile range to gracefully handle asymptotes
        sorted_y = sorted(all_valid_y)
        n = len(sorted_y)
        if n > 20:
            p2 = sorted_y[max(0, int(n * 0.02))]
            p98 = sorted_y[min(n - 1, int(n * 0.98))]
            margin = (p98 - p2) * 0.15 if p98 > p2 else 1.0
            ymin = p2 - margin
            ymax = p98 + margin
        else:
            ymin = min(all_valid_y)
            ymax = max(all_valid_y)
            margin = (ymax - ymin) * 0.1 if ymax > ymin else 1.0
            ymin -= margin
            ymax += margin

        # Prevent flat lines
        if abs(ymax - ymin) < 1e-9:
            ymin -= 1.0
            ymax += 1.0

        # Save viewport state for hover tracing
        self.last_xmin = xmin
        self.last_xmax = xmax
        self.last_ymin = ymin
        self.last_ymax = ymax

        # Coordinate helpers
        def to_px(x_val):
            return (x_val - xmin) / (xmax - xmin) * W

        def to_py(y_val):
            return H - (y_val - ymin) / (ymax - ymin) * H

        # --- Draw background gradient (subtle) ---
        self.graph_canvas.create_rectangle(0, 0, W, H, fill="#111111", outline="")

        # --- Draw Grid ---
        x_step = self._nice_step(xmax - xmin)
        y_step = self._nice_step(ymax - ymin)

        # Vertical grid lines
        curr_x = math.ceil(xmin / x_step) * x_step
        while curr_x <= xmax + 1e-9:
            px = to_px(curr_x)
            is_zero = abs(curr_x) < x_step * 0.01
            color = "#3A3A3C" if not is_zero else "#555558"
            self.graph_canvas.create_line(px, 0, px, H, fill=color, width=1)
            if not is_zero:
                label = self._format_tick(curr_x)
                self.graph_canvas.create_text(
                    px, H - 8, text=label, fill="#636366",
                    font=("Segoe UI", 7), anchor="s"
                )
            curr_x += x_step
            if x_step <= 0:
                break

        # Horizontal grid lines
        curr_y = math.ceil(ymin / y_step) * y_step
        while curr_y <= ymax + 1e-9:
            py = to_py(curr_y)
            is_zero = abs(curr_y) < y_step * 0.01
            color = "#3A3A3C" if not is_zero else "#555558"
            self.graph_canvas.create_line(0, py, W, py, fill=color, width=1)
            if not is_zero:
                label = self._format_tick(curr_y)
                self.graph_canvas.create_text(
                    6, py, text=label, fill="#636366",
                    font=("Segoe UI", 7), anchor="w"
                )
            curr_y += y_step
            if y_step <= 0:
                break

        # --- Draw main axes (bright) ---
        if ymin <= 0 <= ymax:
            py_zero = to_py(0)
            self.graph_canvas.create_line(0, py_zero, W, py_zero, fill="#8E8E93", width=1, dash=(4, 4))
        if xmin <= 0 <= xmax:
            px_zero = to_px(0)
            self.graph_canvas.create_line(px_zero, 0, px_zero, H, fill="#8E8E93", width=1, dash=(4, 4))

        # --- Plot each curve ---
        for i, pts in enumerate(all_curves_pts):
            if not pts:
                continue
            self._draw_curve(pts, self.colors[i], to_px, to_py, H)

        # --- Y range labels ---
        self.graph_canvas.create_text(
            W - 4, 4,
            text=f"↑ {self._fmt_val(ymax)}",
            fill="#8E8E93", font=("Segoe UI", 7), anchor="ne"
        )
        self.graph_canvas.create_text(
            W - 4, H - 4,
            text=f"↓ {self._fmt_val(ymin)}",
            fill="#8E8E93", font=("Segoe UI", 7), anchor="se"
        )

        # Update status
        expr_list = ", ".join(
            e.get().strip() for e in self.graph_entries if e.get().strip()
        )
        self.status_var.set(f"Plotted: {expr_list} | x∈[{xmin:.3g}, {xmax:.3g}]")

    def _draw_curve(self, pts, color, to_px, to_py, H):
        """Draw a single curve with gap detection at discontinuities."""
        coords = []
        prev_y = None
        JUMP_THRESHOLD = H * 3  # Pixel jump threshold for discontinuity detection

        for x, y in pts:
            if y is None:
                if len(coords) >= 4:
                    self.graph_canvas.create_line(coords, fill=color, width=2, smooth=True, splinesteps=12)
                coords = []
                prev_y = None
                continue

            px = to_px(x)
            py = to_py(y)
            py_clipped = max(-H, min(2 * H, py))

            # Detect large jumps (asymptotes) — break the line
            if prev_y is not None and abs(py_clipped - prev_y) > JUMP_THRESHOLD:
                if len(coords) >= 4:
                    self.graph_canvas.create_line(coords, fill=color, width=2, smooth=True, splinesteps=12)
                coords = []

            coords.extend([px, py_clipped])
            prev_y = py_clipped

        if len(coords) >= 4:
            self.graph_canvas.create_line(coords, fill=color, width=2, smooth=True, splinesteps=12)

    # -------------------------------------------------------------------------
    #  Helpers
    # -------------------------------------------------------------------------
    def _nice_step(self, range_val):
        """Calculate a human-readable grid step size."""
        if range_val <= 0:
            return 1.0
        raw_step = range_val / 8.0
        if raw_step <= 0:
            return 1.0
        power = math.floor(math.log10(raw_step))
        ratio = raw_step / (10 ** power)
        if ratio < 1.5:
            nice_ratio = 1.0
        elif ratio < 3.0:
            nice_ratio = 2.0
        elif ratio < 7.0:
            nice_ratio = 5.0
        else:
            nice_ratio = 10.0
        return nice_ratio * (10 ** power)

    def _format_tick(self, val):
        if abs(val) >= 1000 or (abs(val) < 0.01 and val != 0):
            return f"{val:.2e}"
        if val == int(val):
            return str(int(val))
        return f"{val:.2g}"

    def _fmt_val(self, val):
        if abs(val) >= 10000 or (abs(val) < 0.001 and val != 0):
            return f"{val:.2e}"
        return f"{val:.4g}"

    def _draw_error(self, W, H, msg):
        self.graph_canvas.create_rectangle(0, 0, W, H, fill="#111111", outline="")
        self.graph_canvas.create_text(
            W / 2, H / 2, text=f"⚠ {msg}",
            fill="#FF453A", font=("Segoe UI", 10, "bold"), justify="center"
        )
        self.status_var.set(f"Error: {msg}")

    def _draw_placeholder(self, W, H):
        self.graph_canvas.create_rectangle(0, 0, W, H, fill="#111111", outline="")
        self.graph_canvas.create_text(
            W / 2, H / 2 - 10,
            text="Enter a function above",
            fill="#636366", font=("Segoe UI", 11, "bold")
        )
        self.graph_canvas.create_text(
            W / 2, H / 2 + 12,
            text="e.g.  sin(x),  x^2,  1/x",
            fill="#48484A", font=("Segoe UI", 9)
        )

    # -------------------------------------------------------------------------
    #  Zoom, Pan, Reset
    # -------------------------------------------------------------------------
    def reset_view(self):
        self.graph_xmin_entry.delete(0, tk.END)
        self.graph_xmin_entry.insert(0, "-10")
        self.graph_xmax_entry.delete(0, tk.END)
        self.graph_xmax_entry.insert(0, "10")
        self.plot_function()

    def zoom_in(self):
        try:
            xmin = float(self.graph_xmin_entry.get().strip())
            xmax = float(self.graph_xmax_entry.get().strip())
            center = (xmin + xmax) / 2
            half_range = (xmax - xmin) / 2 * 0.7
            self._set_range(center - half_range, center + half_range)
            self.plot_function()
        except ValueError:
            pass

    def zoom_out(self):
        try:
            xmin = float(self.graph_xmin_entry.get().strip())
            xmax = float(self.graph_xmax_entry.get().strip())
            center = (xmin + xmax) / 2
            half_range = (xmax - xmin) / 2 * 1.4
            self._set_range(center - half_range, center + half_range)
            self.plot_function()
        except ValueError:
            pass

    def _set_range(self, xmin, xmax):
        self.graph_xmin_entry.delete(0, tk.END)
        self.graph_xmin_entry.insert(0, f"{xmin:.4g}")
        self.graph_xmax_entry.delete(0, tk.END)
        self.graph_xmax_entry.insert(0, f"{xmax:.4g}")

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.zoom_in()
        elif event.delta < 0:
            self.zoom_out()

    # -------------------------------------------------------------------------
    #  Drag-to-Pan
    # -------------------------------------------------------------------------
    def on_drag_start(self, event):
        self._is_dragging = True
        self._drag_start_canvas_x = event.x
        try:
            self._drag_xmin = float(self.graph_xmin_entry.get().strip())
            self._drag_xmax = float(self.graph_xmax_entry.get().strip())
        except ValueError:
            self._is_dragging = False

    def on_drag_move(self, event):
        if not self._is_dragging:
            return
        dx = event.x - self._drag_start_canvas_x
        W = self.graph_canvas.winfo_width()
        if W <= 1:
            W = 300
        dx_world = dx * (self._drag_xmax - self._drag_xmin) / W
        self._set_range(self._drag_xmin - dx_world, self._drag_xmax - dx_world)
        self.plot_function()

    def on_drag_end(self, event):
        self._is_dragging = False

    # -------------------------------------------------------------------------
    #  Hover Tooltip & Crosshair
    # -------------------------------------------------------------------------
    def on_mouse_hover(self, event):
        W = self.graph_canvas.winfo_width()
        H = self.graph_canvas.winfo_height()
        if W <= 1:
            W = 300
        if H <= 1:
            H = 280

        px = event.x
        if px < 0 or px > W:
            return

        self.graph_canvas.delete("crosshair")

        xmin, xmax = self.last_xmin, self.last_xmax
        ymin, ymax = self.last_ymin, self.last_ymax

        # Vertical crosshair
        self.graph_canvas.create_line(
            px, 0, px, H, fill="#555558", dash=(2, 4), tags="crosshair"
        )

        x = xmin + (px / W) * (xmax - xmin)

        def to_py(y_val):
            return H - (y_val - ymin) / (ymax - ymin) * H

        mode = self.app.mode_manager.get_mode()
        tooltip_lines = [f"x = {x:.4g}"]
        has_point = False

        for i, entry in enumerate(self.graph_entries):
            expr = entry.get().strip()
            if not expr:
                continue
            try:
                y = self.app.evaluator.evaluate(expr, mode, variables={"x": x})
                if isinstance(y, complex) and abs(y.imag) < 1e-10:
                    y = y.real
                if isinstance(y, (int, float)) and math.isfinite(y):
                    py = to_py(y)
                    if -10 <= py <= H + 10:
                        # Dot on curve
                        self.graph_canvas.create_oval(
                            px - 4, py - 4, px + 4, py + 4,
                            fill=self.colors[i], outline="#FFFFFF", width=1, tags="crosshair"
                        )
                        has_point = True
                    tooltip_lines.append(f"y{i+1} = {y:.4g}")
            except Exception:
                pass

        if not has_point:
            return

        # Tooltip box
        tooltip_text = "\n".join(tooltip_lines)
        lines_count = len(tooltip_lines)
        box_w = 100
        box_h = 10 + lines_count * 14

        tx = px + 12
        ty = event.y - box_h // 2
        if tx + box_w > W:
            tx = px - box_w - 12
        if ty < 2:
            ty = 2
        if ty + box_h > H - 2:
            ty = H - box_h - 2

        self.graph_canvas.create_rectangle(
            tx - 4, ty - 4, tx + box_w, ty + box_h,
            fill="#1C1C1E", outline="#FF9500", width=1, tags="crosshair"
        )
        self.graph_canvas.create_text(
            tx, ty + 4, text=tooltip_text,
            fill="#FFFFFF", font=("Consolas", 8), anchor="nw", tags="crosshair"
        )

    def on_mouse_leave(self, event):
        self.graph_canvas.delete("crosshair")

    # -------------------------------------------------------------------------
    #  PNG Export
    # -------------------------------------------------------------------------
    def export_png(self):
        if not PIL_AVAILABLE:
            messagebox.showerror(
                "Feature Unavailable",
                "The Pillow library (PIL) is not installed.\n\n"
                "Install it with:\n  pip install pillow\n\n"
                "Then restart the calculator."
            )
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            title="Export Graph as PNG"
        )
        if not filepath:
            return

        W, H = 800, 600
        img = Image.new("RGB", (W, H), "#111111")
        draw = ImageDraw.Draw(img)

        try:
            xmin = float(self.graph_xmin_entry.get().strip())
            xmax = float(self.graph_xmax_entry.get().strip())
            if xmin >= xmax:
                return
        except ValueError:
            return

        mode = self.app.mode_manager.get_mode()
        N = 600
        x_vals = [xmin + (xmax - xmin) * i / (N - 1) for i in range(N)]

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
                    if isinstance(y, complex) and abs(y.imag) < 1e-10:
                        y = y.real
                    if isinstance(y, (int, float)) and math.isfinite(y):
                        pts.append((x, float(y)))
                        all_valid_y.append(float(y))
                    else:
                        pts.append((x, None))
                except Exception:
                    pts.append((x, None))
            all_curves_pts.append(pts)

        if not all_valid_y:
            messagebox.showwarning("Export Failed", "No plottable data to export.")
            return

        sorted_y = sorted(all_valid_y)
        n = len(sorted_y)
        if n > 20:
            p2 = sorted_y[max(0, int(n * 0.02))]
            p98 = sorted_y[min(n - 1, int(n * 0.98))]
            margin = (p98 - p2) * 0.15 if p98 > p2 else 1.0
            ymin = p2 - margin
            ymax = p98 + margin
        else:
            ymin = min(all_valid_y)
            ymax = max(all_valid_y)
            margin = (ymax - ymin) * 0.1 if ymax > ymin else 1.0
            ymin -= margin
            ymax += margin

        if abs(ymax - ymin) < 1e-9:
            ymin -= 1.0
            ymax += 1.0

        def to_px(x_val):
            return int((x_val - xmin) / (xmax - xmin) * W)

        def to_py(y_val):
            return int(H - (y_val - ymin) / (ymax - ymin) * H)

        x_step = self._nice_step(xmax - xmin)
        y_step = self._nice_step(ymax - ymin)

        # Grid
        curr_x = math.ceil(xmin / x_step) * x_step
        while curr_x <= xmax + 1e-9:
            px = to_px(curr_x)
            draw.line([(px, 0), (px, H)], fill="#2A2A2C", width=1)
            curr_x += x_step
            if x_step <= 0:
                break

        curr_y = math.ceil(ymin / y_step) * y_step
        while curr_y <= ymax + 1e-9:
            py = to_py(curr_y)
            draw.line([(0, py), (W, py)], fill="#2A2A2C", width=1)
            curr_y += y_step
            if y_step <= 0:
                break

        # Axes
        if ymin <= 0 <= ymax:
            draw.line([(0, to_py(0)), (W, to_py(0))], fill="#555558", width=1)
        if xmin <= 0 <= xmax:
            draw.line([(to_px(0), 0), (to_px(0), H)], fill="#555558", width=1)

        # Curves
        for i, pts in enumerate(all_curves_pts):
            if not pts:
                continue
            coords = []
            prev_py = None
            JUMP = H * 2
            for x, y in pts:
                if y is None:
                    if len(coords) >= 2:
                        draw.line(coords, fill=self.colors[i], width=3)
                    coords = []
                    prev_py = None
                    continue
                px = to_px(x)
                py = max(-H, min(2 * H, to_py(y)))
                if prev_py is not None and abs(py - prev_py) > JUMP:
                    if len(coords) >= 2:
                        draw.line(coords, fill=self.colors[i], width=3)
                    coords = []
                coords.append((px, py))
                prev_py = py
            if len(coords) >= 2:
                draw.line(coords, fill=self.colors[i], width=3)

        try:
            img.save(filepath, "PNG")
            self.status_var.set(f"Exported: {filepath}")
        except Exception as ex:
            messagebox.showerror("Export Failed", str(ex))
