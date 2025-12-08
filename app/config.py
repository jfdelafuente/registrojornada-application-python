"""Application configuration using Pydantic Settings."""

from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Application settings using Pydantic Settings.

    Loads configuration from environment variables and .env file.
    Provides type-safe configuration with validation.

    Example:
        >>> settings = get_settings()
        >>> print(settings.app_name)
        'RegistroJornada Bot'
    """

    # Application metadata
    app_name: str = Field(default="RegistroJornada Bot", description="Application name")
    version: str = Field(default="4.0", description="Application version")
    environment: str = Field(default="production", description="Environment (dev/staging/production)")

    # Paths
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent, description="Base directory")
    logs_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "logs", description="Logs directory")
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data", description="Data directory")

    # ViveOrange OAM URLs
    vive_orange_url: str = Field(
        default="https://viveorange.orange.es/irj/portal",
        description="ViveOrange portal URL"
    )
    oam_base_url: str = Field(
        default="https://login.orange.es/oam/server",
        description="OAM authentication base URL"
    )

    # HR System URLs
    hr_attendance_url: str = Field(
        default="https://viveorange.orange.es/irj/servlet/prt/portal/prtroot/pcd!3aportal_content!2fOrange!2fOrangeRoles!2fOrange.RRHH_MisHorarios!2fOrange.RRHH_MisHorarios?NavMode=1",
        description="HR attendance registration URL"
    )

    # Holidays configuration
    holidays_file: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent / "data" / "holidays.json",
        description="Path to holidays JSON file"
    )

    # Telegram configuration (optional, can be overridden)
    default_chat_id: Optional[int] = Field(default=None, description="Default Telegram chat ID")
    telegram_api_timeout: int = Field(default=30, description="Telegram API timeout in seconds")
    telegram_rate_limit: int = Field(default=20, description="Max messages per minute to Telegram")

    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    log_max_bytes: int = Field(default=10_485_760, description="Max log file size (10MB)")
    log_backup_count: int = Field(default=5, description="Number of log backups to keep")

    # HTTP configuration
    http_timeout: int = Field(default=30, description="HTTP request timeout in seconds")
    http_max_retries: int = Field(default=3, description="Max HTTP retries")
    http_retry_backoff: float = Field(default=0.5, description="Retry backoff factor")

    # Work schedule defaults (can be overridden by configD.py)
    default_start_time: str = Field(default="8:00", description="Default work start time")
    default_end_time: str = Field(default="18:00", description="Default work end time")
    default_telework_days: list[int] = Field(default_factory=lambda: [1, 2], description="Default telework days (1=Monday)")

    # Security
    encryption_algorithm: str = Field(default="Fernet", description="Encryption algorithm")

    # Feature flags
    enable_statistics: bool = Field(default=True, description="Enable statistics generation")
    enable_json_export: bool = Field(default=True, description="Enable JSON export")
    enable_connectivity_check: bool = Field(default=False, description="Enable connectivity checks")

    # Cache configuration
    holiday_cache_size: int = Field(default=128, description="LRU cache size for holidays")

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'  # Ignore extra fields in .env
    )

    def __init__(self, **kwargs):
        """Initialize settings and create directories if needed."""
        super().__init__(**kwargs)

        # Ensure directories exist
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        logger.debug(f"Settings loaded: {self.app_name} v{self.version}")

    def get_log_file_path(self, name: str) -> Path:
        """
        Get path for a log file.

        Args:
            name: Log file name (without .log extension)

        Returns:
            Full path to log file
        """
        return self.logs_dir / f"{name}.log"

    def get_data_file_path(self, name: str) -> Path:
        """
        Get path for a data file.

        Args:
            name: Data file name

        Returns:
            Full path to data file
        """
        return self.data_dir / name


# Global settings instance (singleton)
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global Settings singleton instance.

    Returns:
        Settings singleton

    Example:
        >>> settings = get_settings()
        >>> # All subsequent calls return the same instance
        >>> assert get_settings() is settings
    """
    global _settings_instance

    if _settings_instance is None:
        _settings_instance = Settings()
        logger.info(f"Settings initialized: {_settings_instance.app_name} v{_settings_instance.version}")

    return _settings_instance


def reset_settings():
    """
    Reset the global settings instance.

    Useful for testing or when you need to reload configuration.
    """
    global _settings_instance
    _settings_instance = None
    logger.info("Settings reset")
