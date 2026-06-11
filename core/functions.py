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
            if val_float > 1000:
                raise MathOperationError("Factorial input too large (max 1000)")
            return math.factorial(int(val_float))
        except (ValueError, TypeError):
            raise MathOperationError("Factorial of invalid value")

    @staticmethod
    def asin(value, mode="RAD"):
        if value < -1 or value > 1:
            raise MathOperationError("asin domain error: expects value in [-1, 1]")
        result = math.asin(value)
        if mode == "DEG":
            result = math.degrees(result)
        return result

    @staticmethod
    def acos(value, mode="RAD"):
        if value < -1 or value > 1:
            raise MathOperationError("acos domain error: expects value in [-1, 1]")
        result = math.acos(value)
        if mode == "DEG":
            result = math.degrees(result)
        return result

    @staticmethod
    def atan(value, mode="RAD"):
        result = math.atan(value)
        if mode == "DEG":
            result = math.degrees(result)
        return result

    @staticmethod
    def sinh(value):
        try:
            return math.sinh(value)
        except OverflowError:
            raise MathOperationError("sinh calculation overflow")

    @staticmethod
    def cosh(value):
        try:
            return math.cosh(value)
        except OverflowError:
            raise MathOperationError("cosh calculation overflow")

    @staticmethod
    def tanh(value):
        return math.tanh(value)

    @staticmethod
    def exp(value):
        try:
            return math.exp(value)
        except OverflowError:
            raise MathOperationError("exp calculation overflow")