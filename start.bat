@echo off
setlocal enabledelayedexpansion
REM ============================================
REM SmartHire - Unified Startup Script
REM ============================================
title SmartHire - Starting Application

echo.
echo ============================================
echo   SmartHire Application Startup
echo ============================================
echo.

REM Change to the script's directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ and add it to your PATH.
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [2/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created!
) else (
    echo [2/5] Virtual environment found!
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment activation script not found!
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated!
echo.

REM Install/upgrade dependencies
echo [4/5] Checking dependencies...
set PYTHON_EXE=venv\Scripts\python.exe
set PIP_EXE=venv\Scripts\pip.exe

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python executable not found in venv!
    pause
    exit /b 1
)

"%PYTHON_EXE%" -m pip install --upgrade pip >nul 2>&1
"%PIP_EXE%" install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some dependencies may have failed to install.
    echo Continuing anyway...
)
echo.

REM Check if spacy model is installed (non-blocking - never exit)
echo [5/5] Checking NLP model...
set SPACY_CHECK=0
"%PYTHON_EXE%" -c "import spacy; spacy.load('en_core_web_sm')" >nul 2>&1
set SPACY_ERROR=!errorlevel!
if !SPACY_ERROR! neq 0 (
    set SPACY_CHECK=1
)

if !SPACY_CHECK!==1 (
    echo [INFO] Installing SpaCy English model (this may take a moment)...
    "%PYTHON_EXE%" -m spacy download en_core_web_sm
    set SPACY_DL_ERROR=!errorlevel!
    if !SPACY_DL_ERROR! neq 0 (
        echo [WARNING] NLP model installation failed, but continuing...
        echo [WARNING] Resume screening features may not work properly.
    ) else (
        echo [OK] NLP model installed successfully!
    )
) else (
    echo [OK] NLP model found!
)
echo.

REM Initialize database if needed (non-blocking - never exit)
echo [Database] Checking database...
"%PYTHON_EXE%" -c "from app import app, db; app.app_context().push(); db.create_all()" >nul 2>&1
set DB_ERROR=!errorlevel!
if !DB_ERROR! neq 0 (
    echo [WARNING] Database initialization check failed, but continuing...
) else (
    echo [OK] Database ready!
)
echo.

REM Force continue - ensure we don't exit here
goto :continue_setup

:continue_setup

echo ============================================
echo   Starting SmartHire Application
echo ============================================
echo.
echo Server will be available at:
echo   - http://localhost:5000
echo   - http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

REM Run the Flask application using the venv Python
REM Note: This will run until you press Ctrl+C
echo Starting Flask server...
"%PYTHON_EXE%" app.py

REM If we reach here, the app has stopped
echo.
echo ============================================
echo   Application has stopped
echo ============================================
pause
endlocal
