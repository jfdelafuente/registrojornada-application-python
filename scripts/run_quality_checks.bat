@echo off
REM Script to run code quality checks on Windows
REM Usage: scripts\run_quality_checks.bat [fast|full]

setlocal

set MODE=%1
if "%MODE%"=="" set MODE=full

echo.
echo ======================================
echo   Running Code Quality Checks
echo   Mode: %MODE%
echo ======================================
echo.

if "%MODE%"=="fast" goto :fast
if "%MODE%"=="full" goto :full

echo Unknown mode: %MODE%
echo Usage: scripts\run_quality_checks.bat [fast^|full]
exit /b 1

:fast
echo Running quick quality checks (auto-fix)...
echo.

echo [1/2] Formatting code with Black...
python -m black app\ tests\
if errorlevel 1 (
    echo ERROR: Black formatting failed
    exit /b 1
)

echo [2/2] Sorting imports with isort...
python -m isort app\ tests\
if errorlevel 1 (
    echo ERROR: isort failed
    exit /b 1
)

echo.
echo ======================================
echo   Quick checks completed!
echo ======================================
echo.
echo Code has been formatted and imports sorted.
echo Run 'scripts\run_quality_checks.bat full' for complete verification.
goto :end

:full
echo Running full quality checks...
echo.

echo [1/5] Checking code formatting with Black...
python -m black --check app\ tests\
if errorlevel 1 (
    echo FAILED: Code formatting issues found
    echo Run: black app\ tests\
    exit /b 1
)
echo PASSED: Code formatting is correct

echo.
echo [2/5] Checking import sorting with isort...
python -m isort --check-only app\ tests\
if errorlevel 1 (
    echo FAILED: Import sorting issues found
    echo Run: isort app\ tests\
    exit /b 1
)
echo PASSED: Imports are correctly sorted

echo.
echo [3/5] Running Flake8 linting...
python -m flake8 app\ tests\ --max-line-length=100
if errorlevel 1 (
    echo FAILED: Linting issues found
    exit /b 1
)
echo PASSED: No linting issues

echo.
echo [4/5] Running Mypy type checking...
python -m mypy app\ --ignore-missing-imports --no-strict-optional
if errorlevel 1 (
    echo WARNING: Type checking issues found
    echo This is not blocking, but should be reviewed
)
echo Type checking completed

echo.
echo [5/5] Running tests with coverage...
python -m pytest
if errorlevel 1 (
    echo FAILED: Tests failed
    exit /b 1
)
echo PASSED: All tests passed

echo.
echo ======================================
echo   All quality checks passed!
echo ======================================
echo.
echo Your code meets all quality standards.
echo Ready to commit!
goto :end

:end
exit /b 0
