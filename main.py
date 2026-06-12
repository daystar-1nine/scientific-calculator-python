"""
Application entry point.
"""

from gui.app import CalculatorApp
from utils.error_handler import handle_error


def main():
    try:
        app = CalculatorApp()
        app.run()
    except Exception as e:
        # Final safety net (prevents silent crash)
        print(handle_error(e, debug=True))


if __name__ == "__main__":
    main()