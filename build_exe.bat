@echo off
title Build Calculator GPT Standalone Executable
cd /d "%~dp0"
echo ========================================================
echo       Building Calculator GPT Standalone Executable
echo ========================================================
echo.
pyinstaller --noconfirm --onedir --windowed --add-data "index.html;." --add-data "icon.svg;." --add-data "manifest.json;." --add-data "engine;engine" --name "CalculatorGPT" app.py
echo.
echo [*] Build completed successfully!
echo [*] Executable location: dist\CalculatorGPT\CalculatorGPT.exe
pause
