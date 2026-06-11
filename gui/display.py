"""
Handles calculator display operations.
"""

import tkinter as tk


class Display:
    def __init__(self, parent):
        # Cohesive black screen container
        self.screen_frame = tk.Frame(parent, bg="#000000", bd=5)
        self.screen_frame.pack(fill="x", padx=10, pady=15)

        # Status header row
        self.status_frame = tk.Frame(self.screen_frame, bg="#000000")
        self.status_frame.pack(fill="x", padx=5, pady=(2, 0))

        self.memory_label = tk.Label(
            self.status_frame,
            text="",
            fg="#FF9500",
            bg="#000000",
            font=("Segoe UI", 9, "bold")
        )
        self.memory_label.pack(side="left")

        self.mode_label = tk.Label(
            self.status_frame,
            text="DEG",
            fg="#0A84FF",
            bg="#000000",
            font=("Segoe UI", 9, "bold")
        )
        self.mode_label.pack(side="right")

        self.entry = tk.Entry(
            self.screen_frame,
            justify="right",
            font=("Segoe UI", 22, "bold"),
            bg="#000000",
            fg="#FFFFFF",
            insertbackground="#FFFFFF", # White cursor
            relief="flat",
            bd=5,
            highlightthickness=0
        )
        self.entry.pack(fill="x", padx=5, pady=(0, 5))

    def set_memory_indicator(self, active: bool):
        self.memory_label.config(text="M" if active else "")

    def set_mode_indicator(self, mode: str):
        self.mode_label.config(text=mode)

    def get_text(self):
        return self.entry.get()

    def set_text(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self._on_content_change()

    def clear(self):
        self.entry.delete(0, tk.END)
        self._on_content_change()

    def append(self, value):
        self.entry.insert(tk.END, value)
        self._on_content_change()

    def _on_content_change(self):
        self._adjust_font_size()
        self._update_bracket_highlighting()

    def _adjust_font_size(self):
        text_len = len(self.get_text())
        if text_len <= 15:
            self.entry.config(font=("Segoe UI", 22, "bold"))
        elif text_len <= 22:
            self.entry.config(font=("Segoe UI", 18, "bold"))
        elif text_len <= 30:
            self.entry.config(font=("Segoe UI", 14, "bold"))
        else:
            self.entry.config(font=("Segoe UI", 11, "bold"))

    def _update_bracket_highlighting(self):
        text = self.get_text()
        if '(' not in text and ')' not in text:
            self.entry.config(fg="#FFFFFF")
            return

        open_count = 0
        balanced = True
        for char in text:
            if char == '(':
                open_count += 1
            elif char == ')':
                open_count -= 1
                if open_count < 0:
                    balanced = False
                    break
        if open_count != 0:
            balanced = False

        if balanced:
            self.entry.config(fg="#FFFFFF")
        else:
            self.entry.config(fg="#FFCC00") # Amber warning for unbalanced brackets