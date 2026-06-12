import unittest
import tkinter as tk
from gui.app import CalculatorApp


class TestFinanceModule(unittest.TestCase):

    def setUp(self):
        self.app = CalculatorApp()

    def tearDown(self):
        self.app.root.update()
        self.app.root.destroy()

    def set_val(self, entry, val):
        entry.delete(0, tk.END)
        entry.insert(0, str(val))

    def test_tvm_solve_future_value(self):
        # Solve FV, set PV = -1000, I/Y = 10%, N = 5, PMT = 0
        # FV = 1000 * (1.1)^5 = 1610.51
        self.set_val(self.app.finance_controller.entries["PV"], -1000)
        self.set_val(self.app.finance_controller.entries["I"], 10)
        self.set_val(self.app.finance_controller.entries["N"], 5)
        self.set_val(self.app.finance_controller.entries["PMT"], 0)

        self.app.finance_controller.solve_tvm("FV")
        
        fv_str = self.app.finance_controller.entries["FV"].get()
        fv_val = float(fv_str)
        self.assertAlmostEqual(fv_val, 1610.51, places=1)

    def test_tvm_solve_payment(self):
        # Solve PMT, set PV = -10000 (loan), I/Y = 12% annual (compounded matching periods), N = 12, FV = 0
        # PMT = 10000 * (0.12 * (1.12)^12) / ((1.12)^12 - 1) = 1614.36
        self.set_val(self.app.finance_controller.entries["PV"], -10000)
        self.set_val(self.app.finance_controller.entries["I"], 12)
        self.set_val(self.app.finance_controller.entries["N"], 12)
        self.set_val(self.app.finance_controller.entries["FV"], 0)

        self.app.finance_controller.solve_tvm("PMT")

        pmt_str = self.app.finance_controller.entries["PMT"].get()
        pmt_val = float(pmt_str)
        self.assertAlmostEqual(pmt_val, 1614.36, places=1)

    def test_generate_amortization_schedule(self):
        # PV = 10000, I/Y = 12%, N = 12 (months)
        self.set_val(self.app.finance_controller.entries["PV"], 10000)
        self.set_val(self.app.finance_controller.entries["I"], 12)
        self.set_val(self.app.finance_controller.entries["N"], 12)

        self.app.finance_controller.generate_amort()
        res = self.app.finance_controller.result_text.get("1.0", tk.END).strip()
        
        # Verify headers and sample lines are outputted
        self.assertIn("Monthly PMT", res)
        self.assertIn("Interest", res)
        self.assertIn("Principal", res)


if __name__ == "__main__":
    unittest.main()
