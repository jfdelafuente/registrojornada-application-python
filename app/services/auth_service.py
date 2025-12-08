"""Authentication service for ViveOrange OAM system."""

from bs4 import BeautifulSoup
from typing import Dict, Optional
import logging
import requests
from app.security.secrets_manager import SecretsManager
from app.config import get_settings
from app.exceptions import (
    AuthenticationError,
    InvalidCredentialsError,
    OAMRedirectError,
    SessionExpiredError,
    HTMLParsingError
)

logger = logging.getLogger(__name__)


class AuthService:
    """
    Service for handling authentication with ViveOrange OAM system.

    Manages the multi-step authentication process including:
    1. Initial ViveOrange request
    2. OAM redirect
    3. Login submission
    4. Session validation
    """

    def __init__(self):
        """Initialize authentication service with credentials."""
        self.settings = get_settings()
        self.secrets = SecretsManager()

        # Decrypt credentials
        self.username = self.secrets.get_secret('HR_USERNAME_ENCRYPTED')
        self.password = self.secrets.get_secret('HR_PASSWORD_ENCRYPTED')
        self.employee_code = self.secrets.get_secret('EMPLOYEE_CODE_ENCRYPTED')

    def authenticate(self, session: requests.Session) -> bool:
        """
        Perform complete authentication flow.

        Args:
            session: Requests session to authenticate

        Returns:
            True if authentication successful, False otherwise

        Raises:
            AuthenticationError: On authentication failure
            OAMRedirectError: On OAM redirect failure
            HTMLParsingError: On HTML parsing failure
        """
        try:
            # Step 1: Initial ViveOrange request
            logger.info("Step 1: Accessing ViveOrange portal...")
            oam_url, oam_data = self._step1_initial_request(session)

            # Step 2: OAM redirect
            logger.info("Step 2: Processing OAM redirect...")
            login_url, login_data = self._step2_oam_redirect(session, oam_url, oam_data)

            # Step 3: Submit login
            logger.info("Step 3: Submitting login credentials...")
            return_url, return_data = self._step3_submit_login(session, login_url, login_data)

            # Step 4: Return to ViveOrange
            logger.info("Step 4: Returning to ViveOrange...")
            self._step4_return_to_viveorange(session, return_url, return_data)

            logger.info("✓ Authentication successful")
            return True

        except (AuthenticationError, OAMRedirectError, HTMLParsingError):
            # Re-raise our custom exceptions
            raise
        except requests.RequestException as e:
            logger.error(f"Network error during authentication: {e}")
            raise AuthenticationError(
                "Network error during authentication",
                {'error': str(e)}
            )
        except Exception as e:
            logger.error(f"Unexpected authentication error: {e}", exc_info=True)
            raise AuthenticationError(
                "Unexpected authentication error",
                {'error': str(e)}
            )

    def _step1_initial_request(
        self,
        session: requests.Session
    ) -> tuple[str, Dict[str, str]]:
        """
        Step 1: Initial request to ViveOrange.

        Args:
            session: Authenticated session

        Returns:
            Tuple of (OAM URL, form data)
        """
        response = session.get(self.settings.vive_orange_url)
        response.raise_for_status()

        logger.debug(f"Initial request status: {response.status_code}")

        # Parse OAM redirect form
        soup = BeautifulSoup(response.text, 'lxml')
        form = soup.select_one('body form')

        if not form:
            raise OAMRedirectError(step="step1_initial_request")

        oam_url = form.get('action')
        if not oam_url:
            raise HTMLParsingError(element="form action attribute")

        oam_data = {}
        for tag in form.find_all("input", type="hidden"):
            oam_data[tag.get("name")] = tag.get("value")

        logger.debug(f"OAM URL: {oam_url}")
        return oam_url, oam_data

    def _step2_oam_redirect(
        self,
        session: requests.Session,
        oam_url: str,
        oam_data: Dict[str, str]
    ) -> tuple[str, Dict[str, str]]:
        """
        Step 2: Handle OAM redirect.

        Args:
            session: Session object
            oam_url: OAM URL from step 1
            oam_data: Form data from step 1

        Returns:
            Tuple of (login URL, login data)
        """
        response = session.post(oam_url, data=oam_data)
        response.raise_for_status()

        logger.debug(f"OAM redirect status: {response.status_code}")

        # Parse login form
        soup = BeautifulSoup(response.text, 'lxml')
        form = soup.select_one('form#loginData')

        if not form:
            raise OAMRedirectError(step="step2_oam_redirect")

        form_action = form.get('action')
        if not form_action:
            raise HTMLParsingError(element="login form action")

        login_url = self.settings.oam_base_url + form_action
        login_data = {}

        # Process form fields
        for tag in form.find_all("input", type="hidden"):
            name = tag.get("name")
            if name == "username":
                login_data["username"] = self.username
            elif name == "password":
                login_data["password"] = self.password
            else:
                login_data[name] = tag.get("value")

        # Add credentials
        login_data["temp-username"] = self.username
        login_data["password"] = self.password

        logger.debug(f"Login URL: {login_url}")
        return login_url, login_data

    def _step3_submit_login(
        self,
        session: requests.Session,
        login_url: str,
        login_data: Dict[str, str]
    ) -> tuple[str, Dict[str, str]]:
        """
        Step 3: Submit login credentials.

        Args:
            session: Session object
            login_url: Login URL from step 2
            login_data: Login form data

        Returns:
            Tuple of (return URL, return data)
        """
        response = session.post(login_url, data=login_data)
        response.raise_for_status()

        logger.debug(f"Login submit status: {response.status_code}")

        # Parse return form
        soup = BeautifulSoup(response.text, 'lxml')
        form = soup.select_one('body form')

        if not form:
            # Login credentials might be invalid
            raise InvalidCredentialsError(username=self.username)

        return_url = form.get('action')
        if not return_url:
            raise HTMLParsingError(element="return form action")
        return_data = {}

        for tag in form.find_all("input", type="hidden"):
            return_data[tag.get("name")] = tag.get("value")

        logger.debug(f"Return URL: {return_url}")
        return return_url, return_data

    def _step4_return_to_viveorange(
        self,
        session: requests.Session,
        return_url: str,
        return_data: Dict[str, str]
    ):
        """
        Step 4: Return to ViveOrange with authentication.

        Args:
            session: Session object
            return_url: Return URL from step 3
            return_data: Return form data
        """
        response = session.post(return_url, data=return_data)
        response.raise_for_status()

        logger.debug(f"Return to ViveOrange status: {response.status_code}")

    def get_employee_code(self) -> str:
        """
        Get decrypted employee code.

        Returns:
            Employee code as string
        """
        return self.employee_code
