#!/bin/bash
# Script to run code quality checks on Linux/Mac
# Usage: ./scripts/run_quality_checks.sh [fast|full]

set -e

MODE=${1:-full}

echo ""
echo "======================================"
echo "  Running Code Quality Checks"
echo "  Mode: $MODE"
echo "======================================"
echo ""

case "$MODE" in
    fast)
        echo "Running quick quality checks (auto-fix)..."
        echo ""

        echo "[1/2] Formatting code with Black..."
        if ! python -m black app/ tests/; then
            echo "ERROR: Black formatting failed"
            exit 1
        fi

        echo "[2/2] Sorting imports with isort..."
        if ! python -m isort app/ tests/; then
            echo "ERROR: isort failed"
            exit 1
        fi

        echo ""
        echo "======================================"
        echo "  Quick checks completed!"
        echo "======================================"
        echo ""
        echo "Code has been formatted and imports sorted."
        echo "Run './scripts/run_quality_checks.sh full' for complete verification."
        ;;

    full)
        echo "Running full quality checks..."
        echo ""

        echo "[1/5] Checking code formatting with Black..."
        if ! python -m black --check app/ tests/; then
            echo "FAILED: Code formatting issues found"
            echo "Run: black app/ tests/"
            exit 1
        fi
        echo "PASSED: Code formatting is correct"

        echo ""
        echo "[2/5] Checking import sorting with isort..."
        if ! python -m isort --check-only app/ tests/; then
            echo "FAILED: Import sorting issues found"
            echo "Run: isort app/ tests/"
            exit 1
        fi
        echo "PASSED: Imports are correctly sorted"

        echo ""
        echo "[3/5] Running Flake8 linting..."
        if ! python -m flake8 app/ tests/ --max-line-length=100; then
            echo "FAILED: Linting issues found"
            exit 1
        fi
        echo "PASSED: No linting issues"

        echo ""
        echo "[4/5] Running Mypy type checking..."
        if ! python -m mypy app/ --ignore-missing-imports --no-strict-optional; then
            echo "WARNING: Type checking issues found"
            echo "This is not blocking, but should be reviewed"
        fi
        echo "Type checking completed"

        echo ""
        echo "[5/5] Running tests with coverage..."
        if ! python -m pytest; then
            echo "FAILED: Tests failed"
            exit 1
        fi
        echo "PASSED: All tests passed"

        echo ""
        echo "======================================"
        echo "  All quality checks passed!"
        echo "======================================"
        echo ""
        echo "Your code meets all quality standards."
        echo "Ready to commit!"
        ;;

    *)
        echo "Unknown mode: $MODE"
        echo "Usage: ./scripts/run_quality_checks.sh [fast|full]"
        exit 1
        ;;
esac

echo ""
echo "Quality checks completed successfully!"
