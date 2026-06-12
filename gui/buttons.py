"""
Defines calculator button layout and configuration (Improved Version).
"""

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
            "mode": {"bg": "#0A84FF", "fg": "#FFFFFF", "hover": "#30B0FF"},
            "action_clear": {"bg": "#FF3B30", "fg": "#FFFFFF", "hover": "#FF453A"},
            "action_delete": {"bg": "#E04B4B", "fg": "#FFFFFF", "hover": "#FF5E5E"},
            "action_equal": {"bg": "#30D158", "fg": "#FFFFFF", "hover": "#34C759"},
            "action_history": {"bg": "#5856D6", "fg": "#FFFFFF", "hover": "#6D6BF0"},
        }

        # ✅ UPDATED: Added "command" field
        self.button_defs = [
            # Row 0
            {"text": "DEG", "command": "MODE", "row": 0, "col": 0, "category": "mode"},
            {"text": "MC", "command": "MEM_CLEAR", "row": 0, "col": 1, "category": "memory"},
            {"text": "MR", "command": "MEM_RECALL", "row": 0, "col": 2, "category": "memory"},
            {"text": "M+", "command": "MEM_ADD", "row": 0, "col": 3, "category": "memory"},
            {"text": "M-", "command": "MEM_SUB", "row": 0, "col": 4, "category": "memory"},
            {"text": "C", "command": "CLEAR", "row": 0, "col": 5, "category": "action_clear"},
            {"text": "DEL", "command": "DELETE", "row": 0, "col": 6, "category": "action_delete"},

            # Row 1
            {"text": "sin", "row": 1, "col": 0, "category": "scientific"},
            {"text": "cos", "row": 1, "col": 1, "category": "scientific"},
            {"text": "tan", "row": 1, "col": 2, "category": "scientific"},
            {"text": "7", "row": 1, "col": 3, "category": "number"},
            {"text": "8", "row": 1, "col": 4, "category": "number"},
            {"text": "9", "row": 1, "col": 5, "category": "number"},
            {"text": "/", "row": 1, "col": 6, "category": "operator"},

            # Row 2
            {"text": "asin", "row": 2, "col": 0, "category": "scientific"},
            {"text": "acos", "row": 2, "col": 1, "category": "scientific"},
            {"text": "atan", "row": 2, "col": 2, "category": "scientific"},
            {"text": "4", "row": 2, "col": 3, "category": "number"},
            {"text": "5", "row": 2, "col": 4, "category": "number"},
            {"text": "6", "row": 2, "col": 5, "category": "number"},
            {"text": "*", "row": 2, "col": 6, "category": "operator"},

            # Row 3
            {"text": "sinh", "row": 3, "col": 0, "category": "scientific"},
            {"text": "cosh", "row": 3, "col": 1, "category": "scientific"},
            {"text": "tanh", "row": 3, "col": 2, "category": "scientific"},
            {"text": "1", "row": 3, "col": 3, "category": "number"},
            {"text": "2", "row": 3, "col": 4, "category": "number"},
            {"text": "3", "row": 3, "col": 5, "category": "number"},
            {"text": "-", "row": 3, "col": 6, "category": "operator"},

            # Row 4
            {"text": "log", "row": 4, "col": 0, "category": "scientific"},
            {"text": "ln", "row": 4, "col": 1, "category": "scientific"},
            {"text": "sqrt", "row": 4, "col": 2, "category": "scientific"},
            {"text": "0", "row": 4, "col": 3, "category": "number"},
            {"text": ".", "row": 4, "col": 4, "category": "number"},
            {"text": "=", "command": "EQUAL", "row": 4, "col": 5, "category": "action_equal"},
            {"text": "+", "row": 4, "col": 6, "category": "operator"},

            # Row 5
            {"text": "pi", "row": 5, "col": 0, "category": "scientific"},
            {"text": "e", "row": 5, "col": 1, "category": "scientific"},
            {"text": "exp", "row": 5, "col": 2, "category": "scientific"},
            {"text": "^", "row": 5, "col": 3, "category": "scientific"},
            {"text": "!", "row": 5, "col": 4, "category": "scientific"},
            {"text": "(", "row": 5, "col": 5, "category": "scientific"},
            {"text": ")", "row": 5, "col": 6, "category": "scientific"},

            # Row 6
            {"text": "x^2", "row": 6, "col": 0, "category": "scientific"},
            {"text": "x^3", "row": 6, "col": 1, "category": "scientific"},
            {"text": "1/x", "row": 6, "col": 2, "category": "scientific"},
            {"text": "e^x", "row": 6, "col": 3, "category": "scientific"},
            {"text": "THEME", "command": "THEME", "row": 6, "col": 4, "category": "scientific"},
            {"text": "HIST", "command": "TOGGLE_HISTORY", "row": 6, "col": 5, "category": "action_history", "columnspan": 2},
        ]

    def create_buttons(self, click_callback):
        self.widgets = {}

        for btn in self.button_defs:
            text = btn["text"]
            command = btn.get("command", text)  # ✅ key improvement
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
                command=lambda c=command: click_callback(c)
            )

            button.grid(
                row=btn["row"],
                column=btn["col"],
                columnspan=btn.get("columnspan", 1),
                padx=3,
                pady=3,
                sticky="nsew"
            )

            self._bind_hover(button, style["bg"], style["hover"])
            self.widgets[text] = button

        # Responsive grid
        for i in range(7):
            self.parent.columnconfigure(i, weight=1)
            self.parent.rowconfigure(i, weight=1)

    def _bind_hover(self, widget, bg, hover_bg):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=bg))

    def set_layout(self, layout_name):
        for button in self.widgets.values():
            button.grid_forget()
            
        if layout_name == "Basic Focus":
            # Grid only basic buttons in a 4-column layout
            basic_layout = {
                "C": {"row": 0, "col": 0},
                "DEL": {"row": 0, "col": 1},
                "HIST": {"row": 0, "col": 2},
                "/": {"row": 0, "col": 3},
                
                "7": {"row": 1, "col": 0},
                "8": {"row": 1, "col": 1},
                "9": {"row": 1, "col": 2},
                "*": {"row": 1, "col": 3},
                
                "4": {"row": 2, "col": 0},
                "5": {"row": 2, "col": 1},
                "6": {"row": 2, "col": 2},
                "-": {"row": 2, "col": 3},
                
                "1": {"row": 3, "col": 0},
                "2": {"row": 3, "col": 1},
                "3": {"row": 3, "col": 2},
                "+": {"row": 3, "col": 3},
                
                "0": {"row": 4, "col": 0, "colspan": 2},
                ".": {"row": 4, "col": 2},
                "=": {"row": 4, "col": 3},
            }
            
            for text, grid_info in basic_layout.items():
                if text in self.widgets:
                    colspan = grid_info.get("colspan", 1)
                    self.widgets[text].grid(
                        row=grid_info["row"],
                        column=grid_info["col"],
                        columnspan=colspan,
                        padx=3,
                        pady=3,
                        sticky="nsew"
                    )
            
            for i in range(7):
                if i < 4:
                    self.parent.columnconfigure(i, weight=1)
                else:
                    self.parent.columnconfigure(i, weight=0)
            for i in range(7):
                if i < 5:
                    self.parent.rowconfigure(i, weight=1)
                else:
                    self.parent.rowconfigure(i, weight=0)
        else:
            # Standard Scientific Layout
            for btn in self.button_defs:
                text = btn["text"]
                if text in self.widgets:
                    self.widgets[text].grid(
                        row=btn["row"],
                        column=btn["col"],
                        columnspan=btn.get("columnspan", 1),
                        padx=3,
                        pady=3,
                        sticky="nsew"
                    )
            for i in range(7):
                self.parent.columnconfigure(i, weight=1)
                self.parent.rowconfigure(i, weight=1)