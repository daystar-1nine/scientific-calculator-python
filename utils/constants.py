"""
Global constants and configuration for the calculator.
"""

import math


# ============================
# MATHEMATICAL CONSTANTS
# ============================
PI = math.pi
E = math.e

# Physics / scientific constants (optional global use)
SPEED_OF_LIGHT = 299792458            # m/s
PLANCK_CONSTANT = 6.62607015e-34      # J·s
GRAVITATIONAL_CONSTANT = 6.6743e-11   # m^3/kg/s^2


# ============================
# DEFAULT SETTINGS
# ============================
DEFAULT_MODE = "DEG"   # Keep consistent with CalculatorMode

MAX_HISTORY_SIZE = 100


# ============================
# NUMERIC LIMITS (Safety)
# ============================
MAX_FACTORIAL = 1000
MAX_EXP_INPUT = 700          # prevent overflow in exp()
MAX_POWER = 1e6              # safe exponent cap


# ============================
# UI / FORMAT SETTINGS
# ============================
MAX_DISPLAY_LENGTH = 30
SCI_NOTATION_THRESHOLD = 1e12
SMALL_NUMBER_THRESHOLD = 1e-10