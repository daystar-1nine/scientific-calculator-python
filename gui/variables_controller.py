"""
Controller for the Variables Registry & Scientific Constants tab.
"""

import tkinter as tk
from utils.error_handler import handle_error

class VariablesController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.user_entries = {}
        self.constants_list = [
            ("Speed of Light (c)", "c", "299792458 m/s"),
            ("Planck Constant (h)", "h", "6.62607e-34 J·s"),
            ("Gravitational (G)", "G", "6.6743e-11 m³/kg/s²"),
            ("Gas Constant (R)", "R", "8.3145 J/mol·K"),
            ("Avogadro (NA)", "NA", "6.02214e23 /mol"),
            ("Boltzmann (k)", "k", "1.38065e-23 J/K"),
            ("Electron Charge (qe)", "qe", "1.60218e-19 C"),
            ("Electron Mass (me)", "me", "9.10938e-31 kg"),
            ("Proton Mass (mp)", "mp", "1.67262e-27 kg")
        ]

        self.setup_ui()

    def setup_ui(self):
        # 1. User Variables Section
        var_label = tk.Label(
            self.tab_frame, text="User Variables (A, B, C, D, X, Y):",
            fg="#8E8E93", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), anchor="w"
        )
        var_label.pack(fill="x", padx=10, pady=(5, 2))

        grid_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        grid_frame.pack(fill="x", padx=10, pady=2)

        vars_list = ["A", "B", "C", "D", "X", "Y"]
        for idx, var in enumerate(vars_list):
            row = idx // 3
            col = idx % 3

            cell_frame = tk.Frame(grid_frame, bg="#2C2C2E")
            cell_frame.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

            tk.Label(
                cell_frame, text=f"{var}:", fg="#FFFFFF", bg="#2C2C2E",
                font=("Segoe UI", 9, "bold")
            ).pack(side="left")

            entry = tk.Entry(
                cell_frame, bg="#1C1C1E", fg="#FFFFFF", width=5,
                font=("Segoe UI", 9, "bold"), bd=2, relief="flat",
                justify="center", insertbackground="#FFFFFF"
            )
            entry.pack(side="left", fill="x", expand=True, padx=(2, 0))
            entry.insert(0, "0")
            self.user_entries[var] = entry

        # Configure columns equally
        for i in range(3):
            grid_frame.grid_columnconfigure(i, weight=1)

        # 2. Custom Functions Section
        funcs_header = tk.Label(
            self.tab_frame, text="Custom Functions (e.g. f(x, y) = x^2 + y^2):",
            fg="#8E8E93", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), anchor="w"
        )
        funcs_header.pack(fill="x", padx=10, pady=(10, 2))

        func_input_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        func_input_frame.pack(fill="x", padx=10, pady=2)

        tk.Label(func_input_frame, text="Define:", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 8, "bold")).pack(side="left")
        
        self.func_name_entry = tk.Entry(
            func_input_frame, bg="#1C1C1E", fg="#FFFFFF", width=8,
            font=("Segoe UI", 9, "bold"), bd=2, relief="flat",
            justify="center", insertbackground="#FFFFFF"
        )
        self.func_name_entry.pack(side="left", padx=2)
        self.func_name_entry.insert(0, "f(x, y)")

        tk.Label(func_input_frame, text="=", fg="#FFFFFF", bg="#2C2C2E", font=("Segoe UI", 9, "bold")).pack(side="left", padx=2)

        self.func_body_entry = tk.Entry(
            func_input_frame, bg="#1C1C1E", fg="#FFFFFF", width=12,
            font=("Segoe UI", 9, "bold"), bd=2, relief="flat",
            insertbackground="#FFFFFF"
        )
        self.func_body_entry.pack(side="left", fill="x", expand=True, padx=2)
        self.func_body_entry.insert(0, "x^2 + y^2")

        save_func_btn = tk.Button(
            func_input_frame, text="Save", bg="#30D158", fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"), bd=0, relief="flat", padx=6, pady=2,
            command=self.save_custom_function
        )
        save_func_btn.pack(side="right", padx=(5, 0))

        # Listbox for functions
        self.funcs_listbox = tk.Listbox(
            self.tab_frame, bg="#1C1C1E", fg="#FFFFFF",
            selectbackground="#FF9500", selectforeground="#FFFFFF",
            font=("Segoe UI", 8, "bold"), height=2, bd=0, highlightthickness=0
        )
        self.funcs_listbox.pack(fill="x", padx=10, pady=2)

        delete_func_btn = tk.Button(
            self.tab_frame, text="Delete Selected Function", bg="#FF3B30", fg="#FFFFFF",
            font=("Segoe UI", 8, "bold"), bd=0, relief="flat", height=1,
            command=self.delete_custom_function
        )
        delete_func_btn.pack(fill="x", padx=10, pady=(2, 5))

        # 3. Scientific Constants Section Header
        consts_header = tk.Label(
            self.tab_frame, text="Physical Constants:",
            fg="#8E8E93", bg="#2C2C2E", font=("Segoe UI", 9, "bold"), anchor="w"
        )
        consts_header.pack(fill="x", padx=10, pady=(5, 2))

        # 4. Scrollable Constants list
        list_container = tk.Frame(self.tab_frame, bg="#2C2C2E")
        list_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side="right", fill="y")

        canvas = tk.Canvas(
            list_container, bg="#1C1C1E", bd=0, highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg="#1C1C1E")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Force inner frame width to match canvas width on resize
        canvas.bind('<Configure>', lambda event: canvas.itemconfig(canvas_window, width=event.width))
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Fill Scrollable List
        for name, symbol, desc in self.constants_list:
            item_frame = tk.Frame(scrollable_frame, bg="#1C1C1E", bd=0)
            item_frame.pack(fill="x", padx=5, pady=4)

            # Left side text: Name and symbol
            info_frame = tk.Frame(item_frame, bg="#1C1C1E")
            info_frame.pack(side="left", fill="x", expand=True)

            tk.Label(
                info_frame, text=f"{name} ({symbol})", fg="#FFFFFF", bg="#1C1C1E",
                font=("Segoe UI", 8, "bold"), anchor="w"
            ).pack(fill="x")

            tk.Label(
                info_frame, text=desc, fg="#30D158", bg="#1C1C1E",
                font=("Consolas", 7, "bold"), anchor="w"
            ).pack(fill="x")

            # Right side button: Insert
            btn = tk.Button(
                item_frame, text="Insert", bg="#48484A", fg="#FFFFFF",
                font=("Segoe UI", 8, "bold"), bd=0, relief="flat", padx=6, pady=2,
                command=lambda s=symbol: self.insert_constant(s)
            )
            btn.pack(side="right", padx=(5, 0))

    def insert_constant(self, symbol):
        # Appends constant to main display
        self.app.display.append(symbol)

    def get_variables_dict(self):
        # Define base constant values
        d = {
            'c': 299792458,
            'h': 6.62607015e-34,
            'G': 6.6743e-11,
            'R': 8.314462618,
            'NA': 6.02214076e23,
            'k': 1.380649e-23,
            'qe': 1.602176634e-19,
            'me': 9.1093837e-31,
            'mp': 1.67262192e-27
        }

        # Add capitalized versions
        for k, v in list(d.items()):
            d[k.upper()] = v

        # Evaluate and load user variable registers
        mode = self.app.mode_manager.get_mode()
        for var_name, entry in self.user_entries.items():
            val_str = entry.get().strip()
            val = 0.0
            if val_str:
                try:
                    # Allow variables to compose constants or other variables
                    val = self.app.evaluator.evaluate(val_str, mode, variables=d)
                except Exception:
                    pass
            d[var_name] = val
            d[var_name.upper()] = val
            if var_name != "C":
                d[var_name.lower()] = val
        return d

    def save_custom_function(self):
        sig = self.func_name_entry.get().strip()
        body = self.func_body_entry.get().strip()
        if not sig or not body:
            return
        
        try:
            if "(" not in sig or ")" not in sig:
                raise ValueError("Signature must contain arguments, e.g. f(x)")
            name_part, args_part = sig.split("(", 1)
            name = name_part.strip()
            args_str = args_part.split(")", 1)[0]
            args = [a.strip() for a in args_str.split(",") if a.strip()]
            
            if not name:
                raise ValueError("Function name cannot be empty")
            
            if not hasattr(self.app, "custom_functions"):
                self.app.custom_functions = {}
            self.app.custom_functions[name] = {
                "args": args,
                "body": body
            }
            self.update_funcs_listbox()
        except Exception as e:
            # Display warning/error in some way
            pass

    def delete_custom_function(self):
        sel = self.funcs_listbox.curselection()
        if not sel:
            return
        item_str = self.funcs_listbox.get(sel[0])
        name = item_str.split("(", 1)[0].strip()
        if hasattr(self.app, "custom_functions") and name in self.app.custom_functions:
            del self.app.custom_functions[name]
            self.update_funcs_listbox()

    def update_funcs_listbox(self):
        self.funcs_listbox.delete(0, tk.END)
        if hasattr(self.app, "custom_functions"):
            for name, data in self.app.custom_functions.items():
                args_str = ", ".join(data["args"])
                self.funcs_listbox.insert(tk.END, f"{name}({args_str}) = {data['body']}")
