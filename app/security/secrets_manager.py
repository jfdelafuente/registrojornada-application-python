"""Secure secrets management with encryption."""

import logging
import os
from typing import Optional

from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


class SecretsManager:
    """
    Manages encrypted credentials and secrets.

    Provides secure storage and retrieval of sensitive information using
    Fernet symmetric encryption.

    Usage:
        secrets = SecretsManager()
        password = secrets.get_secret('HR_PASSWORD_ENCRYPTED')
    """

    def __init__(self):
        """Initialize secrets manager with encryption key."""
        encryption_key = os.getenv("ENCRYPTION_KEY")
        if not encryption_key:
            raise ValueError(
                "ENCRYPTION_KEY not found in environment variables. "
                "Please run scripts/encrypt_secrets.py to generate one."
            )

        try:
            self.cipher = Fernet(encryption_key.encode())
            logger.info("SecretsManager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SecretsManager: {e}")
            raise ValueError(f"Invalid ENCRYPTION_KEY: {e}")

    def get_secret(self, key: str) -> str:
        """
        Retrieve and decrypt a secret.

        Args:
            key: Environment variable name containing encrypted value

        Returns:
            Decrypted secret value

        Raises:
            ValueError: If secret not found or decryption fails
        """
        encrypted_value = os.getenv(key)
        if not encrypted_value:
            raise ValueError(
                f"Secret '{key}' not found in environment variables. "
                f"Please ensure .env file contains {key}."
            )

        try:
            decrypted = self.cipher.decrypt(encrypted_value.encode()).decode()
            logger.debug(f"Successfully decrypted secret: {key}")
            return decrypted
        except Exception as e:
            logger.error(f"Failed to decrypt '{key}': {e}")
            raise ValueError(f"Error decrypting '{key}': {str(e)}")

    @staticmethod
    def encrypt_secret(plain_text: str, key: str) -> str:
        """
        Encrypt a secret value.

        This is a utility method for initial secret encryption.
        Use scripts/encrypt_secrets.py for interactive encryption.

        Args:
            plain_text: The value to encrypt
            key: Encryption key (Fernet key)

        Returns:
            Encrypted value as string
        """
        cipher = Fernet(key.encode())
        return cipher.encrypt(plain_text.encode()).decode()

    @staticmethod
    def generate_key() -> str:
        """
        Generate a new Fernet encryption key.

        Returns:
            New encryption key as string
        """
        return Fernet.generate_key().decode()
