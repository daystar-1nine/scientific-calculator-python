"""
Contains scientific calculator functions.
"""

import math


from utils.error_handler import MathOperationError


class ScientificFunctions:

    @staticmethod
    def sin(value, mode="RAD"):
        if mode == "DEG":
            value = math.radians(value)
        return math.sin(value)

    @staticmethod
    def cos(value, mode="RAD"):
        if mode == "DEG":
            value = math.radians(value)
        return math.cos(value)

    @staticmethod
    def tan(value, mode="RAD"):
        if mode == "DEG":
            # Check for 90, 270, etc. where tangent is undefined
            if (value - 90) % 180 == 0:
                raise MathOperationError("Tangent undefined for this angle")
            value = math.radians(value)
        else:
            # Check for pi/2, 3pi/2, etc. (with float tolerance)
            # cos(x) close to 0
            if abs(math.cos(value)) < 1e-15:
                raise MathOperationError("Tangent undefined for this angle")
        return math.tan(value)

    @staticmethod
    def log(value):
        if value <= 0:
            raise MathOperationError("Logarithm of non-positive number")
        return math.log10(value)

    @staticmethod
    def ln(value):
        if value <= 0:
            raise MathOperationError("Natural logarithm of non-positive number")
        return math.log(value)

    @staticmethod
    def sqrt(value):
        if value < 0:
            raise MathOperationError("Square root of negative number")
        return math.sqrt(value)

    @staticmethod
    def factorial(value):
        # Allow integer-valued floats like 5.0
        try:
            val_float = float(value)
            if val_float < 0 or not val_float.is_integer():
                raise MathOperationError("Factorial of negative or non-integer number")
            return math.factorial(int(val_float))
        except (ValueError, TypeError):
            raise MathOperationError("Factorial of invalid value")