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

        self.xmin_label = tk.Label(graph_range_frame, text="x min:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        self.xmin_label.pack(side="left", padx=(0, 2))

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

        self.xmax_label = tk.Label(graph_range_frame, text="x max:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 9, "bold"))
        self.xmax_label.pack(side="left", padx=(0, 2))

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

        # Mode & Key Points Selection Frame
        mode_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        mode_frame.pack(fill="x", padx=10, pady=2)

        tk.Label(mode_frame, text="Mode:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 8, "bold")).pack(side="left")
        self.graph_mode = tk.StringVar(value="Cartesian")
        mode_menu = tk.OptionMenu(
            mode_frame, self.graph_mode,
            "Cartesian", "Polar", "Parametric",
            command=self.on_mode_change
        )
        mode_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 8, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        mode_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 8, "bold"))
        mode_menu.pack(side="left", padx=5)

        self.show_key_points = tk.BooleanVar(value=False)
        self.key_points_cb = tk.Checkbutton(
            mode_frame, text="Show Key Points", variable=self.show_key_points,
            fg="#FFFFFF", bg="#2C2C2E", selectcolor="#1C1C1E",
            activebackground="#2C2C2E", activeforeground="#FFFFFF",
            font=("Segoe UI", 8, "bold"), command=self.plot_function
        )
        self.key_points_cb.pack(side="right", padx=5)

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
        if W <= 1:
            W = 300
        if H <= 1:
            H = 280

        # Parse range
        try:
            pmin = float(self.graph_xmin_entry.get().strip())
            pmax = float(self.graph_xmax_entry.get().strip())
            if pmin >= pmax:
                self._draw_error(W, H, "Invalid X range (xmin must be < xmax)")
                return
        except Exception:
            self._draw_error(W, H, "Invalid range")
            return

        mode_name = self.graph_mode.get()
        mode = self.app.mode_manager.get_mode()
        N = 500

        all_curves_pts = []
        all_valid_y = []
        all_valid_x = []
        plotted_count = 0

        if mode_name == "Cartesian":
            xmin, xmax = pmin, pmax
            x_vals = [xmin + (xmax - xmin) * i / (N - 1) for i in range(N)]

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

        elif mode_name == "Polar":
            expr = self.graph_entries[0].get().strip()
            if not expr:
                self._draw_placeholder(W, H)
                return
            plotted_count = 1
            pts = []
            for i in range(N):
                theta = pmin + (pmax - pmin) * i / (N - 1)
                try:
                    r = self.app.evaluator.evaluate(expr, mode, variables={"theta": theta})
                    if isinstance(r, complex):
                        r = r.real
                    if isinstance(r, (int, float)) and math.isfinite(r):
                        x = r * math.cos(theta)
                        y = r * math.sin(theta)
                        pts.append((x, y))
                        all_valid_x.append(x)
                        all_valid_y.append(y)
                except Exception:
                    pass
            all_curves_pts.append(pts)

            if not all_valid_y or not all_valid_x:
                self._draw_error(W, H, "No plottable values found")
                return

            xmin, xmax = min(all_valid_x), max(all_valid_x)
            ymin, ymax = min(all_valid_y), max(all_valid_y)
            margin_x = (xmax - xmin) * 0.15 or 1.0
            margin_y = (ymax - ymin) * 0.15 or 1.0
            xmin -= margin_x
            xmax += margin_x
            ymin -= margin_y
            ymax += margin_y

        elif mode_name == "Parametric":
            expr_x = self.graph_entries[0].get().strip()
            expr_y = self.graph_entries[1].get().strip()
            if not expr_x or not expr_y:
                self._draw_placeholder(W, H)
                return
            plotted_count = 2
            pts = []
            for i in range(N):
                t = pmin + (pmax - pmin) * i / (N - 1)
                try:
                    x = self.app.evaluator.evaluate(expr_x, mode, variables={"t": t})
                    y = self.app.evaluator.evaluate(expr_y, mode, variables={"t": t})
                    if isinstance(x, complex): x = x.real
                    if isinstance(y, complex): y = y.real
                    if isinstance(x, (int, float)) and isinstance(y, (int, float)) and math.isfinite(x) and math.isfinite(y):
                        pts.append((x, y))
                        all_valid_x.append(x)
                        all_valid_y.append(y)
                except Exception:
                    pass
            all_curves_pts.append(pts)

            if not all_valid_y or not all_valid_x:
                self._draw_error(W, H, "No plottable values found")
                return

            xmin, xmax = min(all_valid_x), max(all_valid_x)
            ymin, ymax = min(all_valid_y), max(all_valid_y)
            margin_x = (xmax - xmin) * 0.15 or 1.0
            margin_y = (ymax - ymin) * 0.15 or 1.0
            xmin -= margin_x
            xmax += margin_x
            ymin -= margin_y
            ymax += margin_y

        # Prevent flat lines
        if abs(ymax - ymin) < 1e-9:
            ymin -= 1.0
            ymax += 1.0
        if abs(xmax - xmin) < 1e-9:
            xmin -= 1.0
            xmax += 1.0

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

        # --- Draw key points ---
        if self.show_key_points.get() and mode_name == "Cartesian":
            self._find_and_draw_key_points(W, H, xmin, xmax, ymin, ymax, to_px, to_py)

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
        if mode_name == "Cartesian":
            self.status_var.set(f"Plotted: {expr_list} | x∈[{xmin:.3g}, {xmax:.3g}]")
        elif mode_name == "Polar":
            self.status_var.set(f"Plotted Polar Rose | θ∈[{pmin:.3g}, {pmax:.3g}]")
        else:
            self.status_var.set(f"Plotted Parametric Curve | t∈[{pmin:.3g}, {pmax:.3g}]")

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

    def on_mode_change(self, *args):
        m = self.graph_mode.get()
        if m == "Cartesian":
            self.xmin_label.config(text="x min:")
            self.xmax_label.config(text="x max:")
            self.graph_xmin_entry.delete(0, tk.END)
            self.graph_xmin_entry.insert(0, "-10")
            self.graph_xmax_entry.delete(0, tk.END)
            self.graph_xmax_entry.insert(0, "10")
            self.graph_entries[0].master.pack(fill="x", pady=2)
            self.graph_entries[1].master.pack(fill="x", pady=2)
            self.graph_entries[2].master.pack(fill="x", pady=2)
            self.graph_entries[0].delete(0, tk.END)
            self.graph_entries[0].insert(0, "sin(x)")
            self.graph_entries[1].delete(0, tk.END)
            self.graph_entries[2].delete(0, tk.END)
        elif m == "Polar":
            self.xmin_label.config(text="θ min:")
            self.xmax_label.config(text="θ max:")
            self.graph_xmin_entry.delete(0, tk.END)
            self.graph_xmin_entry.insert(0, "0")
            self.graph_xmax_entry.delete(0, tk.END)
            self.graph_xmax_entry.insert(0, "6.28318")
            self.graph_entries[0].delete(0, tk.END)
            self.graph_entries[0].insert(0, "2 * cos(4 * theta)")
            self.graph_entries[0].master.pack(fill="x", pady=2)
            self.graph_entries[1].master.pack_forget()
            self.graph_entries[2].master.pack_forget()
        elif m == "Parametric":
            self.xmin_label.config(text="t min:")
            self.xmax_label.config(text="t max:")
            self.graph_xmin_entry.delete(0, tk.END)
            self.graph_xmin_entry.insert(0, "0")
            self.graph_xmax_entry.delete(0, tk.END)
            self.graph_xmax_entry.insert(0, "6.28318")
            self.graph_entries[0].master.pack(fill="x", pady=2)
            self.graph_entries[1].master.pack(fill="x", pady=2)
            self.graph_entries[2].master.pack_forget()
            self.graph_entries[0].delete(0, tk.END)
            self.graph_entries[0].insert(0, "sin(2 * t)")
            self.graph_entries[1].delete(0, tk.END)
            self.graph_entries[1].insert(0, "sin(3 * t)")
        self.plot_function()

    def _find_and_draw_key_points(self, W, H, xmin, xmax, ymin, ymax, to_px, to_py):
        mode = self.app.mode_manager.get_mode()
        exprs = []
        for i, entry in enumerate(self.graph_entries):
            expr = entry.get().strip()
            if expr:
                exprs.append((expr, self.colors[i]))
        if not exprs:
            return

        def eval_f(expr, val):
            try:
                res = self.app.evaluator.evaluate(expr, mode, variables={"x": val})
                if isinstance(res, complex):
                    res = res.real
                return float(res) if math.isfinite(res) else None
            except Exception:
                return None

        def eval_df(expr, val, h=1e-5):
            y_h = eval_f(expr, val + h)
            y_mh = eval_f(expr, val - h)
            if y_h is not None and y_mh is not None:
                return (y_h - y_mh) / (2 * h)
            return None

        def bisect(g_func, x1, x2, tol=1e-5, max_iter=30):
            y1, y2 = g_func(x1), g_func(x2)
            if y1 is None or y2 is None or y1 * y2 > 0:
                return None
            for _ in range(max_iter):
                mid = (x1 + x2) / 2.0
                ymid = g_func(mid)
                if ymid is None:
                    return None
                if abs(ymid) < tol or abs(x2 - x1) < tol:
                    return mid
                if y1 * ymid < 0:
                    x2 = mid
                    y2 = ymid
                else:
                    x1 = mid
                    y1 = ymid
            return (x1 + x2) / 2.0

        steps = 80
        dx = (xmax - xmin) / steps
        roots_found = set()
        extrema_found = set()
        intersections_found = set()

        for expr, color in exprs:
            for i in range(steps):
                x1 = xmin + i * dx
                x2 = x1 + dx

                r = bisect(lambda x: eval_f(expr, x), x1, x2)
                if r is not None and xmin <= r <= xmax:
                    y_r = eval_f(expr, r)
                    if y_r is not None and abs(y_r) < 1e-3:
                        if not any(abs(r - val) < 1e-2 for val in roots_found):
                            roots_found.add(r)
                            px, py = to_px(r), to_py(y_r)
                            if 0 <= px <= W and 0 <= py <= H:
                                self.graph_canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill="#FF3B30", outline="#FFFFFF", width=1)
                                label = f"({self.app.format_result(r)}, 0)"
                                self.graph_canvas.create_text(px, py - 10, text=label, fill="#FF3B30", font=("Segoe UI", 7, "bold"))

                e = bisect(lambda x: eval_df(expr, x), x1, x2)
                if e is not None and xmin <= e <= xmax:
                    y_e = eval_f(expr, e)
                    if y_e is not None:
                        if not any(abs(e - val) < 1e-2 for val in extrema_found):
                            extrema_found.add(e)
                            px, py = to_px(e), to_py(y_e)
                            if 0 <= px <= W and 0 <= py <= H:
                                self.graph_canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill="#0A84FF", outline="#FFFFFF", width=1)
                                label = f"({self.app.format_result(e)}, {self.app.format_result(y_e)})"
                                self.graph_canvas.create_text(px, py - 10, text=label, fill="#0A84FF", font=("Segoe UI", 7, "bold"))

        if len(exprs) >= 2:
            for idx1 in range(len(exprs)):
                for idx2 in range(idx1 + 1, len(exprs)):
                    e1, _ = exprs[idx1]
                    e2, _ = exprs[idx2]
                    for i in range(steps):
                        x1 = xmin + i * dx
                        x2 = x1 + dx
                        
                        def diff_val(x):
                            v1 = eval_f(e1, x)
                            v2 = eval_f(e2, x)
                            if v1 is not None and v2 is not None:
                                return v1 - v2
                            return None
                            
                        sect = bisect(diff_val, x1, x2)
                        if sect is not None and xmin <= sect <= xmax:
                            y_sect = eval_f(e1, sect)
                            if y_sect is not None:
                                if not any(abs(sect - val) < 1e-2 for val in intersections_found):
                                    intersections_found.add(sect)
                                    px, py = to_px(sect), to_py(y_sect)
                                    if 0 <= px <= W and 0 <= py <= H:
                                        self.graph_canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill="#5856D6", outline="#FFFFFF", width=1)
                                        label = f"({self.app.format_result(sect)}, {self.app.format_result(y_sect)})"
                                        self.graph_canvas.create_text(px, py + 10, text=label, fill="#5856D6", font=("Segoe UI", 7, "bold"))
