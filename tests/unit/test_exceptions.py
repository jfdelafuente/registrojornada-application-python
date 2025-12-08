"""Unit tests for app.exceptions module."""

import pytest

from app.exceptions import (
    RegistroJornadaException,
    AuthenticationError,
    OAMRedirectError,
    InvalidCredentialsError,
    NetworkError,
    RegistrationError,
    ReportGenerationError,
    HTMLParsingError,
    InvalidDateError,
    HolidayValidationError,
    NotificationError
)


@pytest.mark.unit
class TestExceptionHierarchy:
    """Test exception hierarchy and inheritance."""

    def test_base_exception_creation(self):
        """Test creating base exception."""
        exc = RegistroJornadaException("Test error")
        assert str(exc) == "Test error"
        assert isinstance(exc, Exception)

    def test_authentication_error_is_base_exception(self):
        """Test AuthenticationError inherits from base."""
        exc = AuthenticationError("Auth failed")
        assert isinstance(exc, RegistroJornadaException)
        assert isinstance(exc, Exception)
        assert str(exc) == "Auth failed"

    def test_oam_redirect_error_is_authentication_error(self):
        """Test OAMRedirectError inherits from AuthenticationError."""
        exc = OAMRedirectError("Redirect needed")
        assert isinstance(exc, AuthenticationError)
        assert isinstance(exc, RegistroJornadaException)

    def test_credentials_error_is_authentication_error(self):
        """Test InvalidCredentialsError inherits from AuthenticationError."""
        exc = InvalidCredentialsError("testuser")
        assert isinstance(exc, AuthenticationError)

    def test_network_error_is_base_exception(self):
        """Test NetworkError inherits from base."""
        exc = NetworkError("Connection failed")
        assert isinstance(exc, RegistroJornadaException)

    def test_registration_error_is_base_exception(self):
        """Test RegistrationError inherits from base."""
        exc = RegistrationError("Registration failed")
        assert isinstance(exc, RegistroJornadaException)

    def test_report_generation_error_is_base_exception(self):
        """Test ReportGenerationError inherits from base."""
        exc = ReportGenerationError("Report failed")
        assert isinstance(exc, RegistroJornadaException)

    def test_html_parsing_error_is_base_exception(self):
        """Test HTMLParsingError inherits from base."""
        exc = HTMLParsingError("Parsing failed")
        assert isinstance(exc, RegistroJornadaException)

    def test_invalid_date_error_is_base_exception(self):
        """Test InvalidDateError inherits from base."""
        exc = InvalidDateError("Invalid date")
        assert isinstance(exc, RegistroJornadaException)

    def test_holiday_validation_error_is_base_exception(self):
        """Test HolidayValidationError inherits from base."""
        exc = HolidayValidationError("Holiday detected")
        assert isinstance(exc, RegistroJornadaException)

    def test_notification_error_is_base_exception(self):
        """Test NotificationError inherits from base."""
        exc = NotificationError("Notification failed")
        assert isinstance(exc, RegistroJornadaException)


@pytest.mark.unit
class TestExceptionCatching:
    """Test exception catching patterns."""

    def test_catch_specific_authentication_error(self):
        """Test catching specific AuthenticationError."""
        try:
            raise AuthenticationError("Login failed")
        except AuthenticationError as e:
            assert str(e) == "Login failed"
        else:
            pytest.fail("Should have caught AuthenticationError")

    def test_catch_oam_redirect_as_authentication_error(self):
        """Test catching OAMRedirectError as AuthenticationError."""
        try:
            raise OAMRedirectError(step="login")
        except AuthenticationError as e:
            assert isinstance(e, OAMRedirectError)
            assert "OAM authentication redirect failed" in str(e)

    def test_catch_all_as_base_exception(self):
        """Test catching any custom exception as base."""
        exceptions_to_test = [
            AuthenticationError("auth"),
            NetworkError("network"),
            RegistrationError("reg"),
            HTMLParsingError("parse"),
            NotificationError("notify")
        ]

        for exc in exceptions_to_test:
            try:
                raise exc
            except RegistroJornadaException as e:
                assert isinstance(e, RegistroJornadaException)
            else:
                pytest.fail(f"Should have caught {type(exc).__name__}")

    def test_exception_with_context(self):
        """Test exceptions with additional context."""
        original_error = ValueError("Original error")

        try:
            try:
                raise original_error
            except ValueError as e:
                raise NetworkError(f"Network failed: {e}") from e
        except NetworkError as e:
            assert "Network failed: Original error" in str(e)
            assert e.__cause__ == original_error


@pytest.mark.unit
class TestExceptionMessages:
    """Test exception messages and formatting."""

    def test_empty_message(self):
        """Test exception with empty message."""
        exc = RegistroJornadaException("")
        assert str(exc) == ""

    def test_multiline_message(self):
        """Test exception with multiline message."""
        exc = RegistroJornadaException("Error occurred:\nLine 1\nLine 2")
        assert "Error occurred" in str(exc)
        assert "Line 1" in str(exc)

    def test_unicode_message(self):
        """Test exception with unicode characters."""
        exc = HolidayValidationError("Día festivo: Año Nuevo")
        assert "Año Nuevo" in str(exc)

    def test_formatted_message(self):
        """Test exception with formatted message."""
        date_str = "2025-12-08"
        exc = InvalidDateError(f"Invalid date format: {date_str}")
        assert date_str in str(exc)
