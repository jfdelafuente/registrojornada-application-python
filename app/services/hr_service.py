"""HR service for workday registration and reporting."""

from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from typing import Tuple, List
import logging
import requests
from config import get_settings
from models.workday import WorkdayRegistration, WeeklyReport, WorkdayTypeEnum
from exceptions import (
    RegistrationError,
    ReportGenerationError,
    HTMLParsingError,
    ValidationError
)

logger = logging.getLogger(__name__)


class HRService:
    """
    Service for handling HR operations in ViveOrange system.

    Manages:
    1. Workday registration
    2. Weekly report generation
    3. Report parsing and formatting
    """

    def __init__(self):
        """Initialize HR service with settings."""
        self.settings = get_settings()

    def register_workday(
        self,
        session: requests.Session,
        work_date: date,
        start_time: str,
        end_time: str,
        workday_type: WorkdayTypeEnum = WorkdayTypeEnum.TELEWORK,
        location: str = ""
    ) -> WorkdayRegistration:
        """
        Register a workday in ViveOrange system.

        Args:
            session: Authenticated session
            work_date: Date of work
            start_time: Start time (HH:MM)
            end_time: End time (HH:MM)
            workday_type: Type of workday
            location: Work location (e.g., 'La Finca', 'Home')

        Returns:
            WorkdayRegistration with result

        Raises:
            RegistrationError: On registration failure
            ValidationError: On invalid input data
        """
        try:
            # Validate inputs with Pydantic
            registration = WorkdayRegistration(
                date=work_date,
                start_time=start_time,
                end_time=end_time,
                workday_type=workday_type,
                location=location
            )

        except Exception as e:
            # Pydantic validation failed
            logger.error(f"Invalid workday data: {e}")
            raise ValidationError(
                "Invalid workday registration data",
                {'error': str(e)}
            )

        date_str = work_date.strftime("%d/%m/%Y")
        logger.info(f"Registering workday for {date_str} from {start_time} to {end_time}")

        try:
            # Submit registration
            response = session.post(
                self.settings.url_rj_accion,
                data={
                    "tipoAccion": "horaRegistroCargada",
                    "motivo": "1",
                    "fechaini": f"{date_str} {start_time}",
                    "fechafin": f"{date_str} {end_time}",
                    "sede": location,
                    "horaEfectiva": ""
                }
            )
            response.raise_for_status()

            logger.debug(f"Registration response status: {response.status_code}")

            # Check for success indicators in response
            html_text = response.text
            if response.status_code == 200 and "error" not in html_text.lower():
                registration.success = True
                registration.message = f"Registered successfully: {date_str} {start_time}-{end_time}"
                logger.info(f"✓ Workday registered: {date_str}")
            else:
                registration.success = False
                registration.message = "Registration failed - check response"
                logger.warning(f"Registration may have failed for {date_str}")
                raise RegistrationError(
                    date=date_str,
                    reason="Server returned error in response"
                )

            registration.hours_worked = registration.calculate_hours()
            return registration

        except requests.RequestException as e:
            logger.error(f"Network error during workday registration: {e}")
            raise RegistrationError(
                date=date_str,
                reason=f"Network error: {str(e)}"
            )
        except RegistrationError:
            # Re-raise RegistrationError
            raise
        except Exception as e:
            logger.error(f"Unexpected error during workday registration: {e}", exc_info=True)
            raise RegistrationError(
                date=date_str,
                reason=f"Unexpected error: {str(e)}"
            )

    def get_weekly_report(
        self,
        session: requests.Session,
        start_date: date = None,
        end_date: date = None,
        previous_week: bool = False
    ) -> WeeklyReport:
        """
        Get weekly workday report from ViveOrange.

        Args:
            session: Authenticated session
            start_date: Week start date (defaults to current Monday)
            end_date: Week end date (defaults to current Friday)
            previous_week: If True, get previous week's report

        Returns:
            WeeklyReport with all registrations

        Raises:
            ReportGenerationError: On report generation failure
        """
        try:
            # Calculate date range
            if start_date is None or end_date is None:
                # Default to current week (Monday to Friday)
                monday = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
                friday = monday + timedelta(days=4)

                if previous_week:
                    monday = monday - timedelta(days=7)
                    friday = monday + timedelta(days=4)

                start_date = monday.date()
                end_date = friday.date()

            start_str = start_date.strftime("%d/%m/%Y")
            end_str = end_date.strftime("%d/%m/%Y")

            logger.info(f"Fetching weekly report from {start_str} to {end_str}")

            # Request report
            response = session.post(
                self.settings.url_rj_informe,
                data={
                    "tipoInforme": "1",
                    "movil": "0",
                    "num": "0",
                    "seleccionFechaInicio": start_str,
                    "seleccionFechaFin": end_str
                }
            )
            response.raise_for_status()

            logger.debug(f"Report response status: {response.status_code}")

            # Parse HTML response
            report = self._parse_report_html(response.text, start_date, end_date)
            logger.info(f"✓ Report parsed: {report.total_days} days, {report.total_hours:.2f} hours")

            return report

        except requests.RequestException as e:
            logger.error(f"Network error fetching weekly report: {e}")
            raise ReportGenerationError(
                report_type="weekly",
                reason=f"Network error: {str(e)}"
            )
        except HTMLParsingError:
            # Re-raise HTML parsing errors
            raise
        except Exception as e:
            logger.error(f"Unexpected error generating report: {e}", exc_info=True)
            raise ReportGenerationError(
                report_type="weekly",
                reason=f"Unexpected error: {str(e)}"
            )

    def _parse_report_html(
        self,
        html_text: str,
        start_date: date,
        end_date: date
    ) -> WeeklyReport:
        """
        Parse HTML report into structured WeeklyReport.

        Args:
            html_text: HTML response from ViveOrange
            start_date: Report start date
            end_date: Report end date

        Returns:
            Populated WeeklyReport
        """
        report = WeeklyReport(
            start_date=start_date,
            end_date=end_date
        )

        try:
            soup = BeautifulSoup(html_text, 'lxml')
            rows = soup.select('#tblEventos > tbody > tr')

            if not rows:
                # No rows found - might be no data or wrong selector
                logger.warning("No report rows found in HTML")
                return report

            for row in rows:
                try:
                    # Extract data from table columns
                    # Column 1: Employee code
                    # Column 2: Employee name
                    # Column 3: Start date/time
                    # Column 4: Type/Location
                    # Column 5: End date/time
                    # Column 6: Duration

                    start_elem = row.select_one('td:nth-child(3)')
                    type_elem = row.select_one('td:nth-child(4)')
                    end_elem = row.select_one('td:nth-child(5)')

                    if not start_elem or not type_elem or not end_elem:
                        logger.warning("Missing table columns in row, skipping")
                        continue

                    start_str = start_elem.text.strip()
                    type_location = type_elem.text.strip()
                    end_str = end_elem.text.strip()

                    logger.debug(f"Parsing row: {start_str} | {type_location} | {end_str}")

                    # Parse dates and times
                    start_dt = datetime.strptime(start_str, '%d/%m/%Y %H:%M')
                    end_dt = datetime.strptime(end_str, '%d/%m/%Y %H:%M')

                    # Determine workday type from location text
                    workday_type = WorkdayTypeEnum.TELEWORK
                    location = ""

                    if "TELETRABAJO" in type_location.upper():
                        workday_type = WorkdayTypeEnum.TELEWORK
                        location = "Home"
                    elif "FINCA" in type_location.upper():
                        workday_type = WorkdayTypeEnum.OFFICE
                        location = "La Finca"
                    elif "OFICINA" in type_location.upper():
                        workday_type = WorkdayTypeEnum.OFFICE
                        location = type_location

                    # Create registration
                    registration = WorkdayRegistration(
                        date=start_dt.date(),
                        start_time=start_dt.strftime('%H:%M'),
                        end_time=end_dt.strftime('%H:%M'),
                        workday_type=workday_type,
                        location=location,
                        success=True,
                        message="Retrieved from report"
                    )

                    registration.hours_worked = registration.calculate_hours()
                    report.add_registration(registration)

                except Exception as e:
                    logger.warning(f"Failed to parse report row: {e}")
                    continue

        except Exception as e:
            logger.error(f"Critical error parsing report HTML: {e}", exc_info=True)
            raise HTMLParsingError(element="report table")

        return report

    def format_report_message(self, report: WeeklyReport) -> str:
        """
        Format weekly report as a user-friendly message.

        Args:
            report: WeeklyReport to format

        Returns:
            Formatted message string
        """
        return report.to_telegram_message()
