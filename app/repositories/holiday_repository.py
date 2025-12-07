"""Repository for managing holidays and vacation data."""

import json
from pathlib import Path
from datetime import date
from typing import List, Dict, Optional
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


class HolidayRepository:
    """
    Repository for managing holiday data from JSON configuration.

    Provides methods to check if a date is a holiday, vacation,
    or occasional telework day.
    """

    def __init__(self, config_path: Path):
        """
        Initialize repository with config path.

        Args:
            config_path: Path to config directory containing holidays.json
        """
        self.config_path = config_path
        self._holidays_data = self._load_holidays()

    def _load_holidays(self) -> Dict:
        """
        Load holidays from JSON file.

        Returns:
            Dictionary with holidays data

        Raises:
            FileNotFoundError: If holidays.json not found
            json.JSONDecodeError: If JSON is invalid
        """
        holidays_file = self.config_path / "holidays.json"

        if not holidays_file.exists():
            logger.warning(f"Holidays file not found: {holidays_file}")
            return {
                "annual_holidays": [],
                "regional_holidays": {},
                "movable_holidays": {},
                "personal_vacations": {},
                "occasional_telework": {}
            }

        try:
            with open(holidays_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Loaded holidays from {holidays_file}")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing holidays.json: {e}")
            raise

    @lru_cache(maxsize=365)
    def is_annual_holiday(self, check_date: date) -> bool:
        """
        Check if date is an annual holiday (national).

        Args:
            check_date: Date to check

        Returns:
            True if it's an annual holiday

        Example:
            >>> repo = HolidayRepository(Path("config"))
            >>> repo.is_annual_holiday(date(2024, 1, 1))  # New Year
            True
        """
        date_str = check_date.strftime("%d/%m")
        return any(
            h["date"] == date_str
            for h in self._holidays_data.get("annual_holidays", [])
        )

    @lru_cache(maxsize=365)
    def is_regional_holiday(self, check_date: date, region: str = "madrid") -> bool:
        """
        Check if date is a regional holiday.

        Args:
            check_date: Date to check
            region: Region name (default: madrid)

        Returns:
            True if it's a regional holiday
        """
        date_str = check_date.strftime("%d/%m")
        year = str(check_date.year)

        regional = self._holidays_data.get("regional_holidays", {}).get(region, {})
        if year in regional:
            return any(h["date"] == date_str for h in regional[year])

        return False

    @lru_cache(maxsize=365)
    def is_movable_holiday(self, check_date: date) -> bool:
        """
        Check if date is a movable holiday (e.g., Easter).

        Args:
            check_date: Date to check

        Returns:
            True if it's a movable holiday
        """
        date_str = check_date.strftime("%d/%m")
        year = str(check_date.year)

        movable = self._holidays_data.get("movable_holidays", {}).get(year, [])
        return any(h["date"] == date_str for h in movable)

    @lru_cache(maxsize=365)
    def is_holiday(self, check_date: date, region: str = "madrid") -> bool:
        """
        Check if date is any type of holiday.

        Combines annual, regional, and movable holidays.

        Args:
            check_date: Date to check
            region: Region name (default: madrid)

        Returns:
            True if it's a holiday
        """
        return (
            self.is_annual_holiday(check_date) or
            self.is_regional_holiday(check_date, region) or
            self.is_movable_holiday(check_date)
        )

    def get_holiday_name(self, check_date: date, region: str = "madrid") -> Optional[str]:
        """
        Get the name of the holiday.

        Args:
            check_date: Date to check
            region: Region name

        Returns:
            Holiday name or None if not a holiday
        """
        date_str = check_date.strftime("%d/%m")
        year = str(check_date.year)

        # Check annual holidays
        for h in self._holidays_data.get("annual_holidays", []):
            if h["date"] == date_str:
                return h["name"]

        # Check regional holidays
        regional = self._holidays_data.get("regional_holidays", {}).get(region, {})
        if year in regional:
            for h in regional[year]:
                if h["date"] == date_str:
                    return h["name"]

        # Check movable holidays
        movable = self._holidays_data.get("movable_holidays", {}).get(year, [])
        for h in movable:
            if h["date"] == date_str:
                return h["name"]

        return None

    @lru_cache(maxsize=365)
    def is_personal_vacation(self, check_date: date) -> bool:
        """
        Check if date is personal vacation.

        Args:
            check_date: Date to check

        Returns:
            True if it's a vacation day
        """
        date_str = check_date.strftime("%d/%m/%Y")
        year = str(check_date.year)

        vacations = self._holidays_data.get("personal_vacations", {}).get(year, [])
        return any(v["date"] == date_str for v in vacations)

    @lru_cache(maxsize=365)
    def is_occasional_telework(self, check_date: date) -> bool:
        """
        Check if date is occasional telework.

        Args:
            check_date: Date to check

        Returns:
            True if it's an occasional telework day
        """
        date_str = check_date.strftime("%d/%m/%Y")
        year = str(check_date.year)

        telework = self._holidays_data.get("occasional_telework", {}).get(year, [])
        return any(t["date"] == date_str for t in telework)

    def get_holidays_for_year(self, year: int, region: str = "madrid") -> List[Dict]:
        """
        Get all holidays for a specific year.

        Args:
            year: Year to get holidays for
            region: Region name

        Returns:
            List of holiday dictionaries
        """
        holidays = []
        year_str = str(year)

        # Annual holidays (apply to all years)
        for h in self._holidays_data.get("annual_holidays", []):
            holidays.append({
                "date": f"{h['date']}/{year}",
                "name": h["name"],
                "type": h["type"]
            })

        # Regional holidays
        regional = self._holidays_data.get("regional_holidays", {}).get(region, {})
        if year_str in regional:
            for h in regional[year_str]:
                holidays.append({
                    "date": f"{h['date']}/{year}",
                    "name": h["name"],
                    "type": "regional"
                })

        # Movable holidays
        movable = self._holidays_data.get("movable_holidays", {}).get(year_str, [])
        for h in movable:
            holidays.append({
                "date": f"{h['date']}/{year}",
                "name": h["name"],
                "type": "movable"
            })

        return holidays

    def clear_cache(self):
        """Clear the LRU cache."""
        self.is_annual_holiday.cache_clear()
        self.is_regional_holiday.cache_clear()
        self.is_movable_holiday.cache_clear()
        self.is_holiday.cache_clear()
        self.is_personal_vacation.cache_clear()
        self.is_occasional_telework.cache_clear()
        logger.info("Holiday cache cleared")

    def reload(self):
        """Reload holidays from file and clear cache."""
        self._holidays_data = self._load_holidays()
        self.clear_cache()
        logger.info("Holidays reloaded from file")
