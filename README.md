# Calculator GPT — Autonomous AI Math Studio & Standalone CAS Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![SymPy Powered](https://img.shields.io/badge/SymPy-CAS-green.svg)](https://www.sympy.org/)
[![UI](https://img.shields.io/badge/Interface-Modern%20Dark%20Neumorphic-purple.svg)]()

> **Calculator GPT** is a high-performance, offline-first mathematical intelligence studio combining symbolic Computer Algebra Systems (CAS), natural language & Hinglish query resolution, and competitive exam aptitude solvers into a native standalone desktop app and web experience.

---

## 🌟 Key Highlights

- **100% Offline & Private**: Zero external cloud dependencies, zero API keys, and zero telemetry. All computations run natively on your local machine using Python's SymPy and custom deterministic solvers.
- **Natural Language & Hinglish Math Parser**: Understands conversational mathematics in English, Hindi, and Hinglish (e.g., *"Ek train 60 km/h se aur dusri 80 km/h se opposite direction mein. 280 km kitne time mein?"* or *"Khareeda 1200 mein aur becha 1500 mein. Profit kitna?"*).
- **Symbolic CAS Engine**: High-order symbolic derivatives, definite and indefinite integration, algebraic expansions, polynomial factorization, limits, and equation solving.
- **Universal Quantitative Aptitude Engine**:
  - **Motion & Trains**: Relative velocity, opposite/same direction motion, crossing platforms/poles/tunnels.
  - **Work & Time / Chain Rule**: Multiple workers, varying efficiencies, $M_1 D_1 H_1 = M_2 D_2 H_2$.
  - **Commercial Mathematics**: Cost price, selling price, profit/loss percentage, discount, simple & compound interest.
  - **Age Problems**: Multi-person simultaneous algebraic age relationships.
- **Advanced Statistics & Probability**: Mean, median, mode, sample/population variance, standard deviation, quartiles, and IQR with detailed calculation steps.
- **Linear Algebra**: Matrix multiplication, determinants, inverses, rank, eigenvalues, and eigenvectors.
- **Native Desktop App & Web Mode**: Seamlessly launches as a native desktop window via `pywebview` or as a local web service at `http://127.0.0.1:8765`.
- **Standalone Windows Executable**: One-click build script to generate a single portable Windows `.exe` via PyInstaller.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sharmashyama1988-eng/calculator-gpt.git
   cd calculator-gpt
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   - On Windows:
     Double-click `run_app.bat` or run:
     ```bash
     python app.py
     ```
   - In browser/server mode:
     ```bash
     python app.py --server
     ```
     Then open `http://127.0.0.1:8765/index.html` in your browser.

---

## 📦 Building Standalone Windows Executable (.exe)

To bundle Calculator GPT into a standalone native Windows executable that runs without requiring Python to be installed on the client machine:

```bash
build_exe.bat
```
The output executable will be generated at:
```
dist\CalculatorGPT\CalculatorGPT.exe
```

---

## 🧪 Testing & Verification

Run the test suite to verify symbolic CAS calculations and natural language aptitude solvers:

```bash
# Run core CAS and quantitative engine tests
python test_engine.py

# Run dynamic unseen problem tests
python test_unseen.py
```

---

## 📂 Project Architecture

```
calculator-gpt/
├── app.py                   # Desktop application entrypoint & pywebview wrapper
├── build_exe.bat            # Automated PyInstaller packaging script
├── run_app.bat              # One-click Windows runner
├── index.html               # Frontend UI (Responsive Dark Neumorphic Math Studio)
├── icon.svg                 # Vector app icon
├── manifest.json            # PWA manifest
├── sw.js                    # Service Worker for offline asset caching
├── requirements.txt         # Python package dependencies
├── test_engine.py           # Core validation suite
├── test_unseen.py           # Unseen & dynamic word problem verification
└── engine/                  # Core Computational Mathematics Engine
    ├── __init__.py          # Package initialization
    ├── master_solver.py     # Master orchestrator & query dispatcher
    ├── cas_engine.py        # Symbolic Computer Algebra System (SymPy)
    ├── aptitude_engine.py   # Quantitative aptitude, trains, ages, commercial math
    ├── universal_solver.py  # Universal motion, work, and chain rule solver
    ├── stats_engine.py      # Statistical and descriptive analytics
    └── nlp_parser.py        # Natural language and Hinglish expression tokenizer
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
