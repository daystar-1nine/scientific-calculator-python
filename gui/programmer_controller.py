"""
Controller for the Programmer Mode (Base-N) tab.
"""

import tkinter as tk
from utils.error_handler import handle_error, MathOperationError

class ProgrammerController:
    def __init__(self, app, tab_frame):
        self.app = app
        self.tab_frame = tab_frame

        self.bit_width = tk.StringVar(value="32-bit")
        self.active_val = 0  # Internal integer representation
        
        self.setup_ui()

    def setup_ui(self):
        # 1. Bit-width selector
        width_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        width_frame.pack(fill="x", padx=10, pady=5)

        width_label = tk.Label(
            width_frame, text="Bit Width:", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 10, "bold")
        )
        width_label.pack(side="left", padx=(0, 10))

        width_menu = tk.OptionMenu(
            width_frame,
            self.bit_width,
            "64-bit", "32-bit", "16-bit", "8-bit",
            command=self.on_bit_width_change
        )
        width_menu.config(
            bg="#48484A", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=0, relief="flat", highlightthickness=0
        )
        width_menu["menu"].config(bg="#2C2C2E", fg="#FFFFFF", font=("Segoe UI", 9, "bold"))
        width_menu.pack(side="left")

        # 2. Base Entries Frame
        entries_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        entries_frame.pack(fill="x", padx=10, pady=5)

        bases = [
            ("HEX", 16, "hex_entry"),
            ("DEC", 10, "dec_entry"),
            ("OCT", 8, "oct_entry"),
            ("BIN", 2, "bin_entry")
        ]

        self.entries = {}
        for label, base, attr in bases:
            f = tk.Frame(entries_frame, bg="#2C2C2E")
            f.pack(fill="x", pady=2)
            
            lbl = tk.Label(
                f, text=label, fg="#8E8E93", bg="#2C2C2E",
                font=("Consolas", 9, "bold"), width=5, anchor="w"
            )
            lbl.pack(side="left")

            entry = tk.Entry(
                f, bg="#1C1C1E", fg="#FFFFFF", font=("Consolas", 10, "bold"),
                bd=3, relief="flat", insertbackground="#FFFFFF"
            )
            entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
            
            # Bind key release to sync other entries
            entry.bind("<KeyRelease>", lambda event, b=base, a=attr: self.on_entry_edit(b, a))
            self.entries[attr] = entry

        # 3. Operand B Entry Frame
        op_b_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        op_b_frame.pack(fill="x", padx=10, pady=5)

        op_b_label = tk.Label(
            op_b_frame, text="Operand B (DEC/HEX):", fg="#FFFFFF", bg="#2C2C2E",
            font=("Segoe UI", 9, "bold")
        )
        op_b_label.pack(side="left", padx=(0, 5))

        self.op_b_entry = tk.Entry(
            op_b_frame, bg="#1C1C1E", fg="#FFFFFF", font=("Consolas", 10, "bold"),
            bd=3, relief="flat", width=10, insertbackground="#FFFFFF"
        )
        self.op_b_entry.pack(side="left")
        self.op_b_entry.insert(0, "1")

        # 4. Bitwise Operators Frame
        ops_frame = tk.Frame(self.tab_frame, bg="#2C2C2E")
        ops_frame.pack(fill="x", padx=10, pady=5)

        # Row 1 ops
        r1 = tk.Frame(ops_frame, bg="#2C2C2E")
        r1.pack(fill="x", pady=2)
        tk.Button(r1, text="AND", bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", command=lambda: self.run_bitwise("and")).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(r1, text="OR", bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", command=lambda: self.run_bitwise("or")).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(r1, text="XOR", bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", command=lambda: self.run_bitwise("xor")).pack(side="left", fill="x", expand=True, padx=2)

        # Row 2 ops
        r2 = tk.Frame(ops_frame, bg="#2C2C2E")
        r2.pack(fill="x", pady=2)
        tk.Button(r2, text="LSH (<<)", bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", command=lambda: self.run_bitwise("lsh")).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(r2, text="RSH (>>)", bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", command=lambda: self.run_bitwise("rsh")).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(r2, text="NOT A", bg="#FF9500", fg="#FFFFFF", font=("Segoe UI", 9, "bold"), bd=0, relief="flat", command=lambda: self.run_bitwise("not")).pack(side="left", fill="x", expand=True, padx=2)

        self.update_displays()

    def get_mask(self):
        w = self.bit_width.get()
        if w == "64-bit": return 0xFFFFFFFFFFFFFFFF
        if w == "16-bit": return 0xFFFF
        if w == "8-bit": return 0xFF
        return 0xFFFFFFFF  # Default 32-bit

    def on_bit_width_change(self, *args):
        # Apply mask to active value
        self.active_val &= self.get_mask()
        self.update_displays()

    def update_displays(self, skip_attr=None):
        mask = self.get_mask()
        val = self.active_val & mask

        mapping = [
            ("hex_entry", f"{val:X}"),
            ("dec_entry", f"{val}"),
            ("oct_entry", f"{val:o}"),
            ("bin_entry", f"{val:b}")
        ]

        for attr, s in mapping:
            if attr == skip_attr:
                continue
            entry = self.entries[attr]
            entry.delete(0, tk.END)
            entry.insert(0, s)

    def on_entry_edit(self, base, attr):
        entry = self.entries[attr]
        val_str = entry.get().strip()
        if not val_str:
            self.active_val = 0
            self.update_displays(skip_attr=attr)
            return

        try:
            # Parse based on base
            self.active_val = int(val_str, base) & self.get_mask()
            self.update_displays(skip_attr=attr)
        except ValueError:
            # Revert to standard values or do nothing
            pass

    def run_bitwise(self, op):
        mask = self.get_mask()
        A = self.active_val & mask

        try:
            # Try to parse Operand B
            b_str = self.op_b_entry.get().strip()
            if not b_str:
                B = 0
            elif b_str.lower().startswith("0x"):
                B = int(b_str, 16)
            else:
                try:
                    B = int(b_str)
                except ValueError:
                    B = int(b_str, 16)
            B &= mask
        except Exception:
            B = 1

        if op == "not":
            self.active_val = (~A) & mask
        elif op == "and":
            self.active_val = (A & B) & mask
        elif op == "or":
            self.active_val = (A | B) & mask
        elif op == "xor":
            self.active_val = (A ^ B) & mask
        elif op == "lsh":
            self.active_val = (A << B) & mask
        elif op == "rsh":
            self.active_val = (A >> B) & mask

        self.update_displays()
