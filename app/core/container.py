"""Dependency injection container for services."""

import logging
from typing import Optional

from config import Settings, get_settings
from security.secrets_manager import SecretsManager
from services.auth_service import AuthService
from services.hr_service import HRService
from services.notification_service import NotificationService
from services.report_service import ReportService
from utils.error_handler import ErrorHandler

logger = logging.getLogger(__name__)

# Global singleton instance
_container_instance: Optional["ServiceContainer"] = None


class ServiceContainer:
    """
    Dependency injection container for application services.

    Implements singleton pattern and lazy initialization.
    All services are created on first access and cached.

    Example:
        >>> container = get_container()
        >>> notification = container.notification_service
        >>> auth = container.auth_service
    """

    def __init__(self):
        """Initialize container with None values (lazy loading)."""
        self._settings: Optional[Settings] = None
        self._secrets_manager: Optional[SecretsManager] = None
        self._auth_service: Optional[AuthService] = None
        self._hr_service: Optional[HRService] = None
        self._notification_service: Optional[NotificationService] = None
        self._report_service: Optional[ReportService] = None
        self._error_handler: Optional[ErrorHandler] = None

        logger.debug("ServiceContainer initialized")

    @property
    def settings(self) -> Settings:
        """
        Get application settings.

        Returns:
            Settings instance
        """
        if self._settings is None:
            self._settings = get_settings()
            logger.debug("Settings loaded")
        return self._settings

    @property
    def secrets_manager(self) -> SecretsManager:
        """
        Get secrets manager.

        Returns:
            SecretsManager instance
        """
        if self._secrets_manager is None:
            self._secrets_manager = SecretsManager()
            logger.debug("SecretsManager initialized")
        return self._secrets_manager

    @property
    def auth_service(self) -> AuthService:
        """
        Get authentication service.

        Returns:
            AuthService instance
        """
        if self._auth_service is None:
            self._auth_service = AuthService()
            logger.debug("AuthService initialized")
        return self._auth_service

    @property
    def hr_service(self) -> HRService:
        """
        Get HR service.

        Returns:
            HRService instance
        """
        if self._hr_service is None:
            self._hr_service = HRService()
            logger.debug("HRService initialized")
        return self._hr_service

    @property
    def notification_service(self) -> NotificationService:
        """
        Get notification service.

        Returns:
            NotificationService instance
        """
        if self._notification_service is None:
            # Get decrypted bot token
            bot_token = self.secrets_manager.get_secret("BOT_TOKEN_ENCRYPTED")

            # Get chat ID from settings if available
            chat_id = getattr(self.settings, "default_chat_id", None)

            self._notification_service = NotificationService(bot_token=bot_token, chat_id=chat_id)
            logger.debug("NotificationService initialized")
        return self._notification_service

    @property
    def report_service(self) -> ReportService:
        """
        Get report service.

        Returns:
            ReportService instance
        """
        if self._report_service is None:
            self._report_service = ReportService()
            logger.debug("ReportService initialized")
        return self._report_service

    @property
    def error_handler(self) -> ErrorHandler:
        """
        Get error handler.

        Returns:
            ErrorHandler instance with notification service
        """
        if self._error_handler is None:
            self._error_handler = ErrorHandler(notification_service=self.notification_service)
            logger.debug("ErrorHandler initialized")
        return self._error_handler

    def reset(self):
        """
        Reset all services (useful for testing).

        Warning: This will clear all cached instances.
        """
        self._settings = None
        self._secrets_manager = None
        self._auth_service = None
        self._hr_service = None
        self._notification_service = None
        self._report_service = None
        self._error_handler = None
        logger.info("ServiceContainer reset")


def get_container() -> ServiceContainer:
    """
    Get the global ServiceContainer singleton instance.

    Returns:
        ServiceContainer singleton

    Example:
        >>> container = get_container()
        >>> # All subsequent calls return the same instance
        >>> assert get_container() is container
    """
    global _container_instance

    if _container_instance is None:
        _container_instance = ServiceContainer()
        logger.info("ServiceContainer singleton created")

    return _container_instance


def reset_container():
    """
    Reset the global container instance.

    Useful for testing or when you need to reinitialize all services.
    """
    global _container_instance
    _container_instance = None
    logger.info("Global ServiceContainer reset")
