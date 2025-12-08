"""Unit tests for app.services.notification_service module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from telebot.apihelper import ApiException

from app.services.notification_service import NotificationService
from app.models.workday import WorkdayRegistration, WeeklyReport
from app.models.enums import WorkdayTypeEnum
from app.exceptions import TelegramSendError
from datetime import date


@pytest.mark.unit
class TestNotificationServiceInit:
    """Test NotificationService initialization."""

    def test_initialization_with_token(self):
        """Test service initializes with bot token."""
        service = NotificationService(bot_token="test_token", chat_id="123456")

        assert service.bot is not None
        assert service.default_chat_id == "123456"
        assert service.max_messages_per_minute == 20
        assert service.max_retries == 3

    def test_initialization_custom_limits(self):
        """Test initialization with custom rate limits."""
        service = NotificationService(
            bot_token="test_token",
            max_messages_per_minute=10,
            max_retries=5
        )

        assert service.max_messages_per_minute == 10
        assert service.max_retries == 5

    def test_initialization_without_chat_id(self):
        """Test service can initialize without default chat_id."""
        service = NotificationService(bot_token="test_token")

        assert service.default_chat_id is None


@pytest.mark.unit
class TestRateLimiting:
    """Test rate limiting functionality."""

    def test_rate_limit_not_exceeded(self):
        """Test rate limit check passes when under limit."""
        service = NotificationService(
            bot_token="test_token",
            max_messages_per_minute=5
        )

        # Should not raise
        service._check_rate_limit()
        service._check_rate_limit()

    def test_rate_limit_exceeded(self):
        """Test rate limit check fails when limit exceeded."""
        service = NotificationService(
            bot_token="test_token",
            max_messages_per_minute=2
        )

        # Add messages to exceed limit
        service._message_timestamps.append(datetime.now())
        service._message_timestamps.append(datetime.now())

        with pytest.raises(TelegramSendError) as exc_info:
            service._check_rate_limit()

        assert "Rate limit exceeded" in str(exc_info.value)

    def test_rate_limit_window_cleanup(self):
        """Test old timestamps are removed from rate limit window."""
        service = NotificationService(
            bot_token="test_token",
            max_messages_per_minute=2
        )

        # Add old timestamps (>1 minute ago)
        old_time = datetime.now() - timedelta(minutes=2)
        service._message_timestamps.extend([old_time, old_time])

        # Should not raise because old timestamps are cleaned up
        service._check_rate_limit()
        service._check_rate_limit()

        # Should have 2 new timestamps, old ones removed
        assert len(service._message_timestamps) == 2


@pytest.mark.unit
class TestSendMessage:
    """Test send_message functionality."""

    @patch('telebot.TeleBot.send_message')
    def test_send_message_success(self, mock_send):
        """Test successful message sending."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        result = service.send_message("Test message")

        assert result is True
        mock_send.assert_called_once_with(
            chat_id="123",
            text="Test message",
            parse_mode="Markdown",
            disable_notification=False
        )

    @patch('telebot.TeleBot.send_message')
    def test_send_message_with_custom_chat_id(self, mock_send):
        """Test sending to different chat_id."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        result = service.send_message("Test", chat_id="456")

        assert result is True
        assert mock_send.call_args[1]['chat_id'] == "456"

    def test_send_message_no_chat_id(self):
        """Test sending without chat_id fails gracefully."""
        service = NotificationService(bot_token="test_token")

        result = service.send_message("Test")

        assert result is False

    @patch('telebot.TeleBot.send_message')
    def test_send_message_with_html_parse_mode(self, mock_send):
        """Test sending with HTML parse mode."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        service.send_message("Test", parse_mode="HTML")

        assert mock_send.call_args[1]['parse_mode'] == "HTML"

    @patch('telebot.TeleBot.send_message')
    def test_send_message_retry_on_api_exception(self, mock_send):
        """Test message retry on API exception."""
        service = NotificationService(bot_token="test_token", chat_id="123", max_retries=3)

        # Fail first 2 times, succeed on 3rd
        mock_send.side_effect = [
            ApiException("Error", "error", "error"),
            ApiException("Error", "error", "error"),
            None  # Success
        ]

        result = service.send_message("Test")

        assert result is True
        assert mock_send.call_count == 3

    @patch('telebot.TeleBot.send_message')
    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_send_message_all_retries_fail(self, mock_sleep, mock_send):
        """Test when all retries fail."""
        service = NotificationService(bot_token="test_token", chat_id="123", max_retries=2)

        mock_send.side_effect = ApiException("Error", "error", "error")

        with pytest.raises(TelegramSendError):
            service.send_message("Test")

        assert mock_send.call_count == 2

    @patch('telebot.TeleBot.send_message')
    def test_send_message_unexpected_exception(self, mock_send):
        """Test handling unexpected exceptions."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        mock_send.side_effect = RuntimeError("Unexpected error")

        result = service.send_message("Test")

        assert result is False


@pytest.mark.unit
class TestTemplateMessages:
    """Test template message methods."""

    @patch('telebot.TeleBot.send_message')
    def test_send_success(self, mock_send):
        """Test send_success method."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        result = service.send_success("Operation Complete", "All tasks done")

        assert result is True
        called_message = mock_send.call_args[1]['text']
        assert "✅" in called_message
        assert "Operation Complete" in called_message
        assert "All tasks done" in called_message

    @patch('telebot.TeleBot.send_message')
    def test_send_error(self, mock_send):
        """Test send_error method."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        error = Exception("Something went wrong")
        result = service.send_error(error)

        assert result is True
        called_message = mock_send.call_args[1]['text']
        assert "❌" in called_message
        assert "Error" in called_message

    @patch('telebot.TeleBot.send_message')
    def test_send_error_with_custom_message(self, mock_send):
        """Test send_error with custom user message."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        error = Exception("Technical error")
        result = service.send_error(error, user_message="Please try again later")

        called_message = mock_send.call_args[1]['text']
        assert "Please try again later" in called_message

    @patch('telebot.TeleBot.send_message')
    def test_send_warning(self, mock_send):
        """Test send_warning method."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        result = service.send_warning("Low disk space")

        assert result is True
        called_message = mock_send.call_args[1]['text']
        assert "⚠️" in called_message
        assert "Advertencia" in called_message
        assert "Low disk space" in called_message

    @patch('telebot.TeleBot.send_message')
    def test_send_info(self, mock_send):
        """Test send_info method."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        result = service.send_info("System update available")

        assert result is True
        called_message = mock_send.call_args[1]['text']
        assert "ℹ️" in called_message
        assert "System update available" in called_message


@pytest.mark.unit
class TestWorkdayMessages:
    """Test workday-specific messages."""

    @patch('telebot.TeleBot.send_message')
    def test_send_workday_confirmation_success(self, mock_send):
        """Test sending successful workday confirmation."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        registration = WorkdayRegistration(
            date=date(2025, 12, 8),
            start_time="09:00",
            end_time="18:00",
            workday_type=WorkdayTypeEnum.TELEWORK,
            success=True
        )

        result = service.send_workday_confirmation(registration)

        assert result is True
        called_message = mock_send.call_args[1]['text']
        assert "Jornada Registrada" in called_message

    @patch('telebot.TeleBot.send_message')
    def test_send_workday_confirmation_failure(self, mock_send):
        """Test sending failed workday confirmation."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        registration = WorkdayRegistration(
            date=date(2025, 12, 8),
            start_time="09:00",
            end_time="18:00",
            success=False,
            message="Registration failed"
        )

        result = service.send_workday_confirmation(registration)

        called_message = mock_send.call_args[1]['text']
        assert "No se pudo registrar" in called_message

    @patch('telebot.TeleBot.send_message')
    def test_send_weekly_report(self, mock_send):
        """Test sending weekly report."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        report = WeeklyReport(
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 7)
        )

        workday = WorkdayRegistration(
            date=date(2025, 12, 1),
            start_time="09:00",
            end_time="18:00",
            workday_type=WorkdayTypeEnum.TELEWORK
        )
        report.add_registration(workday)

        result = service.send_weekly_report(report)

        assert result is True
        called_message = mock_send.call_args[1]['text']
        assert "Informe Semanal" in called_message


@pytest.mark.unit
class TestHelpAndGreeting:
    """Test help and greeting messages."""

    @patch('telebot.TeleBot.send_message')
    def test_send_help_message(self, mock_send):
        """Test sending help message."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        result = service.send_help_message()

        assert result is True
        called_message = mock_send.call_args[1]['text']
        assert "Comandos Disponibles" in called_message
        assert "/dia" in called_message
        assert "/info" in called_message
        assert "/help" in called_message

    @patch('telebot.TeleBot.send_message')
    def test_send_greeting_without_username(self, mock_send):
        """Test sending greeting without username."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        result = service.send_greeting()

        assert result is True
        called_message = mock_send.call_args[1]['text']
        assert "Hola" in called_message
        assert "bot de Registro de Jornadas" in called_message

    @patch('telebot.TeleBot.send_message')
    def test_send_greeting_with_username(self, mock_send):
        """Test sending greeting with username."""
        service = NotificationService(bot_token="test_token", chat_id="123")

        result = service.send_greeting(username="Juan")

        called_message = mock_send.call_args[1]['text']
        assert "Hola Juan" in called_message
