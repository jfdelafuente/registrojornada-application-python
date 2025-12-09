#!/usr/bin/env python3
"""
Validate Code Quality Tools Environment

Validates that the code quality environment is correctly configured with all
necessary tools and configuration files.

Usage:
    python scripts/validate_quality_tools.py
"""

import sys
import os
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


def check_tool_installed(tool: str, version_flag: str = "--version") -> Tuple[bool, str]:
    """Check if a tool is installed and get version."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", tool, version_flag],
            capture_output=True,
            text=True,
            check=False,
            timeout=5
        )

        if result.returncode == 0:
            # Extract version from output
            version_line = result.stdout.split('\n')[0]
            return True, f"{tool}: {version_line}"
        else:
            return False, f"{tool}: NOT installed"
    except subprocess.TimeoutExpired:
        return False, f"{tool}: Check timed out"
    except Exception as e:
        return False, f"{tool}: Error - {str(e)}"


def check_command_available(command: str) -> Tuple[bool, str]:
    """Check if a command is available in PATH."""
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5
        )

        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            return True, f"{command}: {version_line}"
        else:
            return False, f"{command}: NOT available"
    except FileNotFoundError:
        return False, f"{command}: NOT found in PATH"
    except subprocess.TimeoutExpired:
        return False, f"{command}: Check timed out"
    except Exception as e:
        return False, f"{command}: Error - {str(e)}"


def check_file_exists(path: Path, name: str) -> Tuple[bool, str]:
    """Check if file exists."""
    if path.exists() and path.is_file():
        return True, f"{name}: exists"
    else:
        return False, f"{name}: NOT found at {path}"


def check_directory_exists(path: Path, name: str) -> Tuple[bool, str]:
    """Check if directory exists."""
    if path.exists() and path.is_dir():
        return True, f"{name}: exists"
    else:
        return False, f"{name}: NOT found at {path}"


def count_python_files(base_dir: Path) -> Tuple[bool, str]:
    """Count Python files in directory."""
    if not base_dir.exists():
        return False, "Directory not found"

    py_files = list(base_dir.glob("**/*.py"))
    count = len(py_files)

    if count > 0:
        return True, f"{count} Python files found"
    else:
        return False, "No Python files found"


def test_black_execution(project_root: Path) -> Tuple[bool, str]:
    """Test if Black can execute."""
    try:
        # Test on a small file
        test_file = project_root / "app" / "__init__.py"
        if not test_file.exists():
            return False, "Test file not found"

        result = subprocess.run(
            [sys.executable, "-m", "black", "--check", str(test_file)],
            capture_output=True,
            text=True,
            check=False,
            timeout=10
        )

        # Black returns 0 if formatted, 1 if needs formatting, >1 for errors
        if result.returncode in [0, 1]:
            return True, "Black can format code"
        else:
            return False, f"Black execution failed: {result.stderr[:50]}"
    except subprocess.TimeoutExpired:
        return False, "Black execution timed out"
    except Exception as e:
        return False, f"Black test error: {str(e)}"


def test_isort_execution(project_root: Path) -> Tuple[bool, str]:
    """Test if isort can execute."""
    try:
        test_file = project_root / "app" / "__init__.py"
        if not test_file.exists():
            return False, "Test file not found"

        result = subprocess.run(
            [sys.executable, "-m", "isort", "--check-only", str(test_file)],
            capture_output=True,
            text=True,
            check=False,
            timeout=10
        )

        # isort returns 0 if sorted, 1 if needs sorting
        if result.returncode in [0, 1]:
            return True, "isort can sort imports"
        else:
            return False, f"isort execution failed: {result.stderr[:50]}"
    except subprocess.TimeoutExpired:
        return False, "isort execution timed out"
    except Exception as e:
        return False, f"isort test error: {str(e)}"


def test_flake8_execution(project_root: Path) -> Tuple[bool, str]:
    """Test if Flake8 can execute."""
    try:
        test_file = project_root / "app" / "__init__.py"
        if not test_file.exists():
            return False, "Test file not found"

        result = subprocess.run(
            [sys.executable, "-m", "flake8", str(test_file)],
            capture_output=True,
            text=True,
            check=False,
            timeout=10
        )

        # Flake8 returns 0 if no issues, >0 if issues found (both are valid executions)
        if result.returncode >= 0:
            return True, "Flake8 can lint code"
        else:
            return False, f"Flake8 execution failed: {result.stderr[:50]}"
    except subprocess.TimeoutExpired:
        return False, "Flake8 execution timed out"
    except Exception as e:
        return False, f"Flake8 test error: {str(e)}"


def test_mypy_execution(project_root: Path) -> Tuple[bool, str]:
    """Test if Mypy can execute."""
    try:
        test_file = project_root / "app" / "__init__.py"
        if not test_file.exists():
            return False, "Test file not found"

        result = subprocess.run(
            [sys.executable, "-m", "mypy", str(test_file), "--ignore-missing-imports"],
            capture_output=True,
            text=True,
            check=False,
            timeout=15
        )

        # Mypy returns 0 if no issues, 1 if issues found (both are valid executions)
        if result.returncode in [0, 1]:
            return True, "Mypy can type check"
        else:
            return False, f"Mypy execution failed: {result.stderr[:50]}"
    except subprocess.TimeoutExpired:
        return False, "Mypy execution timed out"
    except Exception as e:
        return False, f"Mypy test error: {str(e)}"


def check_config_file_valid(file_path: Path, name: str) -> Tuple[bool, str]:
    """Check if configuration file is valid and non-empty."""
    if not file_path.exists():
        return False, f"{name}: File not found"

    try:
        content = file_path.read_text(encoding='utf-8')
        if len(content.strip()) > 0:
            return True, f"{name}: Valid (size: {len(content)} bytes)"
        else:
            return False, f"{name}: File is empty"
    except Exception as e:
        return False, f"{name}: Error reading - {str(e)}"


def main():
    """Run all validation checks."""
    print_header("Code Quality Tools Validation")

    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Add project root to sys.path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Change to project root directory
    original_dir = Path.cwd()
    os.chdir(project_root)

    checks: List[Tuple[bool, str, str]] = []

    # 1. Python Environment
    print(f"{Colors.BOLD}1. Python Environment{Colors.RESET}")
    passed, msg = check_python_version()
    print_check(passed, msg)
    checks.append((passed, "Python version", msg))

    passed, msg = check_virtual_env()
    print_check(passed, msg)
    checks.append((passed, "Virtual environment", msg))

    # 2. Code Quality Tools
    print(f"\n{Colors.BOLD}2. Code Quality Tools{Colors.RESET}")

    tools = [
        ("black", "--version"),
        ("isort", "--version"),
        ("flake8", "--version"),
        ("mypy", "--version"),
    ]

    for tool, version_flag in tools:
        passed, msg = check_tool_installed(tool, version_flag)
        print_check(passed, msg)
        checks.append((passed, f"Tool: {tool}", msg))

    # Check pre-commit separately
    passed, msg = check_command_available("pre-commit")
    print_check(passed, msg)
    checks.append((passed, "Tool: pre-commit", msg))

    # 3. Configuration Files
    print(f"\n{Colors.BOLD}3. Configuration Files{Colors.RESET}")

    config_files = [
        (project_root / "pyproject.toml", "pyproject.toml"),
        (project_root / ".flake8", ".flake8"),
        (project_root / ".pre-commit-config.yaml", ".pre-commit-config.yaml"),
    ]

    for path, name in config_files:
        passed, msg = check_config_file_valid(path, name)
        print_check(passed, msg)
        checks.append((passed, f"Config: {name}", msg))

    # 4. Project Structure
    print(f"\n{Colors.BOLD}4. Project Structure{Colors.RESET}")

    dirs_to_check = [
        (project_root / "app", "app directory"),
        (project_root / "tests", "tests directory"),
        (project_root / "scripts", "scripts directory"),
    ]

    for path, name in dirs_to_check:
        passed, msg = check_directory_exists(path, name)
        print_check(passed, msg)
        checks.append((passed, name, msg))

    # Count Python files
    passed, msg = count_python_files(project_root / "app")
    print_check(passed, msg)
    checks.append((passed, "Python files", msg))

    # 5. Tool Execution Tests
    print(f"\n{Colors.BOLD}5. Tool Execution Tests{Colors.RESET}")

    passed, msg = test_black_execution(project_root)
    print_check(passed, msg)
    checks.append((passed, "Black execution", msg))

    passed, msg = test_isort_execution(project_root)
    print_check(passed, msg)
    checks.append((passed, "isort execution", msg))

    passed, msg = test_flake8_execution(project_root)
    print_check(passed, msg)
    checks.append((passed, "Flake8 execution", msg))

    passed, msg = test_mypy_execution(project_root)
    print_check(passed, msg)
    checks.append((passed, "Mypy execution", msg))

    # Restore original directory
    os.chdir(original_dir)

    # Summary
    print_header("Summary")

    print(f"Project root: {project_root}")
    print(f"Working directory: {original_dir}")
    print()

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
        print("2. Install dev dependencies: pip install -r requirements-dev.txt")
        print("3. Verify Python version: python --version (need 3.10+)")
        print("4. Install pre-commit hooks: pre-commit install")
        print(f"\nSee {Colors.BLUE}docs/GUIA_CALIDAD_CODIGO.md{Colors.RESET} for detailed instructions.")
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}Environment is ready for code quality checks!{Colors.RESET}")
        print(f"\nNext steps:")
        print(f"  {Colors.GREEN}black app/ tests/{Colors.RESET}          # Format code")
        print(f"  {Colors.GREEN}isort app/ tests/{Colors.RESET}          # Sort imports")
        print(f"  {Colors.GREEN}flake8 app/ tests/{Colors.RESET}         # Lint code")
        print(f"  {Colors.GREEN}mypy app/{Colors.RESET}                  # Type check")
        print(f"\nSee {Colors.BLUE}docs/GUIA_CALIDAD_CODIGO.md{Colors.RESET} for complete guide.")

    # Exit code
    sys.exit(0 if failed_checks == 0 else 1)


if __name__ == "__main__":
    main()
