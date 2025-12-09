@echo off
REM Quick fix script for code quality - auto-formats code
REM Usage: scripts\quick_fix_quality.bat

echo.
echo =============================================
echo   Quick Fix - Code Quality Auto-Format
echo =============================================
echo.

echo [Step 1/2] Formatting code with Black...
python -m black app\ tests\
if errorlevel 1 (
    echo ERROR: Black formatting failed
    goto :error
)
echo Black formatting completed successfully

echo.
echo [Step 2/2] Sorting imports with isort...
python -m isort app\ tests\
if errorlevel 1 (
    echo ERROR: isort failed
    goto :error
)
echo Import sorting completed successfully

echo.
echo =============================================
echo   Auto-Fix Complete!
echo =============================================
echo.
echo Your code has been automatically formatted.
echo.
echo Next steps:
echo   git diff               # Review changes
echo   git add .              # Stage changes
echo   git commit             # Commit with pre-commit hooks
echo.
goto :end

:error
echo.
echo =============================================
echo   Auto-Fix Failed
echo =============================================
echo.
echo Please check the errors above and try again.
exit /b 1

:end
exit /b 0
