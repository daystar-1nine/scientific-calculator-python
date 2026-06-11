"""
Defines calculator button layout and configuration.
"""

import tkinter as tk


import tkinter as tk


class ButtonPanel:
    def __init__(self, parent):
        self.parent = parent

        # iOS-like premium dark mode colors
        self.colors = {
            "number": {"bg": "#2C2C2E", "fg": "#FFFFFF", "hover": "#3A3A3C"},
            "operator": {"bg": "#FF9500", "fg": "#FFFFFF", "hover": "#FFAC33"},
            "scientific": {"bg": "#48484A", "fg": "#E5E5EA", "hover": "#636366"},
            "memory": {"bg": "#3A3A3C", "fg": "#D1D1D6", "hover": "#48484A"},
            "mode": {"bg": "#0A84FF", "fg": "#FFFFFF", "hover": "#30B0FF"}, # Accent blue
            "action_clear": {"bg": "#FF3B30", "fg": "#FFFFFF", "hover": "#FF453A"}, # Vibrant red
            "action_delete": {"bg": "#E04B4B", "fg": "#FFFFFF", "hover": "#FF5E5E"}, # Soft red
            "action_equal": {"bg": "#30D158", "fg": "#FFFFFF", "hover": "#34C759"}, # Green
            "action_history": {"bg": "#5856D6", "fg": "#FFFFFF", "hover": "#6D6BF0"}, # Purple
        }

        # Button definitions mapping labels, grids, and styling category
        self.button_defs = [
            # Row 0: Mode, Memory, Clear
            {"text": "DEG", "row": 0, "col": 0, "category": "mode"},
            {"text": "MC", "row": 0, "col": 1, "category": "memory"},
            {"text": "MR", "row": 0, "col": 2, "category": "memory"},
            {"text": "M+", "row": 0, "col": 3, "category": "memory"},
            {"text": "M-", "row": 0, "col": 4, "category": "memory"},
            {"text": "C", "row": 0, "col": 5, "category": "action_clear"},
            
            # Row 1: Trig, Numbers, Division
            {"text": "sin", "row": 1, "col": 0, "category": "scientific"},
            {"text": "cos", "row": 1, "col": 1, "category": "scientific"},
            {"text": "7", "row": 1, "col": 2, "category": "number"},
            {"text": "8", "row": 1, "col": 3, "category": "number"},
            {"text": "9", "row": 1, "col": 4, "category": "number"},
            {"text": "/", "row": 1, "col": 5, "category": "operator"},
            
            # Row 2: Trig/Sqrt, Numbers, Multiplication
            {"text": "tan", "row": 2, "col": 0, "category": "scientific"},
            {"text": "sqrt", "row": 2, "col": 1, "category": "scientific"},
            {"text": "4", "row": 2, "col": 2, "category": "number"},
            {"text": "5", "row": 2, "col": 3, "category": "number"},
            {"text": "6", "row": 2, "col": 4, "category": "number"},
            {"text": "*", "row": 2, "col": 5, "category": "operator"},
            
            # Row 3: Logarithms, Numbers, Subtraction
            {"text": "log", "row": 3, "col": 0, "category": "scientific"},
            {"text": "ln", "row": 3, "col": 1, "category": "scientific"},
            {"text": "1", "row": 3, "col": 2, "category": "number"},
            {"text": "2", "row": 3, "col": 3, "category": "number"},
            {"text": "3", "row": 3, "col": 4, "category": "number"},
            {"text": "-", "row": 3, "col": 5, "category": "operator"},
            
            # Row 4: Constants, Parentheses, Backspace, Addition
            {"text": "pi", "row": 4, "col": 0, "category": "scientific"},
            {"text": "e", "row": 4, "col": 1, "category": "scientific"},
            {"text": "(", "row": 4, "col": 2, "category": "scientific"},
            {"text": ")", "row": 4, "col": 3, "category": "scientific"},
            {"text": "DEL", "row": 4, "col": 4, "category": "action_delete"},
            {"text": "+", "row": 4, "col": 5, "category": "operator"},
            
            # Row 5: Powers, Factorial, Numbers, Equals, History
            {"text": "^", "row": 5, "col": 0, "category": "scientific"},
            {"text": "!", "row": 5, "col": 1, "category": "scientific"},
            {"text": "0", "row": 5, "col": 2, "category": "number"},
            {"text": ".", "row": 5, "col": 3, "category": "number"},
            {"text": "=", "row": 5, "col": 4, "category": "action_equal"},
            {"text": "HIST", "row": 5, "col": 5, "category": "action_history"},
        ]

    def create_buttons(self, click_callback):
        self.widgets = {}
        for btn in self.button_defs:
            text = btn["text"]
            cat = btn["category"]
            style = self.colors.get(cat, self.colors["number"])
            
            button = tk.Button(
                self.parent,
                text=text,
                bg=style["bg"],
                fg=style["fg"],
                font=("Segoe UI", 11, "bold"),
                bd=0,
                relief="flat",
                activebackground=style["hover"],
                activeforeground=style["fg"],
                width=5,
                height=2,
                command=lambda t=text: click_callback(t)
            )
            button.grid(row=btn["row"], column=btn["col"], padx=3, pady=3, sticky="nsew")
            
            # Hover bindings
            self._bind_hover(button, style["bg"], style["hover"])
            self.widgets[text] = button

        # Configure columns and rows to be responsive
        for i in range(6):
            self.parent.columnconfigure(i, weight=1)
            self.parent.rowconfigure(i, weight=1)

    def _bind_hover(self, widget, bg, hover_bg):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=bg))