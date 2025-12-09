#!/bin/bash
# Quick fix script for code quality - auto-formats code
# Usage: ./scripts/quick_fix_quality.sh

set -e

echo ""
echo "============================================="
echo "  Quick Fix - Code Quality Auto-Format"
echo "============================================="
echo ""

echo "[Step 1/2] Formatting code with Black..."
if ! python -m black app/ tests/; then
    echo "ERROR: Black formatting failed"
    exit 1
fi
echo "Black formatting completed successfully"

echo ""
echo "[Step 2/2] Sorting imports with isort..."
if ! python -m isort app/ tests/; then
    echo "ERROR: isort failed"
    exit 1
fi
echo "Import sorting completed successfully"

echo ""
echo "============================================="
echo "  Auto-Fix Complete!"
echo "============================================="
echo ""
echo "Your code has been automatically formatted."
echo ""
echo "Next steps:"
echo "  git diff               # Review changes"
echo "  git add .              # Stage changes"
echo "  git commit             # Commit with pre-commit hooks"
echo ""
