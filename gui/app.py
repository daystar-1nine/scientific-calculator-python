"""
Main calculator window.
"""

import tkinter as tk

from gui.display import Display
from gui.buttons import ButtonPanel


from gui.display import Display
from gui.buttons import ButtonPanel
from core.evaluator import Evaluator
from core.modes import CalculatorMode
from features.memory import Memory
from features.history import History
from utils.error_handler import handle_error


class CalculatorApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Scientific Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # State Managers
        self.evaluator = Evaluator()
        self.mode_manager = CalculatorMode()
        self.memory = Memory()
        self.history = History()

        # GUI Setup
        self.root.configure(bg="#1C1C1E")

        # Main layout container
        self.main_frame = tk.Frame(self.root, bg="#1C1C1E")
        self.main_frame.pack(fill="both", expand=True)

        # Left side: Calculator keys and display
        self.calc_frame = tk.Frame(self.main_frame, bg="#1C1C1E", width=400)
        self.calc_frame.pack(side="left", fill="both", expand=True)

        # Display
        self.display = Display(self.calc_frame)

        # Button frame
        self.button_frame = tk.Frame(self.calc_frame, bg="#1C1C1E")
        self.button_frame.pack(fill="both", expand=True, padx=8, pady=8)

        self.buttons = ButtonPanel(self.button_frame)
        self.buttons.create_buttons(self.on_button_click)

        # Sync the mode button text with default
        self.update_mode_button_text()

        # Right side: History frame (initially hidden)
        self.history_frame = tk.Frame(self.main_frame, bg="#2C2C2E", width=250)
        self.history_visible = False

        history_title = tk.Label(
            self.history_frame,
            text="History Log",
            fg="#FFFFFF",
            bg="#2C2C2E",
            font=("Segoe UI", 12, "bold")
        )
        history_title.pack(pady=12)

        # Scrollable listbox for history
        list_frame = tk.Frame(self.history_frame, bg="#2C2C2E")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.history_scrollbar = tk.Scrollbar(list_frame)
        self.history_scrollbar.pack(side="right", fill="y")

        self.history_listbox = tk.Listbox(
            list_frame,
            bg="#1C1C1E",
            fg="#FFFFFF",
            selectbackground="#FF9500",
            selectforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            highlightthickness=0,
            yscrollcommand=self.history_scrollbar.set
        )
        self.history_listbox.pack(side="left", fill="both", expand=True)
        self.history_scrollbar.config(command=self.history_listbox.yview)

        # Bind listbox selection event
        self.history_listbox.bind("<<ListboxSelect>>", self.on_history_select)

        # Clear history button
        clear_hist_btn = tk.Button(
            self.history_frame,
            text="Clear History",
            bg="#FF3B30",
            fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            relief="flat",
            activebackground="#FF453A",
            activeforeground="#FFFFFF",
            height=2,
            command=self.clear_history
        )
        clear_hist_btn.pack(fill="x", padx=10, pady=10)

    def on_button_click(self, char):
        current_text = self.display.get_text()

        # Handle clear
        if char == "C":
            self.display.clear()

        # Handle backspace
        elif char == "DEL":
            self.display.set_text(current_text[:-1])

        # Handle Mode Toggle
        elif char == "DEG":
            mode = self.mode_manager.get_mode()
            if mode == CalculatorMode.DEGREE:
                self.mode_manager.set_radian()
            else:
                self.mode_manager.set_degree()
            self.update_mode_button_text()

        # Handle Memory operations
        elif char == "MC":
            self.memory.clear()
        elif char == "MR":
            val = self.memory.recall()
            self.display.append(self.format_result(val))
        elif char == "M+":
            if current_text:
                try:
                    res = self.evaluator.evaluate(current_text, self.mode_manager.get_mode())
                    self.memory.add(res)
                except Exception as e:
                    self.display.set_text(handle_error(e))
        elif char == "M-":
            if current_text:
                try:
                    res = self.evaluator.evaluate(current_text, self.mode_manager.get_mode())
                    self.memory.subtract(res)
                except Exception as e:
                    self.display.set_text(handle_error(e))

        # Handle History toggle
        elif char == "HIST":
            self.toggle_history()

        # Handle Equal evaluation
        elif char == "=":
            if not current_text:
                return
            try:
                raw_res = self.evaluator.evaluate(current_text, self.mode_manager.get_mode())
                formatted_res = self.format_result(raw_res)
                self.display.set_text(formatted_res)
                self.history.add_entry(current_text, formatted_res)
                if self.history_visible:
                    self.update_history_display()
            except Exception as e:
                self.display.set_text(handle_error(e))

        # Handle Scientific functions (append opening parenthesis)
        elif char in ["sin", "cos", "tan", "log", "ln", "sqrt"]:
            self.display.append(f"{char}(")

        # Standard append
        else:
            self.display.append(char)

    def update_mode_button_text(self):
        mode = self.mode_manager.get_mode()
        # Find the mode button and update its text
        if hasattr(self.buttons, "widgets") and "DEG" in self.buttons.widgets:
            self.buttons.widgets["DEG"].config(text=mode)

    def toggle_history(self):
        if self.history_visible:
            self.history_frame.pack_forget()
            self.root.geometry("400x500")
            self.history_visible = False
        else:
            self.root.geometry("650x500")
            self.history_frame.pack(side="right", fill="both", expand=True)
            self.update_history_display()
            self.history_visible = True

    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        for entry in self.history.get_history():
            self.history_listbox.insert(tk.END, entry)
        self.history_listbox.yview_moveto(1.0)

    def clear_history(self):
        self.history.clear_history()
        self.update_history_display()

    def on_history_select(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            idx = selection[0]
            entry_text = self.history_listbox.get(idx)
            if " = " in entry_text:
                expr = entry_text.split(" = ")[0]
                self.display.set_text(expr)

    def format_result(self, value):
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            res = f"{value:.10f}".rstrip('0').rstrip('.')
            if abs(value) > 1e12 or (abs(value) < 1e-10 and value != 0):
                return f"{value:.6e}"
            return res
        return str(value)

    def run(self):
        self.root.mainloop()