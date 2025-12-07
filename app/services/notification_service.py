"""Notification service for Telegram messages and alerts."""

import logging
import time
from typing import Optional
from datetime import datetime, timedelta
import telebot
from telebot.apihelper import ApiException

from models.workday import WorkdayRegistration, WeeklyReport
from exceptions import TelegramSendError, RegistroJornadaException

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for sending notifications via Telegram.

    Features:
    - Rate limiting to avoid API limits
    - Automatic retries on failure
    - Fallback to logging if Telegram fails
    - Message templates for common scenarios
    """

    def __init__(
        self,
        bot_token: str,
        chat_id: str = None,
        max_messages_per_minute: int = 20,
        max_retries: int = 3
    ):
        """
        Initialize notification service.

        Args:
            bot_token: Telegram bot token
            chat_id: Default chat ID for notifications
            max_messages_per_minute: Rate limit for messages
            max_retries: Maximum retry attempts for failed sends
        """
        self.bot = telebot.TeleBot(bot_token)
        self.default_chat_id = chat_id
        self.max_messages_per_minute = max_messages_per_minute
        self.max_retries = max_retries

        # Rate limiting
        self._message_timestamps = []
        self._rate_limit_window = timedelta(minutes=1)

    def _check_rate_limit(self):
        """
        Check if rate limit is exceeded.

        Raises:
            TelegramSendError: If rate limit is exceeded
        """
        now = datetime.now()
        cutoff = now - self._rate_limit_window

        # Remove old timestamps
        self._message_timestamps = [
            ts for ts in self._message_timestamps if ts > cutoff
        ]

        if len(self._message_timestamps) >= self.max_messages_per_minute:
            logger.warning(f"Rate limit exceeded: {len(self._message_timestamps)} messages in last minute")
            raise TelegramSendError(
                reason=f"Rate limit exceeded ({self.max_messages_per_minute} messages/minute)"
            )

        self._message_timestamps.append(now)

    def send_message(
        self,
        message: str,
        chat_id: str = None,
        parse_mode: str = "Markdown",
        disable_notification: bool = False
    ) -> bool:
        """
        Send a Telegram message with retries and rate limiting.

        Args:
            message: Message text to send
            chat_id: Telegram chat ID (uses default if None)
            parse_mode: Message parse mode (Markdown, HTML, or None)
            disable_notification: If True, sends silently

        Returns:
            True if sent successfully, False otherwise

        Raises:
            Telegram

SendError: If all retries fail
        """
        chat_id = chat_id or self.default_chat_id

        if not chat_id:
            logger.error("No chat ID provided and no default chat ID configured")
            return False

        # Check rate limit
        try:
            self._check_rate_limit()
        except TelegramSendError as e:
            logger.warning(f"Rate limit hit, message will be logged but not sent: {message[:50]}...")
            return False

        # Retry logic
        for attempt in range(self.max_retries):
            try:
                self.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=parse_mode,
                    disable_notification=disable_notification
                )
                logger.debug(f"Message sent successfully to {chat_id}")
                return True

            except ApiException as e:
                logger.warning(f"Telegram API error (attempt {attempt + 1}/{self.max_retries}): {e}")

                if attempt < self.max_retries - 1:
                    # Exponential backoff
                    sleep_time = 2 ** attempt
                    time.sleep(sleep_time)
                else:
                    # Final attempt failed
                    logger.error(f"Failed to send message after {self.max_retries} attempts")
                    logger.info(f"Message content (logged instead): {message}")
                    raise TelegramSendError(
                        chat_id=chat_id,
                        reason=f"API error after {self.max_retries} retries: {str(e)}"
                    )

            except Exception as e:
                logger.error(f"Unexpected error sending Telegram message: {e}", exc_info=True)
                logger.info(f"Message content (logged instead): {message}")
                return False

        return False

    def send_success(
        self,
        title: str,
        details: str = "",
        chat_id: str = None
    ) -> bool:
        """
        Send a success notification.

        Args:
            title: Success title
            details: Additional details (optional)
            chat_id: Telegram chat ID (optional)

        Returns:
            True if sent successfully
        """
        message = f"✅ *{title}*"
        if details:
            message += f"\n{details}"

        return self.send_message(message, chat_id=chat_id)

    def send_error(
        self,
        error: Exception,
        user_message: str = None,
        chat_id: str = None,
        include_details: bool = False
    ) -> bool:
        """
        Send an error notification.

        Args:
            error: Exception that occurred
            user_message: User-friendly error message (optional)
            chat_id: Telegram chat ID (optional)
            include_details: If True, includes technical details

        Returns:
            True if sent successfully
        """
        message = "❌ *Error*"

        if user_message:
            message += f"\n{user_message}"
        else:
            message += f"\n{str(error)}"

        if include_details and isinstance(error, RegistroJornadaException):
            if error.details:
                details_str = "\n".join(f"• {k}: {v}" for k, v in error.details.items())
                message += f"\n\n*Detalles:*\n{details_str}"

        return self.send_message(message, chat_id=chat_id)

    def send_warning(
        self,
        message: str,
        chat_id: str = None
    ) -> bool:
        """
        Send a warning notification.

        Args:
            message: Warning message
            chat_id: Telegram chat ID (optional)

        Returns:
            True if sent successfully
        """
        formatted_message = f"⚠️ *Advertencia*\n{message}"
        return self.send_message(formatted_message, chat_id=chat_id)

    def send_info(
        self,
        message: str,
        chat_id: str = None
    ) -> bool:
        """
        Send an info notification.

        Args:
            message: Info message
            chat_id: Telegram chat ID (optional)

        Returns:
            True if sent successfully
        """
        formatted_message = f"ℹ️ {message}"
        return self.send_message(formatted_message, chat_id=chat_id)

    def send_workday_confirmation(
        self,
        registration: WorkdayRegistration,
        chat_id: str = None
    ) -> bool:
        """
        Send workday registration confirmation.

        Args:
            registration: WorkdayRegistration object
            chat_id: Telegram chat ID (optional)

        Returns:
            True if sent successfully
        """
        if registration.success:
            message = registration.to_telegram_message()
            return self.send_success("Jornada Registrada", message, chat_id=chat_id)
        else:
            return self.send_error(
                Exception(registration.message),
                "No se pudo registrar la jornada",
                chat_id=chat_id
            )

    def send_weekly_report(
        self,
        report: WeeklyReport,
        chat_id: str = None
    ) -> bool:
        """
        Send weekly report.

        Args:
            report: WeeklyReport object
            chat_id: Telegram chat ID (optional)

        Returns:
            True if sent successfully
        """
        message = report.to_telegram_message()
        return self.send_message(message, chat_id=chat_id)

    def send_help_message(
        self,
        chat_id: str = None
    ) -> bool:
        """
        Send help message with available commands.

        Args:
            chat_id: Telegram chat ID (optional)

        Returns:
            True if sent successfully
        """
        message = """
📋 *Comandos Disponibles*

*/dia* - Registrar jornada de trabajo
  Permite registrar HOY, AYER o una fecha específica

*/info* - Ver informe semanal
  Muestra el resumen de la semana actual

*/infop* - Ver informe semana anterior
  Muestra el resumen de la semana pasada

*/help* - Mostrar este mensaje de ayuda

*/start* - Iniciar el bot

---
💡 *Tip:* Usa /dia para registrar tu jornada diaria
"""
        return self.send_message(message, chat_id=chat_id)

    def send_greeting(
        self,
        username: str = None,
        chat_id: str = None
    ) -> bool:
        """
        Send greeting message.

        Args:
            username: User's username (optional)
            chat_id: Telegram chat ID (optional)

        Returns:
            True if sent successfully
        """
        greeting = "👋 *Hola"
        if username:
            greeting += f" {username}"
        greeting += "*"

        message = f"""{greeting}

Soy el bot de Registro de Jornadas de Orange.

Usa /help para ver los comandos disponibles.
"""
        return self.send_message(message, chat_id=chat_id)
