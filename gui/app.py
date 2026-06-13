"""
Main calculator window.
"""

import math
import tkinter as tk

from gui.display import Display
from gui.buttons import ButtonPanel
from gui.converter_controller import ConverterController
from gui.graph_controller import GraphController
from gui.graph3d_controller import Graph3DController
from gui.complex_converter_controller import ComplexConverterController
from gui.matrix_controller import MatrixController
from gui.solver_controller import SolverController
from gui.stats_controller import StatsController
from gui.programmer_controller import ProgrammerController
from gui.variables_controller import VariablesController
from gui.vector_controller import VectorController
from gui.formula_controller import FormulaController
from gui.finance_controller import FinanceController
from gui.settings_controller import SettingsController
from gui.cas_controller import CASController
from gui.hypothesis_testing_controller import HypothesisTestingController
from gui.simulations_controller import SimulationsController
from core.evaluator import Evaluator
from core.modes import CalculatorMode
from features.memory import Memory
from features.history import History
from utils.error_handler import handle_error


class CalculatorApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Scientific Calculator")
        self.root.geometry("760x550")
        self.root.resizable(False, False)

        # State Managers
        self.evaluator = Evaluator()
        self.evaluator.app = self
        self.mode_manager = CalculatorMode()
        self.memory = Memory()
        self.history = History()
        self.custom_functions = {}

        # Keypad Audio Settings
        self.audio_profile = tk.StringVar(value="Off")
        self.audio_volume = tk.IntVar(value=50)

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

        # Right side: Sidebar frame (packed by default on startup to make all premium features visible)
        self.sidebar_frame = tk.Frame(self.main_frame, bg="#2C2C2E", width=280)
        self.sidebar_frame.pack(side="right", fill="both", expand=True)
        self.sidebar_visible = True

        # Tab switch headers (using a premium OptionMenu to support multiple new tools)
        self.sidebar_tabs_frame = tk.Frame(self.sidebar_frame, bg="#2C2C2E")
        self.sidebar_tabs_frame.pack(fill="x", padx=5, pady=5)

        self.active_tab = "History"
        self.tab_selector_var = tk.StringVar(value="History")
        self.tab_selector = tk.OptionMenu(
            self.sidebar_tabs_frame,
            self.tab_selector_var,
            "History", "Grapher", "3D Grapher", "Converter", "Complex Tool", "Matrix", "Solver", "Stats", "Base-N", "Vars/Consts", "Vectors", "Formulas", "Finance", "CAS Tool", "Hypothesis", "Simulations", "Settings", "Guide",
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
        self.tab_graph3d = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_conv = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_complex = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_matrix = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_solver = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_stats = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_programmer = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_variables = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_vector = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_formula = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_finance = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_cas = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_hypothesis = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_simulations = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
        self.tab_settings = tk.Frame(self.sidebar_content_frame, bg="#2C2C2E")
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

        # --- 2.5 3D Grapher Tab (Managed by Controller) ---
        self.graph3d_controller = Graph3DController(self, self.tab_graph3d)

        # --- 3. Converter Tab (Managed by Controller) ---
        self.converter_controller = ConverterController(self, self.tab_conv)

        # --- 3.5 Complex Tool Tab (Managed by Controller) ---
        self.complex_converter_controller = ComplexConverterController(self, self.tab_complex)

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

        # --- 9. Vector Tab (Managed by Controller) ---
        self.vector_controller = VectorController(self, self.tab_vector)

        # --- 10. Formula Tab (Managed by Controller) ---
        self.formula_controller = FormulaController(self, self.tab_formula)

        # --- 11. Finance Tab (Managed by Controller) ---
        self.finance_controller = FinanceController(self, self.tab_finance)

        # --- 11b. CAS Tab ---
        self.cas_controller = CASController(self, self.tab_cas)

        # --- 11c. Hypothesis Testing Tab ---
        self.hypothesis_testing_controller = HypothesisTestingController(self, self.tab_hypothesis)

        # --- 11d. Simulations Tab ---
        self.simulations_controller = SimulationsController(self, self.tab_simulations)

        # --- 12. Settings Tab (Managed by Controller) ---
        self.settings_controller = SettingsController(self, self.tab_settings)

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

        # Show default active tab (History) on startup
        self.switch_sidebar_tab(self.active_tab)

    def on_button_click(self, char):
        self.play_click_sound()
        current_text = self.display.get_text()

        # Handle clear
        if char in ["C", "CLEAR"]:
            self.display.clear()

        # Handle backspace
        elif char in ["DEL", "DELETE"]:
            self.display.set_text(current_text[:-1])

        # Handle Mode Toggle
        elif char in ["DEG", "MODE"]:
            mode = self.mode_manager.get_mode()
            if mode == CalculatorMode.DEGREE:
                self.mode_manager.set_radian()
            else:
                self.mode_manager.set_degree()
            self.update_mode_button_text()

        # Handle Memory operations
        elif char in ["MC", "MEM_CLEAR"]:
            self.memory.clear()
            self.update_memory_indicator()
        elif char in ["MR", "MEM_RECALL"]:
            val = self.memory.recall()
            self.display.append(self.format_result(val))
        elif char in ["M+", "MEM_ADD"]:
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
        elif char in ["M-", "MEM_SUB"]:
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
        elif char in ["HIST", "TOGGLE_HISTORY"]:
            self.toggle_history()
 
        # Handle Theme Cycle
        elif char in ["THEME"]:
            self.cycle_theme()
 
        # Handle Equal evaluation
        elif char in ["=", "EQUAL"]:
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

    def cycle_theme(self):
        if hasattr(self, "settings_controller"):
            themes = list(self.settings_controller.themes.keys())
            current = self.settings_controller.current_theme.get()
            try:
                next_idx = (themes.index(current) + 1) % len(themes)
            except ValueError:
                next_idx = 0
            next_theme = themes[next_idx]
            self.settings_controller.current_theme.set(next_theme)
            self.settings_controller.change_theme(next_theme)

    def switch_sidebar_tab(self, tab_name):
        self.active_tab = tab_name
        self.tab_selector_var.set(tab_name)

        # Pause simulations when switching away
        if tab_name != "Simulations" and hasattr(self, "simulations_controller"):
            self.simulations_controller.pause()

        # Unpack all frames
        self.tab_history.pack_forget()
        self.tab_graph.pack_forget()
        self.tab_graph3d.pack_forget()
        self.tab_conv.pack_forget()
        self.tab_complex.pack_forget()
        self.tab_matrix.pack_forget()
        self.tab_solver.pack_forget()
        self.tab_stats.pack_forget()
        self.tab_programmer.pack_forget()
        self.tab_variables.pack_forget()
        self.tab_vector.pack_forget()
        self.tab_formula.pack_forget()
        self.tab_finance.pack_forget()
        self.tab_cas.pack_forget()
        self.tab_hypothesis.pack_forget()
        self.tab_simulations.pack_forget()
        self.tab_settings.pack_forget()
        self.tab_guide.pack_forget()

        # Switch and perform actions
        if tab_name == "History":
            self.tab_history.pack(fill="both", expand=True)
            self.update_history_display()
        elif tab_name == "Grapher":
            self.tab_graph.pack(fill="both", expand=True)
            # Defer plot so the canvas is fully rendered before drawing
            self.root.after(20, self.graph_controller.plot_function)
        elif tab_name == "3D Grapher":
            self.tab_graph3d.pack(fill="both", expand=True)
            self.root.after(20, self.graph3d_controller.plot_3d)
        elif tab_name == "Converter":
            self.tab_conv.pack(fill="both", expand=True)
            self.converter_controller.run_conversion()
        elif tab_name == "Complex Tool":
            self.tab_complex.pack(fill="both", expand=True)
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
        elif tab_name == "Vectors":
            self.tab_vector.pack(fill="both", expand=True)
        elif tab_name == "Formulas":
            self.tab_formula.pack(fill="both", expand=True)
        elif tab_name == "Finance":
            self.tab_finance.pack(fill="both", expand=True)
        elif tab_name == "CAS Tool":
            self.tab_cas.pack(fill="both", expand=True)
        elif tab_name == "Hypothesis":
            self.tab_hypothesis.pack(fill="both", expand=True)
        elif tab_name == "Simulations":
            self.tab_simulations.pack(fill="both", expand=True)
            self.root.after(20, self.simulations_controller.redraw)
        elif tab_name == "Settings":
            self.tab_settings.pack(fill="both", expand=True)
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

    def play_click_sound(self):
        profile = self.audio_profile.get()
        volume = self.audio_volume.get()
        if profile == "Off" or volume == 0:
            return
            
        try:
            import winsound
            import os
            media_dir = "C:\\Windows\\Media"
            
            if profile == "Mechanical Click":
                path = os.path.join(media_dir, "Windows Navigation Start.wav")
                if os.path.exists(path):
                    winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                else:
                    winsound.PlaySound("SystemDefault", winsound.SND_ALIAS | winsound.SND_ASYNC)
                    
            elif profile == "Soft Pop":
                path = os.path.join(media_dir, "Windows Pop-up Blocked.wav")
                if os.path.exists(path):
                    winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                else:
                    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
                    
            elif profile == "Retro Beep":
                path = os.path.join(media_dir, "ding.wav")
                if os.path.exists(path):
                    winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                else:
                    winsound.PlaySound("SystemDefault", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception:
            pass

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
        self.help_text.insert(tk.END, "• Enter a value for instant, real-time conversion results.\n\n", "bullet")

        self.help_text.insert(tk.END, "🧮 Matrix Algebra\n", "section")
        self.help_text.insert(tk.END, "• Choose 2x2 or 3x3 dimension, input cell expressions, and compute Determinants, Inverses, and Transpositions.\n", "bullet")
        self.help_text.insert(tk.END, "• Perform binary matrix operations (Addition, Subtraction, Multiplication) between Matrix A and B.\n\n", "bullet")

        self.help_text.insert(tk.END, "⚡ Equation Solvers\n", "section")
        self.help_text.insert(tk.END, "• Root Finder: input f(x)=0 expression to solve for x using Newton's method.\n", "bullet")
        self.help_text.insert(tk.END, "• Linear Systems: solve 2x2 or 3x3 linear equation systems using Cramer's Rule.\n", "bullet")
        self.help_text.insert(tk.END, "• Polynomial Roots: compute all real & complex roots for quadratic and cubic equations.\n\n", "bullet")

        self.help_text.insert(tk.END, "📊 Statistics & Probability\n", "section")
        self.help_text.insert(tk.END, "• Statistics: calculate Mean, Median, Variance, Std Dev on comma-separated datasets.\n", "bullet")
        self.help_text.insert(tk.END, "• Regression: fits (x, y) coordinates to find slope, intercept, and correlation coefficient r.\n", "bullet")
        self.help_text.insert(tk.END, "• Probability: compute combinations (nCr), permutations (nPr), and Normal CDF values.\n\n", "bullet")

        self.help_text.insert(tk.END, "💻 Programmer Mode (Base-N)\n", "section")
        self.help_text.insert(tk.END, "• Enter values in Hexadecimal, Decimal, Octal, or Binary to instantly sync across all bases.\n", "bullet")
        self.help_text.insert(tk.END, "• Apply bit-width boundaries (8, 16, 32, 64-bit) and perform logical bitwise operations (AND, OR, XOR, NOT, LSH, RSH).\n\n", "bullet")

        self.help_text.insert(tk.END, "🏷️ Variables & constants\n", "section")
        self.help_text.insert(tk.END, "• Store numeric values into variable registers (A, B, C, D, X, Y).\n", "bullet")
        self.help_text.insert(tk.END, "• Quick-insert fundamental constants (speed of light c, Planck constant h, Boltzmann constant k, etc.) directly into calculations.\n\n", "bullet")

        self.help_text.insert(tk.END, "📐 Vector Mathematics\n", "section")
        self.help_text.insert(tk.END, "• Input 2D or 3D vector coordinates for vector A and vector B.\n", "bullet")
        self.help_text.insert(tk.END, "• Compute magnitudes, dot product, cross product, angles, addition/subtraction, and projections.\n\n", "bullet")

        self.help_text.insert(tk.END, "📝 Formula Library & Solver\n", "section")
        self.help_text.insert(tk.END, "• Choose a preloaded relation (Ohm's Law, Gas Law, Kinetic Energy, etc.) or input a custom formula.\n", "bullet")
        self.help_text.insert(tk.END, "• Select the target variable; enter values for other variables to solve numerically.\n\n", "bullet")

        self.help_text.insert(tk.END, "💰 Financial TVM & Amortization\n", "section")
        self.help_text.insert(tk.END, "• TVM: Input Periods (N), Interest (I/Y), PV, PMT, FV and solve for any missing variable.\n", "bullet")
        self.help_text.insert(tk.END, "• Amortization: Input loan amount (PV), rate (I/Y), and term (N) to generate full monthly payment breakdown.\n\n", "bullet")

        self.help_text.insert(tk.END, "⚙️ Settings & Exporters\n", "section")
        self.help_text.insert(tk.END, "• Switch calculator UI color themes: Midnight, Casio Classic, Cyberpunk, and Arctic Frost.\n", "bullet")
        self.help_text.insert(tk.END, "• Save calculation history logs to local .txt or .csv files.\n", "bullet")

    def change_keypad_layout(self, layout_name):
        self.buttons.set_layout(layout_name)

    def run(self):
        self.root.mainloop()