"""
Main calculator window.
"""

import math
import tkinter as tk

from gui.display import Display
from gui.buttons import ButtonPanel
from gui.converter_controller import ConverterController
from gui.graph_controller import GraphController
from gui.matrix_controller import MatrixController
from gui.solver_controller import SolverController
from gui.stats_controller import StatsController
from gui.programmer_controller import ProgrammerController
from gui.variables_controller import VariablesController
from core.evaluator import Evaluator
from core.modes import CalculatorMode
from features.memory import Memory
from features.history import History
from utils.error_handler import handle_error


class CalculatorApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Scientific Calculator")
        self.root.geometry("480x550")
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
        self.calc_frame = tk.Frame(self.main_frame, bg="#1C1C1E", width=480)
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

        # Right side: Sidebar frame (initially hidden)
        self.sidebar_frame = tk.Frame(self.main_frame, bg="#2C2C2E", width=280)
        self.sidebar_visible = False

        # Tab switch headers (using a premium OptionMenu to support multiple new tools)
        self.sidebar_tabs_frame = tk.Frame(self.sidebar_frame, bg="#2C2C2E")
        self.sidebar_tabs_frame.pack(fill="x", padx=5, pady=5)

        self.active_tab = "History"
        self.tab_selector_var = tk.StringVar(value="History")
        self.tab_selector = tk.OptionMenu(
            self.sidebar_tabs_frame,
            self.tab_selector_var,
            "History", "Grapher", "Converter", "Matrix", "Solver", "Stats", "Base-N", "Vars/Consts", "Guide",
            command=self.switch_sidebar_tab
        )
        self.tab_selector.config(
            bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 10, "bold"),
            bd=0, relief="flat", highlightthickness=0, activebackground="#FF9500", activeforeground="#FFFFFF"
        )
        self.tab_selector["menu"].config(
            bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            activebackground="#FF9500", activeforeground="#FFFFFF", bd=0
        )
        self.tab_selector.pack(fill="x", padx=5, pady=5)

        # Tabs container
        self.sidebar_content_frame = tk.Frame(self.sidebar_frame, bg="#2C2C2E")
        self.sidebar_content_frame.pack(fill="both", expand=True)

        # Create Tab Frames (original + new)
        self.tab_history = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_graph = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_conv = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_matrix = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_solver = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_stats = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_programmer = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_variables = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_guide = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")

        # --- 1. History Tab Widgets ---
        list_frame = tk.Frame(self.tab_history, bg="#2C2C2E")
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
            self.tab_history,
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

        # --- 2. Grapher Tab (Managed by Controller) ---
        self.graph_controller = GraphController(self, self.tab_graph)

        # --- 3. Converter Tab (Managed by Controller) ---
        self.converter_controller = ConverterController(self, self.tab_conv)

        # --- 4. Matrix Tab (Managed by Controller) ---
        self.matrix_controller = MatrixController(self, self.tab_matrix)

        # --- 5. Solver Tab (Managed by Controller) ---
        self.solver_controller = SolverController(self, self.tab_solver)

        # --- 6. Stats Tab (Managed by Controller) ---
        self.stats_controller = StatsController(self, self.tab_stats)

        # --- 7. Programmer Tab (Managed by Controller) ---
        self.programmer_controller = ProgrammerController(self, self.tab_programmer)

        # --- 8. Variables Tab (Managed by Controller) ---
        self.variables_controller = VariablesController(self, self.tab_variables)

        # --- 4. Guide Tab Widgets ---
        help_text_frame = tk.Frame(self.tab_guide, bg="#2C2C2E")
        help_text_frame.pack(fill="both", expand=True, padx=10, pady=5)

        guide_scrollbar = tk.Scrollbar(help_text_frame)
        guide_scrollbar.pack(side="right", fill="y")

        self.help_text = tk.Text(
            help_text_frame,
            bg="#1C1C1E",
            fg="#FFFFFF",
            font=("Segoe UI", 9),
            wrap="word",
            bd=0,
            highlightthickness=0,
            yscrollcommand=guide_scrollbar.set
        )
        self.help_text.pack(side="left", fill="both", expand=True)
        guide_scrollbar.config(command=self.help_text.yview)

        self.populate_guide_text()
        self.help_text.config(state="disabled")

        # Bind physical keyboard events
        self.root.bind("<Key>", self.on_key_press)

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
            self.update_memory_indicator()
        elif char == "MR":
            val = self.memory.recall()
            self.display.append(self.format_result(val))
        elif char == "M+":
            if current_text:
                try:
                    vars_dict = {}
                    if hasattr(self, "variables_controller"):
                        vars_dict = self.variables_controller.get_variables_dict()
                    res = self.evaluator.evaluate(current_text, self.mode_manager.get_mode(), variables=vars_dict)
                    self.memory.add(res)
                    self.update_memory_indicator()
                except Exception as e:
                    self.display.set_text(handle_error(e))
        elif char == "M-":
            if current_text:
                try:
                    vars_dict = {}
                    if hasattr(self, "variables_controller"):
                        vars_dict = self.variables_controller.get_variables_dict()
                    res = self.evaluator.evaluate(current_text, self.mode_manager.get_mode(), variables=vars_dict)
                    self.memory.subtract(res)
                    self.update_memory_indicator()
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
                vars_dict = {}
                if hasattr(self, "variables_controller"):
                    vars_dict = self.variables_controller.get_variables_dict()
                raw_res = self.evaluator.evaluate(current_text, self.mode_manager.get_mode(), variables=vars_dict)
                formatted_res = self.format_result(raw_res)
                self.display.set_text(formatted_res)
                self.history.add_entry(current_text, formatted_res)
                if self.sidebar_visible and self.active_tab == "History":
                    self.update_history_display()
            except Exception as e:
                self.display.set_text(handle_error(e))

        # Handle Scientific functions (append opening parenthesis)
        elif char in ["sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "exp", "log", "ln", "sqrt"]:
            self.display.append(f"{char}(")

        # Handle advanced power keys
        elif char == "x^2":
            self.display.append("^2")
        elif char == "x^3":
            self.display.append("^3")
        elif char == "1/x":
            self.display.append("1/(")
        elif char == "e^x":
            self.display.append("e^")

        # Standard append
        else:
            self.display.append(char)

    def update_mode_button_text(self):
        mode = self.mode_manager.get_mode()
        # Find the mode button and update its text
        if hasattr(self.buttons, "widgets") and "DEG" in self.buttons.widgets:
            self.buttons.widgets["DEG"].config(text=mode)
        # Update display screen mode indicator
        self.display.set_mode_indicator(mode)

    def update_memory_indicator(self):
        has_value = self.memory.recall() != 0.0
        self.display.set_memory_indicator(has_value)

    def toggle_history(self):
        if self.sidebar_visible:
            self.sidebar_frame.pack_forget()
            self.root.geometry("480x550")
            self.sidebar_visible = False
        else:
            self.root.geometry("760x550")
            self.sidebar_frame.pack(side="right", fill="both", expand=True)
            self.switch_sidebar_tab(self.active_tab)
            self.sidebar_visible = True

    def switch_sidebar_tab(self, tab_name):
        self.active_tab = tab_name
        self.tab_selector_var.set(tab_name)

        # Unpack all frames
        self.tab_history.pack_forget()
        self.tab_graph.pack_forget()
        self.tab_conv.pack_forget()
        self.tab_matrix.pack_forget()
        self.tab_solver.pack_forget()
        self.tab_stats.pack_forget()
        self.tab_programmer.pack_forget()
        self.tab_variables.pack_forget()
        self.tab_guide.pack_forget()

        # Switch and perform actions
        if tab_name == "History":
            self.tab_history.pack(fill="both", expand=True)
            self.update_history_display()
        elif tab_name == "Grapher":
            self.tab_graph.pack(fill="both", expand=True)
            self.graph_controller.plot_function()
        elif tab_name == "Converter":
            self.tab_conv.pack(fill="both", expand=True)
            self.converter_controller.run_conversion()
        elif tab_name == "Matrix":
            self.tab_matrix.pack(fill="both", expand=True)
        elif tab_name == "Solver":
            self.tab_solver.pack(fill="both", expand=True)
        elif tab_name == "Stats":
            self.tab_stats.pack(fill="both", expand=True)
        elif tab_name == "Base-N":
            self.tab_programmer.pack(fill="both", expand=True)
        elif tab_name == "Vars/Consts":
            self.tab_variables.pack(fill="both", expand=True)
        elif tab_name == "Guide":
            self.tab_guide.pack(fill="both", expand=True)

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




    def on_key_press(self, event):
        char = event.char
        keysym = event.keysym

        if not char and keysym:
            if keysym.isdigit():
                char = keysym
            elif keysym == "plus":
                char = "+"
            elif keysym == "minus":
                char = "-"
            elif keysym == "asterisk":
                char = "*"
            elif keysym == "slash":
                char = "/"
            elif keysym == "parenleft":
                char = "("
            elif keysym == "parenright":
                char = ")"
            elif keysym == "exclam":
                char = "!"
            elif keysym == "asciicircum":
                char = "^"
            elif keysym == "period":
                char = "."

        if keysym in ["Return", "KP_Enter"]:
            self.on_button_click("=")
            return "break"
        elif keysym == "BackSpace":
            self.on_button_click("DEL")
            return "break"
        elif keysym == "Escape":
            self.on_button_click("C")
            return "break"
        elif char in "0123456789.+-*/^!()":
            self.on_button_click(char)
            return "break"

    def format_result(self, value):
        if isinstance(value, complex):
            real_val = value.real
            imag_val = value.imag
            if abs(real_val) < 1e-15:
                real_val = 0.0
            if abs(imag_val) < 1e-15:
                imag_val = 0.0

            if imag_val == 0.0:
                return self.format_result(real_val)
            if real_val == 0.0:
                if imag_val == 1.0:
                    return "i"
                if imag_val == -1.0:
                    return "-i"
                return f"{self.format_result(imag_val)}i"
            
            real_str = self.format_result(real_val)
            sign = "+" if imag_val > 0 else "-"
            abs_imag = abs(imag_val)
            if abs_imag == 1.0:
                imag_str = "i"
            else:
                imag_str = f"{self.format_result(abs_imag)}i"
            return f"{real_str} {sign} {imag_str}"

        if isinstance(value, int) and not isinstance(value, bool):
            if abs(value) > 1e12:
                s = str(value)
                sign = "-" if s[0] == "-" else ""
                digits = s.lstrip("-")
                exponent = len(digits) - 1
                mantissa = digits[0] + "." + digits[1:7]
                mantissa = mantissa.rstrip('0').rstrip('.')
                return f"{sign}{mantissa}e+{exponent}"
            return str(value)

        if isinstance(value, float):
            if value.is_integer():
                return self.format_result(int(value))
            res = f"{value:.10f}".rstrip('0').rstrip('.')
            if abs(value) > 1e12 or (abs(value) < 1e-10 and value != 0):
                return f"{value:.6e}"
            return res
        return str(value)

    def populate_guide_text(self):
        # Configure tags for beautiful layout styling
        self.help_text.tag_config("heading", font=("Segoe UI", 11, "bold"), foreground="#FF9500")
        self.help_text.tag_config("section", font=("Segoe UI", 10, "bold"), foreground="#30D158")
        self.help_text.tag_config("bullet", font=("Segoe UI", 9), lmargin1=10, lmargin2=20)
        
        self.help_text.insert(tk.END, " SCIENTIFIC CALCULATOR GUIDE\n\n", "heading")
        
        self.help_text.insert(tk.END, "⌨️ Keyboard Shortcuts\n", "section")
        self.help_text.insert(tk.END, "• Enter / Return  =>  Evaluate (=)\n", "bullet")
        self.help_text.insert(tk.END, "• Backspace       =>  Delete last char (DEL)\n", "bullet")
        self.help_text.insert(tk.END, "• Escape          =>  Clear display (C)\n", "bullet")
        self.help_text.insert(tk.END, "• 0-9, ., +, -, *, /, ^, (, ) => Standard keys\n\n", "bullet")
        
        self.help_text.insert(tk.END, "📐 Trigonometric Modes\n", "section")
        self.help_text.insert(tk.END, "• Toggle DEG/RAD mode using the blue mode button.\n", "bullet")
        self.help_text.insert(tk.END, "• Trigonometric functions (sin, cos, tan) and inverse functions (asin, acos, atan) automatically respect the active mode.\n\n", "bullet")
        
        self.help_text.insert(tk.END, "🧠 Memory Operations\n", "section")
        self.help_text.insert(tk.END, "• MC  =>  Clear memory\n", "bullet")
        self.help_text.insert(tk.END, "• MR  =>  Recall memory to display\n", "bullet")
        self.help_text.insert(tk.END, "• M+  =>  Add current expression result to memory\n", "bullet")
        self.help_text.insert(tk.END, "• M-  =>  Subtract current expression result from memory\n", "bullet")
        self.help_text.insert(tk.END, "• 'M' indicator appears on screen when memory is non-zero.\n\n", "bullet")
        
        self.help_text.insert(tk.END, "🌀 Complex Numbers\n", "section")
        self.help_text.insert(tk.END, "• Use 'i' as the imaginary unit (e.g., '2 + 3i').\n", "bullet")
        self.help_text.insert(tk.END, "• Real-valued results are formatted dynamically (e.g., 'sqrt(-9)' yields '3i').\n\n", "bullet")
        
        self.help_text.insert(tk.END, "📈 2D Canvas Grapher\n", "section")
        self.help_text.insert(tk.END, "• Switch to Grapher tab, enter expression (e.g., 'sin(x)'), and click 'Plot Function'.\n", "bullet")
        self.help_text.insert(tk.END, "• Adjust range using 'x min' and 'x max' entry fields.\n\n", "bullet")
        
        self.help_text.insert(tk.END, "🔄 Unit Converter\n", "section")
        self.help_text.insert(tk.END, "• Select Category (Length, Area, Volume, Speed, Data, Temperature, Mass) and desired units.\n", "bullet")
        self.help_text.insert(tk.END, "• Enter a value for instant, real-time conversion results.\n", "bullet")

    def run(self):
        self.root.mainloop()