# Premium Desktop Scientific Calculator (Python & Tkinter)

A Casio-inspired, professional scientific and engineering desktop calculator built with Python and Tkinter. Featuring a stabilized AST-based mathematical expression evaluator, real-time 2D/3D graphing, computer algebra system (CAS) symbolic differentiation, statistics hypothesis testing, interactive physics simulations, and support for complex numbers.

---

## 📷 Screenshots

<p align="center">
  <img src="assets/screenshot1.png" width="400" alt="Scientific Calculator Main Interface" />
  <img src="assets/screenshot2.png" width="400" alt="2D Canvas Function Grapher" />
  <br />
  <img src="assets/screenshot3.png" width="400" alt="3D Surface Wireframe Grapher" />
</p>

---

## 🌟 Key Features

### 1. Advanced Math & Complex Number Engine
- **AST-Based Evaluator**: Secure mathematical parser with safety caps for exponentiation (e.g. `9^9^9`) and recursion depth limits to prevent overflows and CPU locks.
- **Trigonometric Modes**: Instantly toggle between Degree (`DEG`) and Radian (`RAD`) modes.
- **Complex Number Support**: Full parsing and output formatting of imaginary numbers (`a + bi`). Supports fractional powers of negative bases (e.g., `sqrt(-9)` yields `3i`).
- **Phasor Vector Converter**: Interactively convert between Rectangular and Polar complex formats with visual phasor representations drawn on a concentric canvas grid.

### 2. Real-Time Graphical Plotters
- **2D Canvas Grapher**: Plot up to 3 functions concurrently. Supports Cartesian, Polar ($r=f(\theta)$), and Parametric ($x(t), y(t)$) graphing modes with coordinate viewport auto-scaling. Includes interactive pan-and-zoom controls and coordinates tracing tooltips.
- **Critical Points Scanner**: Scans curves using numerical bisection to identify and display Roots ($f(x)=0$), Extrema (min/max points via derivative sign-changes), and Intersections of multiple functions.
- **3D Surface Grapher**: Renders 3D wireframe surfaces ($z=f(x,y)$) with rotation transformation matrices, orthographic parallel projection, and interactive dragging.

### 3. Advanced Engineering Modules
- **Symbolic CAS Tool**: AST-based symbolic differentiation engine that differentiates math expressions and automatically simplifies them using algebraic reduction rules.
- **Calculus Suite**: Definite integration using Simpson's Rule and derivative calculations using central finite difference.
- **Matrix Algebra Suite**: Renders input grids for 2x2 and 3x3 matrices. Computes Determinant, Transpose, Inverse, REF, RREF, and Rank.
- **Equation Solvers**: Solves quadratic/cubic roots, Newton-Raphson single-variable root solving, and 2x2 or 3x3 linear systems using Cramer's Rule. Renders complete step-by-step algebraic explanations when checked.
- **Vector Mathematics**: Calculates vector dot products, cross products, projections, magnitudes, and angles for 2D and 3D vectors.
- **Formula Library**: Solves preset engineering equations (Ohm's Law, Kinetic Energy, Ideal Gas Law) and custom user formulas for any target variable.

### 4. Statistics, TVM & Interactive Simulations
- **Descriptive Statistics**: Calculates mean, median, standard deviation, linear regression fittings, and normal CDF.
- **Hypothesis Testing Tab**: Conducts 1-Sample Z-Test, 1-Sample T-Test, 2-Sample Welch T-Test, and Chi-Square Goodness-of-Fit tests with critical values and p-values approximations.
- **TVM & Amortization**: Solver for Time Value of Money ($N, I/Y, PV, PMT, FV$) with compound calculations and detailed loan amortization tables.
- **Interactive Simulations**: Renders projectile motion animations (speed, altitude, and range telemetry) and Fourier wave builders showing harmonic summation curves.

### 5. Settings, Exporters & Customizations
- **Sound Click Profiles**: Toggle keypad audio click profiles (Mechanical Click, Soft Pop, Retro Beep) with volume controls playing asynchronously.
- **Appearance Themes**: Toggle Midnight, Casio Classic, Cyberpunk, and Arctic Frost themes recursively. Supports layout toggling between "Standard Scientific" (7x7) and "Basic Focus" (4x5) keypad layouts.
- **Data Exporters**: Export calculation history log to CSV or TXT formats via Windows save file dialog.

---

## 🚀 How to Run the App

### Standalone Desktop Executable (No Python Required)
You can launch the calculator as a normal Windows desktop application directly, without opening any terminals or Python projects:
1. Navigate to the `dist` folder: `dist/ScientificCalculator.exe`.
2. Double-click **`ScientificCalculator.exe`** to run!
3. To search for it from your Start Menu, press the **Windows Key** and type **`Scientific Calculator`** (the installer automatically creates a Start Menu search indexing shortcut).

### Running from Python Project Source
1. Make sure you have Python 3.8+ installed.
2. Clone the repository and run:
   ```bash
   python main.py
   ```

---

## 🧪 Running Unit Tests

The project features a suite of **126 unit tests** covering the math evaluators, CAS engines, solvers, and UI bindings:
```bash
python -m unittest discover -s tests
```

---

## 🛠️ Technology Stack
- **Language**: Python 3.14 (compatible with Python 3.8+)
- **UI Toolkit**: Pure Python Tkinter (Zero external UI dependencies)
- **Audio Output**: Windows native Multimedia API (`winsound` PlaySound / MessageBeep)
- **Packaging**: PyInstaller
