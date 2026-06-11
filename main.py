"""
Application entry point.
"""

from gui.app import CalculatorApp


def main():
    app = CalculatorApp()
    app.run()


if __name__ == "__main__":
    main()