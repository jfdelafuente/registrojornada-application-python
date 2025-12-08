"""Unit tests for app.models module."""

import pytest
from datetime import date
from pydantic import ValidationError

from app.models.workday import WorkdayRegistration, WeeklyReport
from app.models.enums import WorkdayTypeEnum


@pytest.mark.unit
class TestWorkdayTypeEnum:
    """Test WorkdayTypeEnum enumeration."""

    def test_enum_values(self):
        """Test enum has expected values."""
        assert WorkdayTypeEnum.OFFICE.value == "office"
        assert WorkdayTypeEnum.TELEWORK.value == "telework"
        assert WorkdayTypeEnum.VACATION.value == "vacation"
        assert WorkdayTypeEnum.HOLIDAY.value == "holiday"
        assert WorkdayTypeEnum.SICK_LEAVE.value == "sick_leave"
        assert WorkdayTypeEnum.PERSONAL_DAY.value == "personal_day"

    def test_enum_from_string(self):
        """Test creating enum from string value."""
        assert WorkdayTypeEnum("office") == WorkdayTypeEnum.OFFICE
        assert WorkdayTypeEnum("telework") == WorkdayTypeEnum.TELEWORK


@pytest.mark.unit
class TestWorkdayRegistration:
    """Test WorkdayRegistration model."""

    def test_create_valid_workday(self):
        """Test creating a valid workday registration."""
        workday = WorkdayRegistration(
            date=date(2025, 12, 8),
            start_time="09:00",
            end_time="18:00",
            workday_type=WorkdayTypeEnum.TELEWORK,
            location="Home"
        )

        assert workday.date == date(2025, 12, 8)
        assert workday.start_time == "09:00"
        assert workday.end_time == "18:00"
        assert workday.workday_type == WorkdayTypeEnum.TELEWORK
        assert workday.location == "Home"
        assert workday.success is False  # Default value
        assert workday.message == ""  # Default value

    def test_workday_defaults(self):
        """Test default values for optional fields."""
        workday = WorkdayRegistration(
            date=date(2025, 12, 8),
            start_time="09:00",
            end_time="18:00"
        )

        assert workday.workday_type == WorkdayTypeEnum.TELEWORK  # Default
        assert workday.location is None
        assert workday.success is False
        assert workday.message == ""
        assert workday.hours_worked is None

    def test_invalid_time_format(self):
        """Test validation fails for invalid time format."""
        with pytest.raises(ValidationError) as exc_info:
            WorkdayRegistration(
                date=date(2025, 12, 8),
                start_time="25:00",  # Invalid: hour > 23
                end_time="18:00"
            )

        assert "Time must be in HH:MM format" in str(exc_info.value)

    def test_invalid_time_format_end_time(self):
        """Test validation fails for invalid end_time format."""
        with pytest.raises(ValidationError) as exc_info:
            WorkdayRegistration(
                date=date(2025, 12, 8),
                start_time="09:00",
                end_time="not_a_time"  # Invalid format
            )

        assert "Time must be in HH:MM format" in str(exc_info.value)

    def test_calculate_hours_full_day(self):
        """Test calculating hours for a full workday."""
        workday = WorkdayRegistration(
            date=date(2025, 12, 8),
            start_time="09:00",
            end_time="18:00"
        )

        hours = workday.calculate_hours()
        assert hours == 9.0

    def test_calculate_hours_half_day(self):
        """Test calculating hours for a half day."""
        workday = WorkdayRegistration(
            date=date(2025, 12, 8),
            start_time="09:00",
            end_time="13:00"
        )

        hours = workday.calculate_hours()
        assert hours == 4.0

    def test_calculate_hours_with_minutes(self):
        """Test calculating hours with fractional hours."""
        workday = WorkdayRegistration(
            date=date(2025, 12, 8),
            start_time="09:15",
            end_time="17:45"
        )

        hours = workday.calculate_hours()
        assert hours == 8.5

    def test_calculate_hours_empty_times(self):
        """Test calculating hours with empty times returns 0."""
        workday = WorkdayRegistration(
            date=date(2025, 12, 8),
            start_time="",
            end_time=""
        )

        hours = workday.calculate_hours()
        assert hours == 0.0

    def test_to_telegram_message_telework(self):
        """Test Telegram message formatting for telework."""
        workday = WorkdayRegistration(
            date=date(2025, 12, 8),
            start_time="09:00",
            end_time="18:00",
            workday_type=WorkdayTypeEnum.TELEWORK,
            location="Home",
            message="Registered"
        )

        msg = workday.to_telegram_message()

        assert "🏠" in msg  # Telework emoji
        assert "08/12/2025" in msg
        assert "telework" in msg
        assert "Home" in msg
        assert "09:00 - 18:00" in msg
        assert "9.0h" in msg or "9h" in msg
        assert "Registered" in msg

    def test_to_telegram_message_office(self):
        """Test Telegram message formatting for office work."""
        workday = WorkdayRegistration(
            date=date(2025, 12, 8),
            start_time="08:00",
            end_time="17:00",
            workday_type=WorkdayTypeEnum.OFFICE,
            location="La Finca"
        )

        msg = workday.to_telegram_message()

        assert "🏢" in msg  # Office emoji
        assert "office" in msg
        assert "La Finca" in msg

    def test_to_telegram_message_vacation(self):
        """Test Telegram message formatting for vacation."""
        workday = WorkdayRegistration(
            date=date(2025, 12, 8),
            start_time="00:00",
            end_time="00:00",
            workday_type=WorkdayTypeEnum.VACATION
        )

        msg = workday.to_telegram_message()

        assert "🏖️" in msg  # Vacation emoji
        assert "vacation" in msg


@pytest.mark.unit
class TestWeeklyReport:
    """Test WeeklyReport model."""

    def test_create_empty_report(self):
        """Test creating an empty weekly report."""
        report = WeeklyReport(
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 7)
        )

        assert report.start_date == date(2025, 12, 1)
        assert report.end_date == date(2025, 12, 7)
        assert report.total_days == 0
        assert report.telework_days == 0
        assert report.office_days == 0
        assert report.total_hours == 0.0
        assert len(report.registrations) == 0

    def test_add_telework_registration(self):
        """Test adding a telework registration to report."""
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

        assert report.total_days == 1
        assert report.telework_days == 1
        assert report.office_days == 0
        assert report.total_hours == 9.0
        assert len(report.registrations) == 1

    def test_add_office_registration(self):
        """Test adding an office registration to report."""
        report = WeeklyReport(
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 7)
        )

        workday = WorkdayRegistration(
            date=date(2025, 12, 2),
            start_time="08:00",
            end_time="17:00",
            workday_type=WorkdayTypeEnum.OFFICE
        )

        report.add_registration(workday)

        assert report.total_days == 1
        assert report.telework_days == 0
        assert report.office_days == 1
        assert report.total_hours == 9.0

    def test_add_multiple_registrations(self):
        """Test adding multiple registrations to report."""
        report = WeeklyReport(
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 7)
        )

        telework = WorkdayRegistration(
            date=date(2025, 12, 1),
            start_time="09:00",
            end_time="18:00",
            workday_type=WorkdayTypeEnum.TELEWORK
        )

        office = WorkdayRegistration(
            date=date(2025, 12, 2),
            start_time="08:00",
            end_time="16:00",
            workday_type=WorkdayTypeEnum.OFFICE
        )

        report.add_registration(telework)
        report.add_registration(office)

        assert report.total_days == 2
        assert report.telework_days == 1
        assert report.office_days == 1
        assert report.total_hours == 17.0  # 9 + 8

    def test_to_telegram_message_empty(self):
        """Test Telegram message for empty report."""
        report = WeeklyReport(
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 7)
        )

        msg = report.to_telegram_message()

        assert "📊" in msg
        assert "Informe Semanal" in msg
        assert "01/12/2025 - 07/12/2025" in msg
        assert "Días trabajados: 0" in msg

    def test_to_telegram_message_with_data(self):
        """Test Telegram message with report data."""
        report = WeeklyReport(
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 7)
        )

        workday1 = WorkdayRegistration(
            date=date(2025, 12, 1),
            start_time="09:00",
            end_time="18:00",
            workday_type=WorkdayTypeEnum.TELEWORK
        )

        workday2 = WorkdayRegistration(
            date=date(2025, 12, 2),
            start_time="08:00",
            end_time="17:00",
            workday_type=WorkdayTypeEnum.OFFICE
        )

        report.add_registration(workday1)
        report.add_registration(workday2)

        msg = report.to_telegram_message()

        assert "Días trabajados: 2" in msg
        assert "Teletrabajo: 1 días" in msg
        assert "Oficina: 1 días" in msg
        assert "Total horas: 18.00h" in msg  # 9 + 9 = 18 hours
        assert "Detalle:" in msg
        assert "01/12" in msg
        assert "02/12" in msg

    def test_registrations_sorted_by_date(self):
        """Test that registrations are sorted by date in message."""
        report = WeeklyReport(
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 7)
        )

        # Add in reverse order
        workday2 = WorkdayRegistration(
            date=date(2025, 12, 5),
            start_time="09:00",
            end_time="18:00",
            workday_type=WorkdayTypeEnum.TELEWORK
        )

        workday1 = WorkdayRegistration(
            date=date(2025, 12, 3),
            start_time="09:00",
            end_time="18:00",
            workday_type=WorkdayTypeEnum.OFFICE
        )

        report.add_registration(workday2)
        report.add_registration(workday1)

        msg = report.to_telegram_message()

        # Check that dates appear in sorted order
        idx_03 = msg.index("03/12")
        idx_05 = msg.index("05/12")
        assert idx_03 < idx_05
