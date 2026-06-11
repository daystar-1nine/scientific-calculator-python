"""
Handles calculator-related errors.
"""


class CalculatorError(Exception):
    """Base calculator exception."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when an expression is invalid."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero occurs."""
    pass


class MathOperationError(CalculatorError):
    """Raised for invalid mathematical operations."""
    pass


def handle_error(error):
    """
    Converts exceptions into user-friendly messages.
    """

    if isinstance(error, DivisionByZeroError):
        return "Error: Division by zero"

    if isinstance(error, InvalidExpressionError):
        return "Error: Invalid expression"

    if isinstance(error, MathOperationError):
        return "Error: Invalid mathematical operation"

    return f"Error: {str(error)}"