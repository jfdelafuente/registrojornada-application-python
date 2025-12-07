"""Day validation utilities for workday registration."""

import logging
from datetime import date, datetime, timedelta
from typing import Tuple
from repositories.holiday_repository import HolidayRepository
from config import get_settings

logger = logging.getLogger(__name__)


def validar_dia(day: str) -> date:
    """
    Validate and parse day string.

    Args:
        day: Day string ('HOY', 'AYER', or 'YYYYMMDD' format)

    Returns:
        Parsed date object
    """
    dia = date.today()
    if day == 'HOY':
        return dia
    elif day == 'AYER':
        ayer = dia - timedelta(days=1)
        return ayer
    else:
        try:
            dia = datetime.strptime(day, "%Y%m%d").date()
        except ValueError:
            logger.warning(f"Invalid date format: {day}, returning default date")
            return datetime(2023, 1, 1).date()
    return dia


def dia_validate(dia: date) -> Tuple[str, bool]:
    """
    Validate if a day should be registered.

    Checks for:
    - Holidays (national and regional)
    - Personal vacations
    - Telework days vs office days

    Args:
        dia: Date to validate

    Returns:
        Tuple of (message, should_register)
    """
    settings = get_settings()
    holiday_repo = HolidayRepository()

    mensaje = ''
    registrar = True

    # Check if it's a holiday
    if holiday_repo.is_holiday(dia, region=settings.region):
        holiday_info = holiday_repo.get_holiday_info(dia, region=settings.region)
        if holiday_info:
            mensaje += f'\n🎉 {holiday_info["name"]} (Festivo)'
        else:
            mensaje += '\n🎉 Festivo'
        registrar = False
        logger.debug(f"Day is a holiday: {dia} - {mensaje}")
        return mensaje, registrar

    # Check if it's a personal vacation day
    if holiday_repo.is_personal_vacation(dia):
        mensaje += '\n🏖️ Vacaciones personales'
        registrar = False
        logger.debug(f"Day is a vacation day: {dia}")
        return mensaje, registrar

    # Check telework days configuration
    is_telework_day = dia.isoweekday() in settings.telework_days

    if not is_telework_day:
        # Not a configured telework day
        # Check if it's in the occasional office days list
        registrar = False
        mensaje += '\n🏢 Día de oficina (no teletrabajo configurado)'
        logger.debug(f"Not a telework day: {dia.isoweekday()} not in {settings.telework_days}")
    else:
        # It's a configured telework day
        mensaje += '\n🏠 Día de teletrabajo'
        logger.debug(f"Telework day: {dia}")

    return mensaje, registrar
