"""HTTP client with automatic retries and connection pooling."""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class HTTPClient:
    """
    HTTP client with automatic retries and connection pooling.

    Features:
    - Automatic retries on failures
    - Connection pooling for better performance
    - Configurable timeouts
    - Exponential backoff
    """

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        pool_connections: int = 10,
        pool_maxsize: int = 20
    ):
        """
        Initialize HTTP client.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            backoff_factor: Backoff factor for retries
            pool_connections: Number of connection pools
            pool_maxsize: Max size of connection pool
        """
        self.timeout = timeout
        self.session = self._create_session(
            max_retries,
            backoff_factor,
            pool_connections,
            pool_maxsize
        )

    def _create_session(
        self,
        max_retries: int,
        backoff_factor: float,
        pool_connections: int,
        pool_maxsize: int
    ) -> requests.Session:
        """
        Create session with retry strategy and connection pooling.

        Args:
            max_retries: Maximum number of retries
            backoff_factor: Backoff factor
            pool_connections: Connection pool count
            pool_maxsize: Max pool size

        Returns:
            Configured requests.Session
        """
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
        )

        # Apply adapter with retry strategy
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize
        )

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'
        })

        return session

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Perform GET request with retries.

        Args:
            url: URL to request
            params: Query parameters
            headers: Additional headers
            **kwargs: Additional arguments for requests

        Returns:
            Response object

        Raises:
            requests.RequestException: On failure after retries
        """
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            logger.debug(f"GET {url} - Status: {response.status_code}")
            return response

        except requests.RequestException as e:
            logger.error(f"GET {url} failed: {e}")
            raise

    def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Perform POST request with retries.

        Args:
            url: URL to request
            data: Form data
            json: JSON data
            headers: Additional headers
            **kwargs: Additional arguments for requests

        Returns:
            Response object

        Raises:
            requests.RequestException: On failure after retries
        """
        try:
            response = self.session.post(
                url,
                data=data,
                json=json,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            logger.debug(f"POST {url} - Status: {response.status_code}")
            return response

        except requests.RequestException as e:
            logger.error(f"POST {url} failed: {e}")
            raise

    def close(self):
        """Close the session."""
        self.session.close()
        logger.debug("HTTP session closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Convenience function to create client with default settings
def create_http_client(
    timeout: int = 30,
    max_retries: int = 3,
    backoff_factor: float = 1.0
) -> HTTPClient:
    """
    Create HTTP client with default or custom settings.

    Args:
        timeout: Request timeout
        max_retries: Maximum retries
        backoff_factor: Backoff factor

    Returns:
        Configured HTTPClient

    Example:
        >>> client = create_http_client(timeout=60)
        >>> response = client.get('https://example.com')
        >>> client.close()

        # Or use as context manager
        >>> with create_http_client() as client:
        ...     response = client.get('https://example.com')
    """
    return HTTPClient(
        timeout=timeout,
        max_retries=max_retries,
        backoff_factor=backoff_factor
    )
