"""
Handles calculator display operations.
"""

import tkinter as tk


class Display:
    def __init__(self, parent):
        self.entry = tk.Entry(
            parent,
            justify="right",
            font=("Segoe UI", 22, "bold"),
            bg="#000000",
            fg="#FFFFFF",
            insertbackground="#FFFFFF", # White cursor
            relief="flat",
            bd=10,                      # Simulated inner padding
            highlightthickness=0
        )
        self.entry.pack(fill="x", padx=10, pady=15)

    def get_text(self):
        return self.entry.get()

    def set_text(self, text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)

    def clear(self):
        self.entry.delete(0, tk.END)

    def append(self, value):
        self.entry.insert(tk.END, value)