"""Enumerations for the application."""

from enum import Enum


class WorkdayTypeEnum(str, Enum):
    """Types of workday."""

    OFFICE = "office"
    TELEWORK = "telework"
    VACATION = "vacation"
    HOLIDAY = "holiday"
    SICK_LEAVE = "sick_leave"
    PERSONAL_DAY = "personal_day"
