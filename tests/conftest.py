"""Shared pytest fixtures for testing."""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import date, datetime
from unittest.mock import Mock, MagicMock

from app.config import Settings, reset_settings
from app.models.workday import WorkdayRegistration, WeeklyReport
from app.models.enums import WorkdayTypeEnum


@pytest.fixture(autouse=True)
def reset_settings_after_test():
    """Reset settings singleton after each test."""
    yield
    reset_settings()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def mock_settings(temp_dir):
    """Create mock settings with temporary directories."""
    return Settings(
        base_dir=temp_dir,
        logs_dir=temp_dir / "logs",
        data_dir=temp_dir / "data",
        holidays_file=temp_dir / "data" / "holidays.json",
        log_level="DEBUG"
    )


@pytest.fixture
def sample_holidays_data():
    """Sample holidays data for testing."""
    return {
        "info": {
            "description": "Test holidays",
            "years": ["2025"],
            "last_updated": "2025-12-08"
        },
        "national": [
            {
                "date": "2025-01-01",
                "name": "Año Nuevo",
                "description": "Primer día del año"
            },
            {
                "date": "2025-12-25",
                "name": "Navidad",
                "description": "Navidad"
            }
        ],
        "regional": {
            "madrid": [
                {
                    "date": "2025-05-02",
                    "name": "Fiesta de la Comunidad de Madrid",
                    "description": "Dos de Mayo"
                }
            ]
        }
    }


@pytest.fixture
def holidays_file(temp_dir, sample_holidays_data):
    """Create a temporary holidays.json file."""
    holidays_path = temp_dir / "data" / "holidays.json"
    holidays_path.parent.mkdir(parents=True, exist_ok=True)

    with open(holidays_path, "w", encoding="utf-8") as f:
        json.dump(sample_holidays_data, f, ensure_ascii=False, indent=2)

    return holidays_path


@pytest.fixture
def sample_workday():
    """Create a sample workday registration."""
    return WorkdayRegistration(
        date=date(2025, 12, 8),
        start_time="09:00",
        end_time="18:00",
        workday_type=WorkdayTypeEnum.TELEWORK,
        location="Home",
        success=True,
        message="Registered successfully",
        hours_worked=9.0
    )


@pytest.fixture
def sample_weekly_report(sample_workday):
    """Create a sample weekly report."""
    report = WeeklyReport(
        start_date=date(2025, 12, 1),
        end_date=date(2025, 12, 7)
    )
    report.add_registration(sample_workday)
    return report


@pytest.fixture
def mock_telegram_bot():
    """Mock Telegram bot instance."""
    bot = Mock()
    bot.send_message = Mock(return_value=True)
    return bot


@pytest.fixture
def mock_http_session():
    """Mock requests.Session for HTTP tests."""
    session = MagicMock()
    session.get = Mock()
    session.post = Mock()
    return session


@pytest.fixture
def mock_auth_response():
    """Mock successful authentication response."""
    response = Mock()
    response.status_code = 200
    response.text = """
    <html>
        <form action="/oam/server/auth_cred_submit">
            <input name="request_id" value="test123"/>
        </form>
    </html>
    """
    response.cookies = {"session": "test_session_cookie"}
    return response


@pytest.fixture
def mock_hr_response():
    """Mock successful HR attendance page response."""
    response = Mock()
    response.status_code = 200
    response.text = """
    <html>
        <table class="attendance">
            <tr>
                <td>08/12/2025</td>
                <td>09:00</td>
                <td>18:00</td>
                <td>9.0</td>
            </tr>
        </table>
    </html>
    """
    return response


@pytest.fixture
def encrypted_credentials_file(temp_dir):
    """Create a temporary encrypted credentials file."""
    creds_path = temp_dir / ".credentials.enc"
    # Mock encrypted content (in real scenario, this would be Fernet encrypted)
    creds_path.write_bytes(b"mock_encrypted_data")
    return creds_path


@pytest.fixture(autouse=True)
def env_vars(monkeypatch, temp_dir):
    """Set up environment variables for tests."""
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("ENVIRONMENT", "test")

    # Set up paths
    monkeypatch.setenv("BASE_DIR", str(temp_dir))
    monkeypatch.setenv("LOGS_DIR", str(temp_dir / "logs"))
    monkeypatch.setenv("DATA_DIR", str(temp_dir / "data"))
