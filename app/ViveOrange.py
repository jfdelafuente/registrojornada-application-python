"""ViveOrange client for workday registration - Refactored version."""

from datetime import date
import logging
import requests
from typing import Optional

# Import new architecture components
from config import get_settings
from services.auth_service import AuthService
from services.hr_service import HRService
from models.workday import WorkdayTypeEnum

logger = logging.getLogger(__name__)


class ViveOrange:
    """
    Client for ViveOrange HR system.

    Handles authentication and workday operations using
    separated service layer architecture.
    """

    def __init__(self, registrar: bool = True, pasada: bool = False):
        """
        Initialize ViveOrange client.

        Args:
            registrar: Whether to register workday (True) or just report (False)
            pasada: Whether to get previous week's report (True) or current week (False)
        """
        self.registrar = registrar
        self.pasada = pasada
        self.settings = get_settings()
        self.auth_service = AuthService()
        self.hr_service = HRService()

    def dummy(self, dia: date, msg: str) -> str:
        """
        Dummy method for testing without actual connections.

        Args:
            dia: Date for the dummy operation
            msg: Message to include in dummy response

        Returns:
            Dummy message string
        """
        mensaje = f"Dummy : {str(dia)} - {msg}"
        logger.info(f"ViveOrange Dummy --> '{mensaje}'")
        return mensaje

    def connectar(self, dia: date) -> str:
        """
        Connect to ViveOrange and perform operations.

        This is the main entry point that:
        1. Authenticates with OAM/ViveOrange
        2. Registers workday if requested
        3. Generates weekly report

        Args:
            dia: Date for workday registration

        Returns:
            Formatted message with operation results
        """
        mensaje = ''

        try:
            # Create session
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'
            })

            logger.info("Connecting to ViveOrange...")

            # Step 1: Authenticate
            logger.info("Authenticating with OAM...")
            auth_success = self.auth_service.authenticate(session)

            if not auth_success:
                return "❌ Authentication failed"

            # Step 2: Register workday if requested
            if self.registrar:
                logger.info(f"Registering workday for {dia}...")

                # Use settings for work hours
                start_time = self.settings.work_start_time
                end_time = self.settings.work_end_time

                # Determine workday type based on day of week
                workday_type = (
                    WorkdayTypeEnum.TELEWORK
                    if dia.isoweekday() in self.settings.telework_days
                    else WorkdayTypeEnum.OFFICE
                )

                location = "Home" if workday_type == WorkdayTypeEnum.TELEWORK else "La Finca"

                registration = self.hr_service.register_workday(
                    session=session,
                    work_date=dia,
                    start_time=start_time,
                    end_time=end_time,
                    workday_type=workday_type,
                    location=location
                )

                if registration.success:
                    mensaje += f'\n✅ {registration.message}'
                    logger.info(f"Workday registered successfully")
                else:
                    mensaje += f'\n❌ {registration.message}'
                    logger.warning(f"Workday registration failed")

            # Step 3: Get weekly report
            logger.info("Fetching weekly report...")

            report = self.hr_service.get_weekly_report(
                session=session,
                previous_week=self.pasada
            )

            # Format report message
            report_msg = self.hr_service.format_report_message(report)
            mensaje += f'\n\n{report_msg}'

            logger.info("ViveOrange operation completed successfully")
            return mensaje

        except requests.RequestException as e:
            error_msg = f"❌ Network error: {str(e)}"
            logger.error(f"ViveOrange connection failed: {e}")
            return error_msg

        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)}"
            logger.error(f"ViveOrange operation failed: {e}", exc_info=True)
            return error_msg

        finally:
            # Close session
            if 'session' in locals():
                session.close()
                logger.debug("Session closed")

    def get_employee_code(self) -> str:
        """
        Get employee code from auth service.

        Returns:
            Employee code string
        """
        return self.auth_service.get_employee_code()
