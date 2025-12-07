"""Custom exceptions for Registro Jornada application."""


class RegistroJornadaException(Exception):
    """
    Base exception for all application errors.

    All custom exceptions should inherit from this class.
    """

    def __init__(self, message: str, details: dict = None):
        """
        Initialize exception with message and optional details.

        Args:
            message: Human-readable error message
            details: Optional dictionary with additional context
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """String representation of the exception."""
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


# ============================================================================
# Authentication Errors
# ============================================================================


class AuthenticationError(RegistroJornadaException):
    """Base class for authentication-related errors."""
    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when username or password is invalid."""

    def __init__(self, username: str = None):
        details = {'username': username} if username else {}
        super().__init__(
            "Invalid credentials provided",
            details
        )


class SessionExpiredError(AuthenticationError):
    """Raised when session has expired."""

    def __init__(self):
        super().__init__("Session has expired, please re-authenticate")


class OAMRedirectError(AuthenticationError):
    """Raised when OAM redirect fails."""

    def __init__(self, step: str = None):
        details = {'step': step} if step else {}
        super().__init__(
            "OAM authentication redirect failed",
            details
        )


# ============================================================================
# HR Service Errors
# ============================================================================


class HRServiceError(RegistroJornadaException):
    """Base class for HR service operation errors."""
    pass


class RegistrationError(HRServiceError):
    """Raised when workday registration fails."""

    def __init__(self, date: str = None, reason: str = None):
        details = {}
        if date:
            details['date'] = date
        if reason:
            details['reason'] = reason

        super().__init__(
            "Failed to register workday",
            details
        )


class ReportGenerationError(HRServiceError):
    """Raised when report generation fails."""

    def __init__(self, report_type: str = None, reason: str = None):
        details = {}
        if report_type:
            details['report_type'] = report_type
        if reason:
            details['reason'] = reason

        super().__init__(
            "Failed to generate report",
            details
        )


class HTMLParsingError(HRServiceError):
    """Raised when HTML parsing fails."""

    def __init__(self, element: str = None):
        details = {'element': element} if element else {}
        super().__init__(
            "Failed to parse HTML response",
            details
        )


# ============================================================================
# Validation Errors
# ============================================================================


class ValidationError(RegistroJornadaException):
    """Base class for data validation errors."""
    pass


class InvalidDateError(ValidationError):
    """Raised when date is invalid."""

    def __init__(self, date_str: str = None, format_expected: str = None):
        details = {}
        if date_str:
            details['date'] = date_str
        if format_expected:
            details['expected_format'] = format_expected

        super().__init__(
            "Invalid date provided",
            details
        )


class InvalidTimeFormatError(ValidationError):
    """Raised when time format is invalid."""

    def __init__(self, time_str: str = None):
        details = {'time': time_str} if time_str else {}
        super().__init__(
            "Invalid time format (expected HH:MM)",
            details
        )


class InvalidWorkdayTypeError(ValidationError):
    """Raised when workday type is invalid."""

    def __init__(self, workday_type: str = None):
        details = {'workday_type': workday_type} if workday_type else {}
        super().__init__(
            "Invalid workday type",
            details
        )


class HolidayValidationError(ValidationError):
    """Raised when attempting to register on a holiday."""

    def __init__(self, date: str = None, holiday_name: str = None):
        details = {}
        if date:
            details['date'] = date
        if holiday_name:
            details['holiday'] = holiday_name

        super().__init__(
            "Cannot register workday on holiday",
            details
        )


# ============================================================================
# Network Errors
# ============================================================================


class NetworkError(RegistroJornadaException):
    """Base class for network-related errors."""
    pass


class ConnectionTimeoutError(NetworkError):
    """Raised when connection times out."""

    def __init__(self, url: str = None, timeout: int = None):
        details = {}
        if url:
            details['url'] = url
        if timeout:
            details['timeout_seconds'] = timeout

        super().__init__(
            "Connection timed out",
            details
        )


class ServiceUnavailableError(NetworkError):
    """Raised when external service is unavailable."""

    def __init__(self, service_name: str = None, status_code: int = None):
        details = {}
        if service_name:
            details['service'] = service_name
        if status_code:
            details['status_code'] = status_code

        super().__init__(
            "External service is unavailable",
            details
        )


class HTTPError(NetworkError):
    """Raised when HTTP request fails."""

    def __init__(self, status_code: int = None, url: str = None):
        details = {}
        if status_code:
            details['status_code'] = status_code
        if url:
            details['url'] = url

        super().__init__(
            "HTTP request failed",
            details
        )


# ============================================================================
# Configuration Errors
# ============================================================================


class ConfigurationError(RegistroJornadaException):
    """Base class for configuration-related errors."""
    pass


class MissingConfigurationError(ConfigurationError):
    """Raised when required configuration is missing."""

    def __init__(self, config_key: str = None):
        details = {'config_key': config_key} if config_key else {}
        super().__init__(
            "Required configuration is missing",
            details
        )


class InvalidConfigurationError(ConfigurationError):
    """Raised when configuration value is invalid."""

    def __init__(self, config_key: str = None, value: str = None):
        details = {}
        if config_key:
            details['config_key'] = config_key
        if value:
            details['value'] = value

        super().__init__(
            "Configuration value is invalid",
            details
        )


# ============================================================================
# Notification Errors
# ============================================================================


class NotificationError(RegistroJornadaException):
    """Base class for notification-related errors."""
    pass


class TelegramSendError(NotificationError):
    """Raised when Telegram message send fails."""

    def __init__(self, chat_id: str = None, reason: str = None):
        details = {}
        if chat_id:
            details['chat_id'] = chat_id
        if reason:
            details['reason'] = reason

        super().__init__(
            "Failed to send Telegram message",
            details
        )


# ============================================================================
# Repository Errors
# ============================================================================


class RepositoryError(RegistroJornadaException):
    """Base class for repository-related errors."""
    pass


class DataNotFoundError(RepositoryError):
    """Raised when requested data is not found."""

    def __init__(self, resource: str = None, identifier: str = None):
        details = {}
        if resource:
            details['resource'] = resource
        if identifier:
            details['identifier'] = identifier

        super().__init__(
            "Requested data not found",
            details
        )


class DataLoadError(RepositoryError):
    """Raised when data loading fails."""

    def __init__(self, source: str = None, reason: str = None):
        details = {}
        if source:
            details['source'] = source
        if reason:
            details['reason'] = reason

        super().__init__(
            "Failed to load data",
            details
        )


# ============================================================================
# Export all exceptions
# ============================================================================

__all__ = [
    # Base
    'RegistroJornadaException',

    # Authentication
    'AuthenticationError',
    'InvalidCredentialsError',
    'SessionExpiredError',
    'OAMRedirectError',

    # HR Service
    'HRServiceError',
    'RegistrationError',
    'ReportGenerationError',
    'HTMLParsingError',

    # Validation
    'ValidationError',
    'InvalidDateError',
    'InvalidTimeFormatError',
    'InvalidWorkdayTypeError',
    'HolidayValidationError',

    # Network
    'NetworkError',
    'ConnectionTimeoutError',
    'ServiceUnavailableError',
    'HTTPError',

    # Configuration
    'ConfigurationError',
    'MissingConfigurationError',
    'InvalidConfigurationError',

    # Notification
    'NotificationError',
    'TelegramSendError',

    # Repository
    'RepositoryError',
    'DataNotFoundError',
    'DataLoadError',
]
