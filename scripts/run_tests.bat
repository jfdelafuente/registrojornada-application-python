@echo off
REM Script to run tests on Windows
REM Usage: scripts\run_tests.bat [fast|coverage|html|full]

setlocal

set MODE=%1
if "%MODE%"=="" set MODE=coverage

echo.
echo ======================================
echo  Running Tests - Mode: %MODE%
echo ======================================
echo.

if "%MODE%"=="fast" (
    echo Running fast tests without coverage...
    pytest --no-cov -x
    goto :end
)

if "%MODE%"=="coverage" (
    echo Running tests with coverage report...
    pytest
    goto :end
)

if "%MODE%"=="html" (
    echo Running tests with HTML coverage report...
    pytest --cov=app --cov-report=html --cov-report=term
    echo.
    echo HTML report generated in: htmlcov\index.html
    goto :end
)

if "%MODE%"=="full" (
    echo Running full quality checks...
    echo.
    echo [1/5] Code formatting check...
    black --check app\ tests\
    if errorlevel 1 (
        echo FAILED: Code formatting issues found
        echo Run: black app\ tests\
        goto :error
    )

    echo [2/5] Import sorting check...
    isort --check-only app\ tests\
    if errorlevel 1 (
        echo FAILED: Import sorting issues found
        echo Run: isort app\ tests\
        goto :error
    )

    echo [3/5] Linting...
    flake8 app\ tests\ --max-line-length=100
    if errorlevel 1 (
        echo FAILED: Linting issues found
        goto :error
    )

    echo [4/5] Type checking...
    mypy app\ --ignore-missing-imports --no-strict-optional
    if errorlevel 1 (
        echo WARNING: Type checking issues found
    )

    echo [5/5] Tests with coverage...
    pytest
    if errorlevel 1 (
        echo FAILED: Tests failed
        goto :error
    )

    echo.
    echo ======================================
    echo  All checks passed!
    echo ======================================
    goto :end
)

echo Unknown mode: %MODE%
echo Usage: scripts\run_tests.bat [fast^|coverage^|html^|full]
goto :error

:error
exit /b 1

:end
exit /b 0
