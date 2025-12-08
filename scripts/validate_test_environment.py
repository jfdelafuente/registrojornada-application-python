#!/usr/bin/env python3
"""
Validate Test Environment

Validates that the testing environment is correctly configured with all
necessary dependencies and structure.

Usage:
    python scripts/validate_test_environment.py
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")


def print_check(passed: bool, message: str, details: str = ""):
    """Print check result with color."""
    if passed:
        status = f"{Colors.GREEN}[OK]{Colors.RESET}"
    else:
        status = f"{Colors.RED}[FAIL]{Colors.RESET}"

    print(f"{status} {message}")
    if details:
        print(f"      {Colors.YELLOW}{details}{Colors.RESET}")


def check_python_version() -> Tuple[bool, str]:
    """Check Python version is 3.10+."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major == 3 and version.minor >= 10:
        return True, f"Python version: {version_str}"
    else:
        return False, f"Python {version_str} - Need Python 3.10+"


def check_virtual_env() -> Tuple[bool, str]:
    """Check if running in virtual environment."""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

    if in_venv:
        return True, "Virtual environment: Active"
    else:
        return False, "Not in virtual environment - activate venv first"


def check_package_installed(package: str, version_check: bool = False) -> Tuple[bool, str]:
    """Check if a package is installed."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0:
            if version_check:
                for line in result.stdout.split('\n'):
                    if line.startswith('Version:'):
                        version = line.split(':', 1)[1].strip()
                        return True, f"{package}: {version}"
            return True, f"{package}: installed"
        else:
            return False, f"{package}: NOT installed"
    except Exception as e:
        return False, f"{package}: Error checking - {str(e)}"


def check_directory_exists(path: Path, name: str) -> Tuple[bool, str]:
    """Check if directory exists."""
    if path.exists() and path.is_dir():
        return True, f"{name}: exists"
    else:
        return False, f"{name}: NOT found at {path}"


def check_file_exists(path: Path, name: str) -> Tuple[bool, str]:
    """Check if file exists."""
    if path.exists() and path.is_file():
        return True, f"{name}: exists"
    else:
        return False, f"{name}: NOT found at {path}"


def count_test_files(test_dir: Path) -> Tuple[bool, str]:
    """Count test files in directory."""
    if not test_dir.exists():
        return False, "Test directory not found"

    test_files = list(test_dir.glob("**/*.py"))
    test_count = len([f for f in test_files if f.name.startswith("test_")])

    if test_count > 0:
        return True, f"{test_count} test files found"
    else:
        return False, "No test files found"


def check_import(module: str) -> Tuple[bool, str]:
    """Check if module can be imported."""
    try:
        __import__(module)
        return True, f"{module}: importable"
    except ImportError as e:
        return False, f"{module}: Import failed - {str(e)}"


def run_pytest_collect() -> Tuple[bool, str]:
    """Try to collect tests with pytest."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10
        )

        if result.returncode == 0:
            # Parse output to count tests
            lines = result.stdout.split('\n')
            for line in lines:
                if 'test' in line.lower():
                    return True, f"pytest can collect tests"
            return True, "pytest collection successful"
        else:
            return False, f"pytest collection failed: {result.stderr[:100]}"
    except subprocess.TimeoutExpired:
        return False, "pytest collection timed out"
    except Exception as e:
        return False, f"pytest collection error: {str(e)}"


def main():
    """Run all validation checks."""
    print_header("Test Environment Validation")

    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    checks: List[Tuple[bool, str, str]] = []

    # 1. Python version
    print(f"{Colors.BOLD}1. Python Environment{Colors.RESET}")
    passed, msg = check_python_version()
    print_check(passed, msg)
    checks.append((passed, "Python version", msg))

    passed, msg = check_virtual_env()
    print_check(passed, msg)
    checks.append((passed, "Virtual environment", msg))

    # 2. Core dependencies
    print(f"\n{Colors.BOLD}2. Core Dependencies{Colors.RESET}")
    core_deps = [
        "pydantic",
        "requests",
        "beautifulsoup4",
        "python-dotenv",
    ]

    for dep in core_deps:
        passed, msg = check_package_installed(dep)
        print_check(passed, msg)
        checks.append((passed, f"Dependency: {dep}", msg))

    # 3. Testing dependencies
    print(f"\n{Colors.BOLD}3. Testing Dependencies{Colors.RESET}")
    test_deps = [
        ("pytest", True),
        ("pytest-cov", True),
        ("pytest-mock", True),
        ("pytest-asyncio", True),
    ]

    for dep, version_check in test_deps:
        passed, msg = check_package_installed(dep, version_check)
        print_check(passed, msg)
        checks.append((passed, f"Test dependency: {dep}", msg))

    # 4. Code quality tools
    print(f"\n{Colors.BOLD}4. Code Quality Tools{Colors.RESET}")
    quality_tools = [
        ("black", True),
        ("flake8", False),
        ("isort", False),
        ("mypy", False),
    ]

    for tool, version_check in quality_tools:
        passed, msg = check_package_installed(tool, version_check)
        print_check(passed, msg)
        checks.append((passed, f"Quality tool: {tool}", msg))

    # 5. Project structure
    print(f"\n{Colors.BOLD}5. Project Structure{Colors.RESET}")

    dirs_to_check = [
        (project_root / "app", "app directory"),
        (project_root / "tests", "tests directory"),
        (project_root / "tests" / "unit", "tests/unit directory"),
        (project_root / "tests" / "integration", "tests/integration directory"),
        (project_root / "scripts", "scripts directory"),
    ]

    for path, name in dirs_to_check:
        passed, msg = check_directory_exists(path, name)
        print_check(passed, msg)
        checks.append((passed, name, msg))

    # 6. Configuration files
    print(f"\n{Colors.BOLD}6. Configuration Files{Colors.RESET}")

    files_to_check = [
        (project_root / "pytest.ini", "pytest.ini"),
        (project_root / "pyproject.toml", "pyproject.toml"),
        (project_root / "requirements.txt", "requirements.txt"),
        (project_root / "requirements-dev.txt", "requirements-dev.txt"),
    ]

    for path, name in files_to_check:
        passed, msg = check_file_exists(path, name)
        print_check(passed, msg)
        checks.append((passed, name, msg))

    # 7. Test files
    print(f"\n{Colors.BOLD}7. Test Files{Colors.RESET}")

    passed, msg = count_test_files(project_root / "tests")
    print_check(passed, msg)
    checks.append((passed, "Test files", msg))

    # 8. Module imports
    print(f"\n{Colors.BOLD}8. Module Imports{Colors.RESET}")

    modules_to_import = [
        "app",
        "app.config",
        "app.models.workday",
        "app.exceptions",
    ]

    for module in modules_to_import:
        passed, msg = check_import(module)
        print_check(passed, msg)
        checks.append((passed, f"Import: {module}", msg))

    # 9. Pytest collection
    print(f"\n{Colors.BOLD}9. Pytest Collection{Colors.RESET}")

    passed, msg = run_pytest_collect()
    print_check(passed, msg)
    checks.append((passed, "Pytest collection", msg))

    # Summary
    print_header("Summary")

    total_checks = len(checks)
    passed_checks = sum(1 for passed, _, _ in checks if passed)
    failed_checks = total_checks - passed_checks

    success_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0

    print(f"Total checks: {total_checks}")
    print(f"{Colors.GREEN}Passed: {passed_checks}{Colors.RESET}")
    if failed_checks > 0:
        print(f"{Colors.RED}Failed: {failed_checks}{Colors.RESET}")
    print(f"Success rate: {success_rate:.1f}%")

    if failed_checks > 0:
        print(f"\n{Colors.RED}{Colors.BOLD}Failed checks:{Colors.RESET}")
        for passed, name, msg in checks:
            if not passed:
                print(f"{Colors.RED}  - {name}: {msg}{Colors.RESET}")

        print(f"\n{Colors.YELLOW}Recommendations:{Colors.RESET}")
        print("1. Activate virtual environment: source venv/bin/activate (or venv\\Scripts\\activate on Windows)")
        print("2. Install dependencies: pip install -r requirements.txt requirements-dev.txt")
        print("3. Verify Python version: python --version (need 3.10+)")
        print(f"\nSee {Colors.BLUE}docs/GUIA_TESTING.md{Colors.RESET} for detailed instructions.")
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}Environment is ready for testing!{Colors.RESET}")
        print(f"\nNext steps:")
        print(f"  {Colors.GREEN}pytest --no-cov{Colors.RESET}          # Quick tests")
        print(f"  {Colors.GREEN}pytest{Colors.RESET}                   # Full tests with coverage")
        print(f"  {Colors.GREEN}pytest -v{Colors.RESET}                # Verbose output")
        print(f"\nSee {Colors.BLUE}docs/GUIA_TESTING.md{Colors.RESET} for more options.")

    # Exit code
    sys.exit(0 if failed_checks == 0 else 1)


if __name__ == "__main__":
    main()
