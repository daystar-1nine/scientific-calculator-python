"""
Manages DEG and RAD calculator modes.
"""


class CalculatorMode:

    DEGREE = "DEG"
    RADIAN = "RAD"

    def __init__(self):
        self.mode = self.DEGREE

    def set_degree(self):
        self.mode = self.DEGREE

    def set_radian(self):
        self.mode = self.RADIAN

    def get_mode(self):
        return self.mode