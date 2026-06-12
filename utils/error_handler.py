"""
Handles calculator-related errors.
"""

# ============================
# BASE EXCEPTION
# ============================
class CalculatorError(Exception):
    """Base calculator exception."""

    def __init__(self, message="", code=None):
        super().__init__(message)
        self.code = code


# ============================
# SPECIFIC ERRORS
# ============================
class InvalidExpressionError(CalculatorError):
    """Raised when an expression is invalid."""
    def __init__(self, message="Invalid expression"):
        super().__init__(message, code="INVALID_EXPR")


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero occurs."""
    def __init__(self, message="Division by zero"):
        super().__init__(message, code="DIV_ZERO")


class MathOperationError(CalculatorError):
    """Raised for invalid mathematical operations."""
    def __init__(self, message="Invalid mathematical operation"):
        super().__init__(message, code="MATH_ERROR")


# ============================
# ERROR HANDLER
# ============================
def handle_error(error, debug=False):
    """
    Converts exceptions into user-friendly messages.

    Args:
        error: Exception instance
        debug: If True, returns detailed debug info
    """

    # Debug mode (for developers)
    if debug:
        return f"[{type(error).__name__}] {str(error)}"

    # User-friendly messages
    if isinstance(error, CalculatorError):
        message = str(error) if str(error) else "Unexpected calculator error"
        return f"Error: {message}"

    # Fallback for unknown exceptions
    return "Error: Something went wrong"