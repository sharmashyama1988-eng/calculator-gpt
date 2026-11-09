@echo off
title Build Calculator GPT Standalone Executable
cd /d "%~dp0"
echo ========================================================
echo       Building Calculator GPT Standalone Executable
echo     Bytecode Optimized (-OO) with SmolLM2-135M Neural AI
echo ========================================================
echo.
python -OO -m PyInstaller --noconfirm --onedir --windowed --icon "icon.ico" --add-data "index.html;." --add-data "icon.svg;." --add-data "icon.ico;." --add-data "manifest.json;." --add-data "engine;engine" --add-data "models;models" --hidden-import "llama_cpp" --hidden-import "sympy" --hidden-import "mpmath" --name "CalculatorGPT" app.py
echo.
echo [*] Build completed successfully!
echo [*] Executable location: dist\CalculatorGPT\CalculatorGPT.exe
pause
