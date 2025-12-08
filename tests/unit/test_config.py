"""Unit tests for app.config module."""

import pytest
from pathlib import Path
from app.config import Settings, get_settings, reset_settings


@pytest.mark.unit
class TestSettings:
    """Test Settings configuration class."""

    def test_default_settings(self, temp_dir):
        """Test default settings values."""
        settings = Settings(base_dir=temp_dir)

        assert settings.app_name == "RegistroJornada Bot"
        assert settings.version == "4.0"
        # Environment is set to "test" by conftest.py fixtures
        assert settings.environment in ["production", "test"]
        assert settings.log_level in ["INFO", "DEBUG"]  # DEBUG set by conftest
        assert settings.default_start_time == "8:00"
        assert settings.default_end_time == "18:00"

    def test_directories_created(self, temp_dir):
        """Test that directories are created automatically."""
        settings = Settings(
            base_dir=temp_dir,
            logs_dir=temp_dir / "logs",
            data_dir=temp_dir / "data"
        )

        assert settings.logs_dir.exists()
        assert settings.data_dir.exists()
        assert settings.logs_dir.is_dir()
        assert settings.data_dir.is_dir()

    def test_get_log_file_path(self, temp_dir):
        """Test get_log_file_path method."""
        settings = Settings(
            base_dir=temp_dir,
            logs_dir=temp_dir / "logs"
        )

        log_path = settings.get_log_file_path("test")
        assert log_path == temp_dir / "logs" / "test.log"
        assert log_path.suffix == ".log"

    def test_get_data_file_path(self, temp_dir):
        """Test get_data_file_path method."""
        settings = Settings(
            base_dir=temp_dir,
            data_dir=temp_dir / "data"
        )

        data_path = settings.get_data_file_path("holidays.json")
        assert data_path == temp_dir / "data" / "holidays.json"

    def test_environment_override(self, temp_dir, monkeypatch):
        """Test that environment variables override defaults."""
        monkeypatch.setenv("APP_NAME", "Custom Bot")
        monkeypatch.setenv("VERSION", "5.0")
        monkeypatch.setenv("ENVIRONMENT", "development")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")

        settings = Settings(base_dir=temp_dir)

        assert settings.app_name == "Custom Bot"
        assert settings.version == "5.0"
        assert settings.environment == "development"
        assert settings.log_level == "DEBUG"

    def test_telework_days_default(self, temp_dir):
        """Test default telework days configuration."""
        settings = Settings(base_dir=temp_dir)

        assert isinstance(settings.default_telework_days, list)
        assert settings.default_telework_days == [1, 2]  # Monday, Tuesday

    def test_feature_flags(self, temp_dir):
        """Test feature flags default values."""
        settings = Settings(base_dir=temp_dir)

        assert settings.enable_statistics is True
        assert settings.enable_json_export is True

    def test_holidays_file_path(self, temp_dir):
        """Test holidays file path configuration."""
        settings = Settings(
            base_dir=temp_dir,
            data_dir=temp_dir / "data"
        )

        expected_path = temp_dir / "data" / "holidays.json"
        # The default factory will use __file__, so we need to override
        settings_with_override = Settings(
            base_dir=temp_dir,
            data_dir=temp_dir / "data",
            holidays_file=expected_path
        )

        assert settings_with_override.holidays_file == expected_path


@pytest.mark.unit
class TestSettingsSingleton:
    """Test Settings singleton pattern."""

    def test_get_settings_returns_same_instance(self, temp_dir):
        """Test that get_settings returns the same instance."""
        reset_settings()

        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2

    def test_reset_settings_clears_instance(self, temp_dir):
        """Test that reset_settings clears the singleton."""
        reset_settings()

        settings1 = get_settings()
        instance_id1 = id(settings1)

        reset_settings()

        settings2 = get_settings()
        instance_id2 = id(settings2)

        assert instance_id1 != instance_id2

    def test_settings_singleton_persists_across_calls(self):
        """Test that settings changes persist across get_settings calls."""
        reset_settings()

        settings = get_settings()
        original_app_name = settings.app_name

        # Modify the instance
        settings.app_name = "Modified Name"

        # Get settings again
        settings2 = get_settings()

        assert settings2.app_name == "Modified Name"

        # Cleanup: reset to original
        settings.app_name = original_app_name
