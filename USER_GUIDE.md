# Scientific Calculator - User Guide & Reference Manual

Welcome to the Scientific Calculator user guide. This guide explains how to use the scientific calculator's operations, modes, scientific functions, complex number capabilities, interactive 2D grapher, unit converter, and physical keyboard shortcuts.

---

## Table of Contents
1. [General Interface & Layout](#1-general-interface--layout)
2. [Input Syntax & Basic Rules](#2-input-syntax--basic-rules)
3. [Mathematical Constants & Variables](#3-mathematical-constants--variables)
4. [Supported Math Functions](#4-supported-math-functions)
5. [Trigonometric Modes (DEG vs. RAD)](#5-trigonometric-modes-deg-vs-rad)
6. [Complex Numbers & Imaginary Arithmetic](#6-complex-numbers--imaginary-arithmetic)
7. [Memory Operations](#7-memory-operations)
8. [Calculations History](#8-calculations-history)
9. [2D Canvas Grapher](#9-2d-canvas-grapher)
10. [Unit Converter](#10-unit-converter)
11. [Keyboard Shortcuts](#11-keyboard-shortcuts)
12. [Troubleshooting & Error Messages](#12-troubleshooting--error-messages)

---

## 1. General Interface & Layout

The calculator features a clean, responsive double-panel interface:
- **Left Panel (Calculator Console)**: Displays the standard numeric and scientific keypad, mathematical expression screen, result output line, and status indicators (`DEG`/`RAD` mode and `M` memory indicator).
- **Right Panel (Interactive Sidebar)**: A multi-tab drawer containing **History**, **Grapher**, **Converter**, and **Guide**. Click the **HIST** key on the left panel to expand or collapse this sidebar.

---

## 2. Input Syntax & Basic Rules

The expression evaluator parses expressions using standard algebraic notation.
- **Implicit Multiplication**: You can omit the multiplication sign `*` in standard mathematical contexts:
  - `2pi` is automatically evaluated as `2 * pi`
  - `3(4 + 5)` is automatically evaluated as `3 * (4 + 5)`
  - `2i` is automatically evaluated as `2 * i` (complex)
  - `x(x+1)` is evaluated as `x * (x+1)` in the grapher
- **Operator Precedence**: Standard PEMDAS rules apply:
  1. Parentheses `()`
  2. Exponentiation `^`
  3. Multiplication `*` and Division `/`
  4. Addition `+` and Subtraction `-`
- **Unary Operators**: The negative sign `-` and positive sign `+` can precede numbers or expressions directly (e.g., `-5`, `-(2+3)`).

---

## 3. Mathematical Constants & Variables

The evaluator recognizes two built-in mathematical constants:
- **$\pi$ (Pi)**: Enter `pi` or `PI`. Evaluates to approximately `3.141592653589793`.
- **$e$ (Euler's Number)**: Enter `e` or `E`. Evaluates to approximately `2.718281828459045`.

In the **Grapher** panel, the variable `x` represents the horizontal coordinate axis variable.

---

## 4. Supported Math Functions

All function arguments must be enclosed in parentheses. For example, use `sin(pi/2)`, not `sin pi/2`.

### Trigonometric Functions
- `sin(theta)`: Sine of `theta`.
- `cos(theta)`: Cosine of `theta`.
- `tan(theta)`: Tangent of `theta`.
- `asin(x)`: Arcsine (inverse sine) of `x`. Domain: `[-1, 1]`.
- `acos(x)`: Arccosine (inverse cosine) of `x`. Domain: `[-1, 1]`.
- `atan(x)`: Arctangent (inverse tangent) of `x`.

### Hyperbolic Functions
- `sinh(x)`: Hyperbolic sine of `x`.
- `cosh(x)`: Hyperbolic cosine of `x`.
- `tanh(x)`: Hyperbolic tangent of `x`.

### Exponential & Logarithmic Functions
- `exp(x)`: Natural exponential function, $e^x$.
- `log(x)`: Common (base-10) logarithm of `x`. Domain: $x > 0$.
- `ln(x)`: Natural (base-$e$) logarithm of `x`. Domain: $x > 0$.
- `sqrt(x)`: Square root of `x`. In real mode, requires $x \ge 0$. If $x < 0$, it automatically returns a complex result (e.g., `sqrt(-9)` yields `3i`).

### Combinatorics & Powers
- `factorial(n)`: Factorial of $n$. Supported for non-negative integers up to `1000` to prevent performance bottlenecks.
- `x^2`: Squares the current value.
- `x^3`: Cubes the current value.
- `1/x`: Divides 1 by the current value.

---

## 5. Trigonometric Modes (DEG vs. RAD)

You can toggle the trigonometric angular units between Degrees and Radians:
1. Click the **DEG** or **RAD** button on the keypad (or look at the blue indicator in the upper-right corner of the display screen).
2. Toggling this button switches the mode instantly.
- **Degree Mode (DEG)**: Trig functions accept arguments in degrees (e.g., `sin(90)` $\approx 1.0$). Inverse trig functions return results in degrees (e.g., `asin(1)` $\approx 90.0$).
- **Radian Mode (RAD)**: Trig functions accept arguments in radians (e.g., `sin(pi/2)` $\approx 1.0$). Inverse trig functions return results in radians (e.g., `asin(1)` $\approx 1.5707963268$).

> [!NOTE]
> The tangent function `tan(x)` will throw an undefined value error at asymptotes (e.g., `tan(90)` in Degree mode or `tan(pi/2)` in Radian mode).

---

## 6. Complex Numbers & Imaginary Arithmetic

The calculator fully supports complex and imaginary numbers in expressions:
- **Imaginary Unit `i`**: Use the symbol `i` (representing $\sqrt{-1}$) in expressions (e.g., `2 + 3i`).
- **Implicit Multiplication**: Digits immediately preceding `i` are parsed correctly (e.g., `3i` becomes `3 * i`).
- **Auto-Imaginary Upgrade**: If an operation results in an imaginary number, it is computed automatically instead of crashing (e.g., `(-4)^0.5` evaluates to `2i`, and `sqrt(-9)` evaluates to `3i`).
- **Formatting**: Output values are formatted dynamically as `a + bi` or `a - bi`. If the real part or imaginary part is approximately zero (below $10^{-15}$), it is truncated for a cleaner output (e.g., `0 + 3i` displays as `3i`, and `5 + 0i` displays as `5`).

### Examples of Complex Expressions:
- `(2 + 3i) * (1 - i)` $\rightarrow$ `5 + i`
- `(1 + i)^2` $\rightarrow$ `2i`
- `e^(i * pi)` $\rightarrow$ `-1` (Euler's Identity)

---

## 7. Memory Operations

The memory register acts as a temporary variable slot to store intermediate calculation results:
- **MC (Memory Clear)**: Resets the stored memory value to `0.0`.
- **MR (Memory Recall)**: Appends the currently stored memory value to the expression display.
- **M+ (Memory Add)**: Evaluates the active display expression and adds the result to the memory register.
- **M- (Memory Subtract)**: Evaluates the active display expression and subtracts the result from the memory register.

> [!TIP]
> A small **M** indicator appears in the top-left portion of the display screen whenever the memory value is non-zero.

---

## 8. Calculations History

Every successful evaluation is recorded in the Calculations History.
- **Open History**: Click **HIST** on the keypad to expand the sidebar. Select the **History** tab.
- **Recalling Entries**: Click any expression in the history listbox. The clicked expression is automatically loaded back into the calculator display input for editing or re-evaluation.
- **Clear History**: Click the red **Clear History** button at the bottom of the sidebar.
- **Persistent Storage**: Your history is saved to a file named `.calculator_history` in your system user profile directory (`os.path.expanduser("~")`), ensuring it remains intact between launches.

---

## 9. 2D Canvas Grapher

The custom coordinate grapher plots functions dynamically on a 2D grid:
1. Open the sidebar and click the **Grapher** tab.
2. Enter a mathematical expression in terms of `x` (e.g., `sin(x)`, `x^2 - 4`, `2^x`).
3. Set your horizontal bounds using the `x min` and `x max` fields (default is `-10` to `10`).
4. Click **Plot Function**.
- **Asymptote Protections**: Functions with asymptotes (like `1/x` or `tan(x)`) are automatically clipped using mathematical percentiles. This prevents vertical line spikes from squashing the rest of the plot.

---

## 10. Unit Converter

The unit converter provides real-time conversions across multiple standard engineering and everyday categories:
1. Open the sidebar and click the **Converter** tab.
2. Choose a category from the dropdown menu:
   - **Length**: meters, kilometers, centimeters, millimeters, miles, yards, feet, inches
   - **Area**: square meters, square kilometers, square miles, acres, hectares
   - **Volume**: liters, milliliters, cubic meters, gallons, quarts, cups
   - **Speed**: m/s, km/h, mph, knots
   - **Data**: Bytes, Kilobytes (KB), Megabytes (MB), Gigabytes (GB), Terabytes (TB)
   - **Temperature**: Celsius, Fahrenheit, Kelvin
   - **Mass**: kilograms, grams, milligrams, pounds, ounces
3. Select the source unit ("From") and the target unit ("To").
4. Type a value in the input field. The target value updates automatically in real-time as you type.

---

## 11. Keyboard Shortcuts

You can operate the calculator directly using your physical keyboard. The key mappings are as follows:

| Physical Key | Calculator Operation |
| :--- | :--- |
| `0` - `9` | Digits `0` - `9` |
| `.` | Decimal Point |
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `^` | Exponentiation |
| `(` and `)` | Parentheses |
| `!` | Factorial |
| **Enter** / **Return** | Evaluate (`=`) |
| **Backspace** | Delete Last Character (`DEL`) |
| **Escape** | Clear Display (`C`) |

---

## 12. Troubleshooting & Error Messages

If the calculator encounters an exceptional condition, it will display a descriptive error message:
- **`Error: Division by zero`**: Attempted to divide by `0` (e.g., `5/0`, `1/0`) or raise `0` to a negative power.
- **`Error: Invalid expression`**: The expression contains syntax errors, unmatched parentheses, or unsupported operators/symbols.
- **`Error: Math operation error`**: An input value was outside the valid mathematical domain for a function (e.g., `asin(2.5)`, `log(-1)`).
- **`Error: Power calculation overflow`**: The exponentiation result is too large to fit in standard double-precision floating-point format (e.g., base and exponent would exceed limits, such as `9^9^9` or `0.1^-25000`).
- **`Error: Expression too deeply nested`**: An expression containing an excessive number of nested parentheses exceeded safety limits. Simplify the formula structure.
