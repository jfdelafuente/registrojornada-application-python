"""Secure logging with sanitization of sensitive data."""

import logging
import re
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class SanitizedFormatter(logging.Formatter):
    """
    Logging formatter that sanitizes sensitive information.

    Automatically redacts:
    - Passwords
    - Tokens and API keys
    - Session IDs and cookies
    - Authentication headers
    - Credit card numbers
    - Email addresses (optional)
    """

    # Patterns to sanitize (pattern, replacement)
    PATTERNS = [
        # Passwords in various formats
        (
            r'(password|Password|PASSWORD|pass|Pass|PASS|pwd|Pwd|PWD)["\']?\s*[:=]\s*["\']?([^"\'}\s,]+)',
            r"\1=***",
        ),
        # Tokens and keys
        (
            r'(token|Token|TOKEN|key|Key|KEY|api[_-]?key)["\']?\s*[:=]\s*["\']?([^"\'}\s,]+)',
            r"\1=***",
        ),
        # Session IDs and cookies
        (
            r'(JSESSIONID|sessionid|session_id|Cookie|cookie)["\']?\s*[:=]\s*["\']?([^"\'}\s,;]+)',
            r"\1=***",
        ),
        # Authentication
        (
            r'(auth|Auth|AUTH|authorization|Authorization)["\']?\s*[:=]\s*["\']?([^"\'}\s,]+)',
            r"\1=***",
        ),
        # Bearer tokens
        (r"Bearer\s+([A-Za-z0-9\-._~+/]+=*)", r"Bearer ***"),
        # HTML password inputs
        (r'(<input[^>]*type=["\']password["\'][^>]*value=["\'])([^"\']+)(["\'])', r"\1***\3"),
        # JSON password fields
        (r'("password"\s*:\s*")([^"]+)(")', r"\1***\3"),
        # Credit card numbers (basic pattern)
        (r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", r"****-****-****-****"),
        # Employee codes (DNI/NIE pattern - Spanish)
        (r"\b[0-9]{8}[A-Z]\b", r"********X"),
    ]

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record and sanitize sensitive data.

        Args:
            record: The log record to format

        Returns:
            Formatted and sanitized log message
        """
        # Get the formatted message
        message = super().format(record)

        # Apply all sanitization patterns
        for pattern, replacement in self.PATTERNS:
            message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)

        return message


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    console: bool = False,
) -> logging.Logger:
    """
    Configure logger with rotation and sanitization.

    Args:
        name: Logger name
        log_file: Path to log file (None for console only)
        level: Logging level (default: INFO)
        max_bytes: Max file size before rotation (default: 10MB)
        backup_count: Number of backup files to keep (default: 5)
        console: Also log to console (default: False)

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logger('myapp', 'logs/app.log', logging.DEBUG)
        >>> logger.info('Application started')
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Create formatter
    formatter = SanitizedFormatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Add file handler if log_file specified
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Create rotating file handler
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)

    # Add console handler if requested
    if console or not log_file:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)
        logger.addHandler(console_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger by name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
