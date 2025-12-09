"""Input validation for user data and configuration."""

import re
from datetime import date, datetime
from typing import Optional


class InputValidator:
    """
    Validates user inputs and configuration data.

    Provides static methods for validating different types of inputs
    to prevent injection attacks and ensure data integrity.
    """

    @staticmethod
    def validate_employee_code(code: str) -> int:
        """
        Validate employee code is a valid integer.

        Args:
            code: Employee code as string

        Returns:
            Employee code as integer

        Raises:
            ValueError: If code is not a valid integer

        Example:
            >>> InputValidator.validate_employee_code("12345")
            12345
            >>> InputValidator.validate_employee_code("ABC")
            ValueError: Invalid employee code
        """
        if not code or not isinstance(code, str):
            raise ValueError("Employee code cannot be empty")

        # Remove whitespace
        code = code.strip()

        # Check if numeric
        if not re.match(r"^\d+$", code):
            raise ValueError(f"Invalid employee code: {code}. Must be numeric.")

        return int(code)

    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        """
        Validate date string is in YYYYMMDD format.

        Args:
            date_str: Date string to validate

        Returns:
            True if valid, False otherwise

        Example:
            >>> InputValidator.validate_date_format("20240615")
            True
            >>> InputValidator.validate_date_format("2024-06-15")
            False
        """
        if not date_str or not isinstance(date_str, str):
            return False

        # Check format
        if not re.match(r"^\d{8}$", date_str):
            return False

        # Try to parse as date
        try:
            datetime.strptime(date_str, "%Y%m%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_url(url: str, require_https: bool = True) -> bool:
        """
        Validate URL is properly formed and secure.

        Args:
            url: URL to validate
            require_https: Require HTTPS protocol (default: True)

        Returns:
            True if valid, False otherwise

        Example:
            >>> InputValidator.validate_url("https://example.com")
            True
            >>> InputValidator.validate_url("http://example.com", require_https=False)
            True
            >>> InputValidator.validate_url("ftp://example.com")
            False
        """
        if not url or not isinstance(url, str):
            return False

        # Basic URL pattern
        url_pattern = (
            r"^https?://[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}(:[0-9]{1,5})?(/.*)?$"
        )

        if not re.match(url_pattern, url):
            return False

        # Check HTTPS requirement
        if require_https and not url.startswith("https://"):
            return False

        return True

    @staticmethod
    def validate_chat_id(chat_id: str) -> bool:
        """
        Validate Telegram chat ID format.

        Args:
            chat_id: Chat ID to validate

        Returns:
            True if valid, False otherwise

        Example:
            >>> InputValidator.validate_chat_id("123456789")
            True
            >>> InputValidator.validate_chat_id("-100123456789")
            True
        """
        if not chat_id or not isinstance(chat_id, str):
            return False

        # Telegram chat IDs are integers, can be negative for groups
        return bool(re.match(r"^-?\d+$", chat_id.strip()))

    @staticmethod
    def validate_time_format(time_str: str) -> bool:
        """
        Validate time string is in HH:MM format.

        Args:
            time_str: Time string to validate

        Returns:
            True if valid, False otherwise

        Example:
            >>> InputValidator.validate_time_format("08:00")
            True
            >>> InputValidator.validate_time_format("8:00")
            False
        """
        if not time_str or not isinstance(time_str, str):
            return False

        # Check HH:MM format
        if not re.match(r"^\d{2}:\d{2}$", time_str):
            return False

        # Validate hours and minutes
        try:
            hours, minutes = map(int, time_str.split(":"))
            return 0 <= hours <= 23 and 0 <= minutes <= 59
        except (ValueError, AttributeError):
            return False

    @staticmethod
    def sanitize_string(input_str: str, max_length: int = 1000) -> str:
        """
        Sanitize string input by removing potential dangerous characters.

        Args:
            input_str: String to sanitize
            max_length: Maximum allowed length (default: 1000)

        Returns:
            Sanitized string

        Example:
            >>> InputValidator.sanitize_string("<script>alert('xss')</script>")
            "scriptalert('xss')/script"
        """
        if not input_str or not isinstance(input_str, str):
            return ""

        # Truncate to max length
        sanitized = input_str[:max_length]

        # Remove HTML tags
        sanitized = re.sub(r"<[^>]+>", "", sanitized)

        # Remove control characters except newline and tab
        sanitized = re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]", "", sanitized)

        return sanitized.strip()

    @staticmethod
    def validate_date_range(start_date: date, end_date: date) -> bool:
        """
        Validate that date range is logical.

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            True if valid range (start <= end), False otherwise

        Example:
            >>> from datetime import date
            >>> InputValidator.validate_date_range(date(2024, 1, 1), date(2024, 12, 31))
            True
        """
        if not isinstance(start_date, date) or not isinstance(end_date, date):
            return False

        return start_date <= end_date
