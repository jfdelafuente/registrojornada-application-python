"""Models for workday registration and reporting."""

from datetime import date as Date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import WorkdayTypeEnum

# Alias for backward compatibility
WorkdayType = WorkdayTypeEnum


class WorkdayRegistration(BaseModel):
    """
    Model for a workday registration.

    Represents a single day's work registration with start/end times,
    type of work, and status.
    """

    date: Date = Field(..., description="Date of the workday")
    start_time: str = Field(..., description="Start time (HH:MM)")
    end_time: str = Field(..., description="End time (HH:MM)")
    workday_type: WorkdayTypeEnum = Field(
        default=WorkdayTypeEnum.TELEWORK, description="Type of workday"
    )
    location: Optional[str] = Field(
        default=None, description="Work location (e.g., 'La Finca', 'Home')"
    )
    success: bool = Field(default=False, description="Registration success status")
    message: str = Field(default="", description="Status message")
    hours_worked: Optional[float] = Field(default=None, description="Total hours worked")

    @field_validator("start_time", "end_time")
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        """Validate time format is HH:MM."""
        if not v:
            return v
        try:
            datetime.strptime(v, "%H:%M")
            return v
        except ValueError:
            raise ValueError(f"Time must be in HH:MM format, got: {v}")

    def calculate_hours(self) -> float:
        """
        Calculate hours worked.

        Returns:
            Hours worked as float
        """
        if not self.start_time or not self.end_time:
            return 0.0

        start = datetime.strptime(f"{self.date} {self.start_time}", "%Y-%m-%d %H:%M")
        end = datetime.strptime(f"{self.date} {self.end_time}", "%Y-%m-%d %H:%M")

        hours = (end - start).total_seconds() / 3600
        return round(hours, 2)

    def to_telegram_message(self) -> str:
        """
        Convert to Telegram message format.

        Returns:
            Formatted message string
        """
        hours = self.calculate_hours()
        type_emoji = {
            WorkdayTypeEnum.OFFICE: "🏢",
            WorkdayTypeEnum.TELEWORK: "🏠",
            WorkdayTypeEnum.VACATION: "🏖️",
            WorkdayTypeEnum.HOLIDAY: "🎉",
            WorkdayTypeEnum.SICK_LEAVE: "🤒",
            WorkdayTypeEnum.PERSONAL_DAY: "📅",
        }

        emoji = type_emoji.get(self.workday_type, "📋")
        location_str = f" ({self.location})" if self.location else ""

        msg = f"{emoji} *{self.date.strftime('%d/%m/%Y')}*\n"
        msg += f"Tipo: {self.workday_type.value}{location_str}\n"
        msg += f"Horario: {self.start_time} - {self.end_time}\n"
        msg += f"Horas: {hours}h\n"

        if self.message:
            msg += f"Estado: {self.message}\n"

        return msg

    model_config = ConfigDict(json_encoders={Date: lambda v: v.strftime("%d/%m/%Y")})


class WeeklyReport(BaseModel):
    """
    Model for weekly work report.

    Aggregates multiple workday registrations into a weekly summary.
    """

    start_date: Date = Field(..., description="Week start date")
    end_date: Date = Field(..., description="Week end date")
    total_days: int = Field(default=0, description="Total days worked")
    telework_days: int = Field(default=0, description="Telework days")
    office_days: int = Field(default=0, description="Office days")
    total_hours: float = Field(default=0.0, description="Total hours worked")
    registrations: list[WorkdayRegistration] = Field(
        default_factory=list, description="List of daily registrations"
    )

    def add_registration(self, registration: WorkdayRegistration):
        """
        Add a registration to the report.

        Args:
            registration: WorkdayRegistration to add
        """
        self.registrations.append(registration)
        self.total_days += 1

        if registration.workday_type == WorkdayTypeEnum.TELEWORK:
            self.telework_days += 1
        elif registration.workday_type == WorkdayTypeEnum.OFFICE:
            self.office_days += 1

        hours = registration.calculate_hours()
        self.total_hours += hours

    def to_telegram_message(self) -> str:
        """
        Convert report to Telegram message format.

        Returns:
            Formatted message string with markdown
        """
        msg = f"📊 *Informe Semanal*\n"
        msg += (
            f"📅 {self.start_date.strftime('%d/%m/%Y')} - {self.end_date.strftime('%d/%m/%Y')}\n\n"
        )

        msg += f"*Resumen:*\n"
        msg += f"• Días trabajados: {self.total_days}\n"
        msg += f"• Teletrabajo: {self.telework_days} días\n"
        msg += f"• Oficina: {self.office_days} días\n"
        msg += f"• Total horas: {self.total_hours:.2f}h\n\n"

        if self.registrations:
            msg += f"*Detalle:*\n"
            for reg in sorted(self.registrations, key=lambda x: x.date):
                type_symbol = "🏠" if reg.workday_type == WorkdayTypeEnum.TELEWORK else "🏢"
                hours = reg.calculate_hours()
                msg += f"{type_symbol} {reg.date.strftime('%d/%m')}: "
                msg += f"{reg.start_time}-{reg.end_time} ({hours:.1f}h)\n"

        return msg

    model_config = ConfigDict(json_encoders={Date: lambda v: v.strftime("%d/%m/%Y")})
