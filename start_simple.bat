@echo off
REM ============================================
REM SmartHire - Simple Startup (Skip Checks)
REM ============================================
title SmartHire - Simple Start

cd /d "%~dp0"

echo.
echo Starting SmartHire...
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
)

echo.
echo Starting Flask server...
echo Server: http://localhost:5000
echo Press Ctrl+C to stop
echo.

REM Run Flask app directly
venv\Scripts\python.exe app.py

pause

