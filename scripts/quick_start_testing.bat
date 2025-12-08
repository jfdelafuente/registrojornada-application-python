@echo off
REM Quick start script for testing environment setup
REM This script will set up everything needed to run tests

echo.
echo =============================================
echo   Quick Start - Testing Environment Setup
echo =============================================
echo.

REM Check Python version
echo [Step 1/5] Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+
    goto :error
)

REM Check/Create virtual environment
echo.
echo [Step 2/5] Setting up virtual environment...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        goto :error
    )
    echo Virtual environment created successfully
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo.
echo [Step 3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    goto :error
)
echo Virtual environment activated

REM Install dependencies
echo.
echo [Step 4/5] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements.txt
    goto :error
)

pip install -r requirements-dev.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements-dev.txt
    goto :error
)
echo Dependencies installed successfully

REM Validate environment
echo.
echo [Step 5/5] Validating environment...
python scripts\validate_test_environment.py
if errorlevel 1 (
    echo WARNING: Some validation checks failed
    echo See above for details
    goto :warn
)

echo.
echo =============================================
echo   Setup Complete!
echo =============================================
echo.
echo Your environment is ready for testing.
echo.
echo Quick commands:
echo   pytest --no-cov          # Fast tests
echo   pytest                   # Full tests with coverage
echo   scripts\run_tests.bat    # Automated test runner
echo.
echo See docs\GUIA_TESTING.md for complete guide
echo.
goto :end

:error
echo.
echo =============================================
echo   Setup Failed
echo =============================================
echo.
echo Please check the errors above and try again.
echo See docs\GUIA_TESTING.md for troubleshooting.
exit /b 1

:warn
echo.
echo =============================================
echo   Setup Completed with Warnings
echo =============================================
echo.
echo Some checks failed but you may still be able to run tests.
echo Try: pytest --no-cov
exit /b 0

:end
exit /b 0
