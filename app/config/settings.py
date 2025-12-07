"""Application settings with Pydantic validation."""

import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration with automatic validation.

    All settings are loaded from environment variables (.env file).
    Pydantic automatically validates types and required fields.
    """

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

    # Encryption
    encryption_key: str

    # Bot Configuration (encrypted)
    bot_token_encrypted: str
    chat_id_encrypted: str

    # HR System Credentials (encrypted)
    hr_username_encrypted: str
    hr_password_encrypted: str
    employee_code_encrypted: str

    # Work Schedule
    work_start_time: str = "8:00"
    work_end_time: str = "18:00"
    telework_days: List[int] = [1, 2]  # Monday, Tuesday

    # URLs
    vive_orange_url: str = "https://newvo.orange.es"
    oam_base_url: str = "https://applogin.orange.es"
    registro_jornada_url: str = "https://newvo.orange.es/group/viveorange/registro-de-jornada"
    registro_jornada_api_url: str = "https://newvo.orange.es/api/jsonws/invoke"
    url_rj_accion: str = "https://www.registratujornadaorange.com/RealizarAccion"
    url_rj_informe: str = "https://www.registratujornadaorange.com/ObtenerContenidoInformeGeneral"

    # Legacy URL aliases for backward compatibility
    @property
    def registro_accion_url(self) -> str:
        """Legacy alias for url_rj_accion."""
        return self.url_rj_accion

    @property
    def registro_informe_url(self) -> str:
        """Legacy alias for url_rj_informe."""
        return self.url_rj_informe

    # Paths
    @property
    def base_dir(self) -> Path:
        """Get base directory of the project."""
        return Path(__file__).parent.parent.parent

    @property
    def config_dir(self) -> Path:
        """Get config directory path."""
        return self.base_dir / "config"

    @property
    def logs_dir(self) -> Path:
        """Get logs directory path."""
        return self.base_dir / "logs"

    @property
    def app_dir(self) -> Path:
        """Get app directory path."""
        return self.base_dir / "app"

    # Logging
    log_level: str = "INFO"
    log_max_bytes: int = 10 * 1024 * 1024  # 10MB
    log_backup_count: int = 5

    # HTTP Client
    http_timeout: int = 30
    http_max_retries: int = 3
    http_backoff_factor: float = 1.0

    # Regional Settings
    region: str = "madrid"
    timezone: str = "Europe/Madrid"

    def get_log_file(self, name: str) -> str:
        """
        Get full path for a log file.

        Args:
            name: Name of the log file (e.g., 'app.log')

        Returns:
            Full path to log file as string
        """
        self.logs_dir.mkdir(exist_ok=True)
        return str(self.logs_dir / name)


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get singleton instance of Settings.

    Returns:
        Settings instance

    Example:
        >>> settings = get_settings()
        >>> print(settings.work_start_time)
        '8:00'
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
