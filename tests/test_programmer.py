import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestProgrammerMode(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def test_programmer_sync_from_hex(self):
        # Input HEX = "FF" => active_val = 255
        self.app.programmer_controller.entries["hex_entry"].delete(0, tk.END)
        self.app.programmer_controller.entries["hex_entry"].insert(0, "FF")
        self.app.programmer_controller.on_entry_edit(16, "hex_entry")

        dec_str = self.app.programmer_controller.entries["dec_entry"].get()
        oct_str = self.app.programmer_controller.entries["oct_entry"].get()
        bin_str = self.app.programmer_controller.entries["bin_entry"].get()

        self.assertEqual(dec_str, "255")
        self.assertEqual(oct_str, "377")
        self.assertEqual(bin_str, "11111111")

    def test_programmer_bitwise_and(self):
        # A = 255 (0xFF), B = 15 (0x0F) => A AND B = 15
        self.app.programmer_controller.entries["dec_entry"].delete(0, tk.END)
        self.app.programmer_controller.entries["dec_entry"].insert(0, "255")
        self.app.programmer_controller.on_entry_edit(10, "dec_entry")

        self.app.programmer_controller.op_b_entry.delete(0, tk.END)
        self.app.programmer_controller.op_b_entry.insert(0, "15")

        self.app.programmer_controller.run_bitwise("and")
        dec_str = self.app.programmer_controller.entries["dec_entry"].get()
        self.assertEqual(dec_str, "15")

    def test_programmer_bitwise_not_byte(self):
        # Set to 8-bit (Byte) width
        self.app.programmer_controller.bit_width.set("8-bit")
        self.app.programmer_controller.on_bit_width_change()

        # A = 0x55 (85) => NOT A = 0xAA (170)
        self.app.programmer_controller.entries["dec_entry"].delete(0, tk.END)
        self.app.programmer_controller.entries["dec_entry"].insert(0, "85")
        self.app.programmer_controller.on_entry_edit(10, "dec_entry")

        self.app.programmer_controller.run_bitwise("not")
        dec_str = self.app.programmer_controller.entries["dec_entry"].get()
        self.assertEqual(dec_str, "170")


if __name__ == "__main__":
    unittest.main()
