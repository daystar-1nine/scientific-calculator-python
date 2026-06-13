"""
Controller for the Interactive Simulations tab.
Provides Projectile Motion animation and Fourier Wave Builder animation.
"""

import math
import tkinter as tk
from utils.error_handler import handle_error

class SimulationsController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.sim_mode = tk.StringVar(value="Projectile Motion")
        
        # Projectile parameters
        self.proj_v0 = tk.StringVar(value="50")
        self.proj_theta = tk.StringVar(value="45")
        self.proj_g = tk.StringVar(value="9.81")
        
        # Fourier parameters
        self.fourier_shape = tk.StringVar(value="Square")
        self.fourier_terms = tk.IntVar(value=5)
        
        # Animation state
        self.is_playing = False
        self.proj_t = 0.0
        self.fourier_phase = 0.0
        self.after_id = None
        
        self.setup_ui()

    def setup_ui(self):
        # 1. Top Controls Frame (Selector)
        select_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        select_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            select_frame, text="Simulation:", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        mode_menu = tk.OptionMenu(
            select_frame, self.sim_mode,
            "Projectile Motion", "Fourier Wave Builder",
            command=self.on_mode_change
        )
        mode_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        mode_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        mode_menu.pack(side="left", padx=5)

        # 2. Parameters Container Frame
        self.params_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        self.params_frame.pack(fill="x", padx=10, pady=5)

        # 3. Canvas for rendering simulation
        canvas_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(
            canvas_frame, bg="#111111", highlightthickness=1, highlightbackground="#48484A"
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.redraw())

        # 4. Playback Buttons Frame
        playback_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        playback_frame.pack(fill="x", padx=10, pady=5)

        self.play_btn = tk.Button(
            playback_frame, text="Play", bg="#30D158", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", width=8,
            command=self.play
        )
        self.play_btn.pack(side="left", padx=2)

        self.pause_btn = tk.Button(
            playback_frame, text="Pause", bg="#FF9500", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", width=8,
            command=self.pause
        )
        self.pause_btn.pack(side="left", padx=2)

        self.reset_btn = tk.Button(
            playback_frame, text="Reset", bg="#FF3B30", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", width=8,
            command=self.reset
        )
        self.reset_btn.pack(side="left", padx=2)

        # 5. Readout Panel
        tk.Label(
            self.tab_frame, text="Real-time Statistics:", fg="#8E8E93", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), anchor="w"
        ).pack(fill="x", padx=10, pady=(5, 2))

        self.stats_text = tk.Text(
            self.tab_frame, bg="#1C1C1E", fg="#30D158",
            font=("Consolas", 9, "bold"), height=5, bd=0, highlightthickness=0,
            padx=10, pady=5
        )
        self.stats_text.pack(fill="x", padx=10, pady=(0, 10))
        self.stats_text.config(state="disabled")

        self.on_mode_change()

    def on_mode_change(self, *args):
        self.pause()
        self.reset()
        
        # Clear params frame
        for w in self.params_frame.winfo_children():
            w.destroy()

        mode = self.sim_mode.get()
        if mode == "Projectile Motion":
            row = tk.Frame(self.params_frame, bg="#2C2C2E")
            row.pack(fill="x", pady=2)

            tk.Label(row, text="v0 (m/s):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=8, anchor="w").pack(side="left")
            v0_entry = tk.Entry(row, textvariable=self.proj_v0, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat", width=8)
            v0_entry.pack(side="left", padx=(0, 10))

            tk.Label(row, text="Angle (°):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=8, anchor="w").pack(side="left")
            theta_entry = tk.Entry(row, textvariable=self.proj_theta, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat", width=8)
            theta_entry.pack(side="left", padx=(0, 10))

            tk.Label(row, text="g (m/s²):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=8, anchor="w").pack(side="left")
            g_entry = tk.Entry(row, textvariable=self.proj_g, bg="#1C1C1E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=2, relief="flat", width=8)
            g_entry.pack(side="left")

        elif mode == "Fourier Wave Builder":
            row = tk.Frame(self.params_frame, bg="#2C2C2E")
            row.pack(fill="x", pady=2)

            tk.Label(row, text="Wave Shape:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=12, anchor="w").pack(side="left")
            shape_menu = tk.OptionMenu(row, self.fourier_shape, "Square", "Sawtooth", "Triangle", command=lambda x: self.redraw())
            shape_menu.config(bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", highlightthickness=0)
            shape_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
            shape_menu.pack(side="left", padx=(0, 15))

            tk.Label(row, text="Terms (N):", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), width=10, anchor="w").pack(side="left")
            terms_slider = tk.Scale(
                row, from_=1, to=50, orient="horizontal", variable=self.fourier_terms,
                bg="#2C2C2E", fg="#FFFFFF", highlightthickness=0, font=("Segoe UI", 8, "bold"),
                command=lambda x: self.redraw()
            )
            terms_slider.pack(side="left", fill="x", expand=True)

        self.redraw()

    def update_stats_display(self, text):
        self.stats_text.config(state="normal")
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, text)
        self.stats_text.config(state="disabled")

    def show_error(self, msg):
        self.update_stats_display(f"Configuration Error:\n{msg}")

    def play(self):
        if not self.is_playing:
            self.is_playing = True
            self.animate_step()

    def pause(self):
        self.is_playing = False
        if self.after_id:
            self.tab_frame.after_cancel(self.after_id)
            self.after_id = None

    def reset(self):
        self.pause()
        self.proj_t = 0.0
        self.fourier_phase = 0.0
        self.redraw()

    def get_projectile_params(self):
        calc_mode = self.app.mode_manager.get_mode()
        v0 = float(self.app.evaluator.evaluate(self.proj_v0.get().strip(), calc_mode))
        theta_deg = float(self.app.evaluator.evaluate(self.proj_theta.get().strip(), calc_mode))
        g = float(self.app.evaluator.evaluate(self.proj_g.get().strip(), calc_mode))
        
        if v0 < 0 or g <= 0:
            raise ValueError("Velocity must be >= 0 and gravity must be > 0")
        
        theta_rad = math.radians(theta_deg)
        return v0, theta_rad, g

    def animate_step(self):
        if not self.is_playing:
            return
            
        mode = self.sim_mode.get()
        if mode == "Projectile Motion":
            try:
                v0, theta, g = self.get_projectile_params()
                t_flight = (2.0 * v0 * math.sin(theta)) / g if math.sin(theta) > 0 else 0.0
                
                if t_flight <= 0:
                    self.proj_t = 0.0
                    self.is_playing = False
                    self.draw_projectile_frame(v0, theta, g, 0.0)
                    return
                
                dt = t_flight / 100.0
                self.proj_t += dt
                
                if self.proj_t >= t_flight:
                    self.proj_t = t_flight
                    self.is_playing = False
                    
                self.draw_projectile_frame(v0, theta, g, t_flight)
                
            except Exception as e:
                self.is_playing = False
                self.show_error(handle_error(e))
                return
        else: # Fourier Wave Builder
            self.fourier_phase += 0.05
            self.draw_fourier_frame()
            
        if self.is_playing:
            self.after_id = self.tab_frame.after(30, self.animate_step)

    def redraw(self):
        mode = self.sim_mode.get()
        if mode == "Projectile Motion":
            try:
                v0, theta, g = self.get_projectile_params()
                t_flight = (2.0 * v0 * math.sin(theta)) / g if math.sin(theta) > 0 else 0.0
                self.draw_projectile_frame(v0, theta, g, t_flight)
            except Exception as e:
                self.canvas.delete("all")
                self.show_error(handle_error(e))
        else:
            self.draw_fourier_frame()

    def draw_grid(self, W, H):
        grid_color = "#222222"
        for x in range(0, W, 50):
            self.canvas.create_line(x, 0, x, H, fill=grid_color)
        for y in range(0, H, 50):
            self.canvas.create_line(0, y, W, y, fill=grid_color)

    def draw_projectile_frame(self, v0, theta, g, t_flight):
        self.canvas.delete("all")
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        if W <= 1: W = 500
        if H <= 1: H = 250
        
        self.canvas.create_rectangle(0, 0, W, H, fill="#111111", outline="")
        self.draw_grid(W, H)
        
        # Max height & range for scaling
        x_max = (v0**2 * math.sin(2.0 * theta)) / g if g > 0 and t_flight > 0 else 1.0
        y_max = (v0 * math.sin(theta))**2 / (2.0 * g) if g > 0 and t_flight > 0 else 1.0
        
        if x_max <= 0: x_max = 1.0
        if y_max <= 0: y_max = 1.0
        
        # Add 20% padding to bounds
        x_bound = x_max * 1.2
        y_bound = y_max * 1.2
        
        margin = 40
        scale_x = (W - 2 * margin) / x_bound
        scale_y = (H - 2 * margin) / y_bound
        scale = min(scale_x, scale_y)
        
        def to_screen(x_phys, y_phys):
            sx = margin + x_phys * scale
            sy = H - margin - y_phys * scale
            return sx, sy
            
        # Draw ground
        gx1, gy1 = to_screen(0, 0)
        gx2, gy2 = to_screen(x_bound, 0)
        self.canvas.create_line(gx1, gy1, W, gy1, fill="#8E8E93", width=2)
        
        # Draw flight trajectory up to current time
        points = []
        n_pts = 100
        t_draw = min(self.proj_t, t_flight)
        dt_draw = t_draw / n_pts if t_draw > 0 else 0.0
        for i in range(n_pts + 1):
            t_curr = i * dt_draw
            px = v0 * math.cos(theta) * t_curr
            py = v0 * math.sin(theta) * t_curr - 0.5 * g * t_curr**2
            if py < 0: py = 0.0
            points.append(to_screen(px, py))
            
        if len(points) > 1:
            flat_pts = [coord for pt in points for coord in pt]
            self.canvas.create_line(flat_pts, fill="#5AC8FA", width=2, dash=(4, 4))
            
        # Draw current projectile position
        curr_x = v0 * math.cos(theta) * self.proj_t
        curr_y = v0 * math.sin(theta) * self.proj_t - 0.5 * g * self.proj_t**2
        if curr_y < 0: curr_y = 0.0
        
        cx, cy = to_screen(curr_x, curr_y)
        self.canvas.create_oval(cx - 6, cy - 6, cx + 6, cy + 6, fill="#FF9500", outline="#FFFFFF", width=1)
        
        vx = v0 * math.cos(theta)
        vy = v0 * math.sin(theta) - g * self.proj_t
        speed = math.sqrt(vx**2 + vy**2)
        
        stats_text = (
            f"Mode: Projectile Motion\n"
            f"Time: {self.proj_t:.2f} s / {t_flight:.2f} s\n"
            f"Position: X = {curr_x:.2f} m, Y = {curr_y:.2f} m\n"
            f"Speed: {speed:.2f} m/s\n"
            f"Max Height: {y_max:.2f} m | Max Range: {x_max:.2f} m"
        )
        self.update_stats_display(stats_text)

    def draw_fourier_frame(self):
        self.canvas.delete("all")
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        if W <= 1: W = 500
        if H <= 1: H = 250
        
        self.canvas.create_rectangle(0, 0, W, H, fill="#111111", outline="")
        self.draw_grid(W, H)
        
        margin = 40
        plot_w = W - 2 * margin
        plot_h = H - 2 * margin
        
        N = self.fourier_terms.get()
        shape = self.fourier_shape.get()
        
        # Collect points for sum
        sum_pts = []
        harmonics_pts = {i: [] for i in range(1, min(N + 1, 4))}
        
        for sx in range(margin, W - margin):
            u = -2.0 * math.pi + 4.0 * math.pi * (sx - margin) / plot_w
            
            y_sum = 0.0
            for k in range(1, N + 1):
                term = 0.0
                if shape == "Square":
                    n = 2 * k - 1
                    term = (4.0 / math.pi) * (math.sin(n * (u + self.fourier_phase)) / n)
                elif shape == "Sawtooth":
                    term = (2.0 / math.pi) * (((-1)**(k+1)) * math.sin(k * (u + self.fourier_phase)) / k)
                elif shape == "Triangle":
                    n = 2 * k - 1
                    term = (8.0 / (math.pi**2)) * (((-1)**(k-1)) * math.sin(n * (u + self.fourier_phase)) / (n**2))
                
                y_sum += term
                if k in harmonics_pts:
                    harmonics_pts[k].append(term)
                    
            sy_sum = H/2 - y_sum * (plot_h / 3.0)
            sum_pts.append((sx, sy_sum))
            
            for k in harmonics_pts:
                term_val = harmonics_pts[k][-1]
                sy_term = H/2 - term_val * (plot_h / 3.0)
                harmonics_pts[k][-1] = (sx, sy_term)
                
        # Draw harmonic components
        colors = ["#3A86F0", "#FF007F", "#8E2DE2"]
        for idx, k in enumerate(sorted(harmonics_pts.keys())):
            pts_list = harmonics_pts[k]
            if len(pts_list) > 1:
                flat_pts = [coord for pt in pts_list for coord in pt]
                self.canvas.create_line(flat_pts, fill=colors[idx % len(colors)], width=1, dash=(2, 2))
                
        # Draw sum wave
        if len(sum_pts) > 1:
            flat_sum = [coord for pt in sum_pts for coord in pt]
            self.canvas.create_line(flat_sum, fill="#30D158", width=3)
            
        stats_text = (
            f"Mode: Fourier Wave Builder\n"
            f"Wave Type: {shape} | Terms (N): {N}\n"
            f"Phase Shift: {self.fourier_phase:.2f} rad\n"
            f"Harmonics: 1st (Blue) | 2nd (Pink) | 3rd (Purple)\n"
            f"Sum Wave: Green (converging to shape)"
        )
        self.update_stats_display(stats_text)
