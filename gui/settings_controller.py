"""
Controller for the Settings, Themes, and Exporters tab.
"""

import tkinter as tk
from tkinter import filedialog
from utils.error_handler import handle_error

class SettingsController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.current_theme = tk.StringVar(value="Midnight")
        
        self.themes = {
            "Midnight": {
                "bg": "#1C1C1E",
                "sidebar_bg": "#2C2C2E",
                "entry_bg": "#1C1C1E",
                "fg": "#FFFFFF",
                "btn_bg": "#48484A",
                "btn_fg": "#FFFFFF",
                "orange_btn": "#FF9500",
                "green_btn": "#30D158",
                "red_btn": "#FF3B30"
            },
            "Casio Classic": {
                "bg": "#E5E5EA",
                "sidebar_bg": "#D1D1D6",
                "entry_bg": "#FFFFFF",
                "fg": "#000000",
                "btn_bg": "#C7C7CC",
                "btn_fg": "#000000",
                "orange_btn": "#FF9500",
                "green_btn": "#34C759",
                "red_btn": "#FF3B30"
            },
            "Cyberpunk": {
                "bg": "#000000",
                "sidebar_bg": "#150020",
                "entry_bg": "#000000",
                "fg": "#00FF00",
                "btn_bg": "#250035",
                "btn_fg": "#00FF00",
                "orange_btn": "#FF007F",
                "green_btn": "#00FFFF",
                "red_btn": "#FF3333"
            },
            "Arctic Frost": {
                "bg": "#E4EBF5",
                "sidebar_bg": "#D2DFEE",
                "entry_bg": "#E4EBF5",
                "fg": "#1C1C1E",
                "btn_bg": "#B8C9DC",
                "btn_fg": "#1C1C1E",
                "orange_btn": "#007AFF",
                "green_btn": "#5AC8FA",
                "red_btn": "#FF3B30"
            }
        }

        self.setup_ui()

    def setup_ui(self):
        # 1. Theme Selection Frame
        theme_frame = tk.LabelFrame(
            self.tab_frame, text="Appearance Theme", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), padx=10, pady=10
        )
        theme_frame.pack(fill="x", padx=10, pady=10)

        theme_lbl = tk.Label(theme_frame, text="Select Theme:", fg="#D1D1D6", bg="#2C2C2E", font=("Segoe UI", 8, "bold"))
        theme_lbl.pack(side="left", padx=(0, 10))

        theme_menu = tk.OptionMenu(
            theme_frame,
            self.current_theme,
            *self.themes.keys(),
            command=self.change_theme
        )
        theme_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        theme_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        theme_menu.pack(side="left", fill="x", expand=True)

        # 2. Exporters Frame
        export_frame = tk.LabelFrame(
            self.tab_frame, text="Data Exporters", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), padx=10, pady=10
        )
        export_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(
            export_frame, text="Export Calculation History", bg="#FF9500", fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=0, relief="flat", height=2,
            command=self.export_history
        ).pack(fill="x", pady=5)

        # 3. Status/About display
        status_lbl = tk.Label(
            self.tab_frame, text="Status Output:", fg="#8E8E93", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold"), anchor="w"
        )
        status_lbl.pack(fill="x", padx=10, pady=(15, 2))

        self.status_text = tk.Text(
            self.tab_frame, bg="#1C1C1E", fg="#30D158",
            font=("Consolas", 10, "bold"), height=5, bd=0, highlightthickness=0,
            padx=10, pady=10
        )
        self.status_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.status_text.insert(tk.END, "Engine is ready.")
        self.status_text.config(state="disabled")

    def show_status(self, msg):
        self.status_text.config(state="normal")
        self.status_text.delete("1.0", tk.END)
        self.status_text.insert(tk.END, msg)
        self.status_text.config(state="disabled")

    # --- Themes core painter ---
    def change_theme(self, theme_name):
        theme = self.themes[theme_name]
        try:
            self.app.root.configure(bg=theme["bg"])
            self.app.main_frame.configure(bg=theme["bg"])
            self.app.calc_frame.configure(bg=theme["bg"])
            self.app.button_frame.configure(bg=theme["bg"])
            self.app.sidebar_frame.configure(bg=theme["sidebar_bg"])
            self.app.sidebar_tabs_frame.configure(bg=theme["sidebar_bg"])
            self.app.sidebar_content_frame.configure(bg=theme["sidebar_bg"])
            self.app.tab_selector.config(bg=theme["orange_btn"], activebackground=theme["orange_btn"])

            self.update_widget_colors(self.app.root, theme)
            
            # Force Display Redraw
            self.app.display.set_mode_indicator(self.app.mode_manager.get_mode())
            self.show_status(f"Theme successfully toggled to {theme_name}.")
        except Exception as e:
            self.show_status(f"Theme paint error:\n{handle_error(e)}")

    def update_widget_colors(self, widget, theme):
        class_name = widget.winfo_class()
        try:
            if class_name in ["Frame", "LabelFrame"]:
                is_sidebar = False
                parent = widget
                while parent:
                    if parent == self.app.sidebar_frame:
                        is_sidebar = True
                        break
                    parent = parent.master
                bg = theme["sidebar_bg"] if is_sidebar else theme["bg"]
                widget.configure(bg=bg)
                if class_name == "LabelFrame":
                    widget.configure(fg=theme["fg"])

            elif class_name == "Label":
                is_sidebar = False
                parent = widget
                while parent:
                    if parent == self.app.sidebar_frame:
                        is_sidebar = True
                        break
                    parent = parent.master
                bg = theme["sidebar_bg"] if is_sidebar else theme["bg"]
                
                # Check for special display indicators to not wipe their color highlights
                curr_fg = widget.cget("fg")
                if curr_fg in ["#30D158", "#FF9500", "#FF3B30", "#00FF00", "#FF007F", "#00FFFF", "#34C759", "#34c759", "#30d158"]:
                    # Keep highlight but match background
                    widget.configure(bg=bg)
                else:
                    widget.configure(bg=bg, fg=theme["fg"])

            elif class_name in ["Entry", "Text"]:
                widget.configure(bg=theme["entry_bg"], fg=theme["fg"])
                if hasattr(widget, "config"):
                    try:
                        widget.config(insertbackground=theme["fg"])
                    except Exception:
                        pass

            elif class_name == "Button":
                curr_bg = widget.cget("bg")
                if curr_bg in ["#FF9500", "#FF8F00", "#ff9500", "#ff8f00"]:
                    widget.configure(bg=theme["orange_btn"], fg=theme["btn_fg"])
                elif curr_bg in ["#30D158", "#34C759", "#30d158", "#34c759", "#00FFFF", "#00ffff"]:
                    widget.configure(bg=theme["green_btn"], fg=theme["btn_fg"])
                elif curr_bg in ["#FF3B30", "#FF453A", "#ff3b30", "#ff453a", "#FF3333", "#ff3333"]:
                    widget.configure(bg=theme["red_btn"], fg=theme["btn_fg"])
                else:
                    widget.configure(bg=theme["btn_bg"], fg=theme["btn_fg"])

            elif class_name == "Canvas":
                widget.configure(bg=theme["entry_bg"])

            elif class_name == "Listbox":
                widget.configure(bg=theme["entry_bg"], fg=theme["fg"])

            elif class_name == "Scrollbar":
                widget.configure(bg=theme["sidebar_bg"])

        except Exception:
            pass

        for child in widget.winfo_children():
            self.update_widget_colors(child, theme)

    # --- Data History Exporter ---
    def export_history(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("CSV File", "*.csv")],
            title="Export History Log"
        )
        if not filepath:
            return

        try:
            history_entries = self.app.history.get_history()
            is_csv = filepath.lower().endswith(".csv")

            with open(filepath, "w", encoding="utf-8") as f:
                if is_csv:
                    f.write("Expression,Result\n")
                    for entry in history_entries:
                        if " = " in entry:
                            expr, res = entry.split(" = ", 1)
                            # Escape double quotes for csv format
                            expr_esc = expr.replace('"', '""')
                            res_esc = res.replace('"', '""')
                            f.write(f'"{expr_esc}","{res_esc}"\n')
                else:
                    for entry in history_entries:
                        f.write(f"{entry}\n")

            self.show_status(f"History successfully exported to:\n{filepath}")
        except Exception as e:
            self.show_status(f"Export failed:\n{handle_error(e)}")
