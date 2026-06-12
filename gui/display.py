"""
Improved Display System - Smart, Responsive, Professional
"""

import tkinter as tk


class Display:
    def __init__(self, parent):
        self.last_was_result = False

        # Main screen
        self.screen_frame = tk.Frame(parent, bg="#000000", bd=5)
        self.screen_frame.pack(fill="x", padx=10, pady=15)

        # Status row
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

        # Main entry
        self.entry = tk.Entry(
            self.screen_frame,
            justify="right",
            font=("Segoe UI", 22, "bold"),
            bg="#000000",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            relief="flat",
            bd=5
        )
        self.entry.pack(fill="x", padx=5, pady=(0, 5))

    # ---------------------------
    # STATE INDICATORS
    # ---------------------------
    def set_memory_indicator(self, active: bool):
        self.memory_label.config(text="M" if active else "")

    def set_mode_indicator(self, mode: str):
        self.mode_label.config(text=mode)

    # ---------------------------
    # TEXT OPERATIONS
    # ---------------------------
    def get_text(self):
        return self.entry.get()

    def set_text(self, text, is_result=False):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.last_was_result = is_result
        self._on_content_change()

    def clear(self):
        self.entry.delete(0, tk.END)
        self.last_was_result = False
        self._on_content_change()

    def append(self, value):
        # If last was result → replace instead of append
        if self.last_was_result:
            self.clear()

        self.entry.insert(tk.END, value)
        self.last_was_result = False
        self._on_content_change()

    def insert_at_cursor(self, value):
        pos = self.entry.index(tk.INSERT)
        self.entry.insert(pos, value)
        self.last_was_result = False
        self._on_content_change()

    # ---------------------------
    # ERROR DISPLAY
    # ---------------------------
    def show_error(self, message):
        self.set_text(message)
        self.entry.config(fg="#FF3B30")  # red
        self.last_was_result = True

    def show_normal(self):
        self.entry.config(fg="#FFFFFF")

    # ---------------------------
    # AUTO UI UPDATES
    # ---------------------------
    def _on_content_change(self):
        self._adjust_font_size()
        self._update_bracket_highlighting()

    def _adjust_font_size(self):
        text_len = len(self.get_text())

        if text_len <= 15:
            size = 22
        elif text_len <= 22:
            size = 18
        elif text_len <= 30:
            size = 14
        else:
            size = 11

        self.entry.config(font=("Segoe UI", size, "bold"))

    def _update_bracket_highlighting(self):
        text = self.get_text()

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
            self.entry.config(fg="#FFCC00")  # warning