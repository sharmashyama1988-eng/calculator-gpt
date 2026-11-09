@echo off
title Calculator GPT — Standalone Desktop App
cd /d "%~dp0"
echo ========================================================
echo       Calculator GPT - AI Math Studio (Standalone)
echo ========================================================
echo.
echo [*] Checking Python runtime...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.10+ from python.org and try again.
    pause
    exit /b 1
)

echo [*] Starting Python CAS & Physics Engine...
python app.py
if %errorlevel% neq 0 (
    echo.
    echo [*] If desktop window failed, starting local web mode...
    start http://127.0.0.1:8765/index.html
    python app.py --server
)
