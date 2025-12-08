#!/bin/bash
# Script to run tests on Linux/Mac
# Usage: ./scripts/run_tests.sh [fast|coverage|html|full]

set -e

MODE=${1:-coverage}

echo ""
echo "======================================"
echo "  Running Tests - Mode: $MODE"
echo "======================================"
echo ""

case "$MODE" in
    fast)
        echo "Running fast tests without coverage..."
        pytest --no-cov -x
        ;;

    coverage)
        echo "Running tests with coverage report..."
        pytest
        ;;

    html)
        echo "Running tests with HTML coverage report..."
        pytest --cov=app --cov-report=html --cov-report=term
        echo ""
        echo "HTML report generated in: htmlcov/index.html"
        ;;

    full)
        echo "Running full quality checks..."
        echo ""

        echo "[1/5] Code formatting check..."
        if ! black --check app/ tests/; then
            echo "FAILED: Code formatting issues found"
            echo "Run: black app/ tests/"
            exit 1
        fi

        echo "[2/5] Import sorting check..."
        if ! isort --check-only app/ tests/; then
            echo "FAILED: Import sorting issues found"
            echo "Run: isort app/ tests/"
            exit 1
        fi

        echo "[3/5] Linting..."
        if ! flake8 app/ tests/ --max-line-length=100; then
            echo "FAILED: Linting issues found"
            exit 1
        fi

        echo "[4/5] Type checking..."
        if ! mypy app/ --ignore-missing-imports --no-strict-optional; then
            echo "WARNING: Type checking issues found"
        fi

        echo "[5/5] Tests with coverage..."
        if ! pytest; then
            echo "FAILED: Tests failed"
            exit 1
        fi

        echo ""
        echo "======================================"
        echo "  All checks passed!"
        echo "======================================"
        ;;

    *)
        echo "Unknown mode: $MODE"
        echo "Usage: ./scripts/run_tests.sh [fast|coverage|html|full]"
        exit 1
        ;;
esac

echo ""
echo "Tests completed successfully!"
