# Scientific Calculator (Python)

A Casio-inspired, professional scientific calculator built in Python using Tkinter. Featuring an AST-based secure mathematical expression evaluator, 2D function graphing, a multi-category unit converter, and support for complex number math.

---

## 🌟 Key Features

- **Advanced Math Parser**: High-accuracy evaluator with implicit multiplication support and safety checks to prevent memory exhaustion and recursion issues.
- **Trigonometric Modes**: Seamlessly toggle between Degree (`DEG`) and Radian (`RAD`) modes.
- **Complex Number Engine**: Full support for imaginary numbers using the `i` unit, automatic parsing, and dynamic formatting (e.g. `sqrt(-9)` evaluates to `3i`).
- **2D Canvas Grapher**: Plot single-variable functions in real-time with automatic outlier/asymptote clipping.
- **Interactive Unit Converter**: Convert units across seven categories (Length, Area, Volume, Speed, Data, Temperature, and Mass) with real-time feedback.
- **Persistent Calculation History**: Access past calculations in the sidebar. Double-click to load them back to the input line. Saved persistently to `~/.calculator_history`.
- **Keyboard Shortcuts**: Control the calculator directly from your physical keyboard.

---

## 📖 User Guide & Reference Manual

For a complete guide on input syntax, supported functions list, complex numbers syntax, and instructions on how to use the grapher and unit converter, check out the [**User Guide & Reference Manual**](USER_GUIDE.md).

---

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.8 or higher installed on your system.

### Installation

Clone this repository and navigate to the project directory:

```bash
git clone https://github.com/daystar-1nine/scientific-calculator-python.git
cd scientific-calculator-python
```

### Running the Application

Launch the desktop GUI by executing the main script:

```bash
python main.py
```

---

## 🧪 Running Unit Tests

The codebase comes equipped with an extensive test suite verifying mathematical functions, AST parser stability, complex number conversions, history features, and GUI bindings.

To execute the unit tests, run:

```bash
python -m unittest discover -s tests
```
