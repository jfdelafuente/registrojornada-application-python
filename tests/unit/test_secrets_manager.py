"""Unit tests for app.security.secrets_manager module."""

import pytest
from cryptography.fernet import Fernet
from unittest.mock import patch

from app.security.secrets_manager import SecretsManager


@pytest.mark.unit
class TestSecretsManager:
    """Test SecretsManager functionality."""

    @pytest.fixture
    def encryption_key(self):
        """Generate a test encryption key."""
        return Fernet.generate_key().decode()

    @pytest.fixture
    def encrypted_secret(self, encryption_key):
        """Create an encrypted test secret."""
        cipher = Fernet(encryption_key.encode())
        plain_text = "test_password_123"
        return cipher.encrypt(plain_text.encode()).decode()

    def test_initialization_with_valid_key(self, encryption_key, monkeypatch):
        """Test SecretsManager initializes with valid encryption key."""
        monkeypatch.setenv("ENCRYPTION_KEY", encryption_key)

        manager = SecretsManager()

        assert manager.cipher is not None

    def test_initialization_without_key_raises_error(self, monkeypatch):
        """Test SecretsManager raises error without encryption key."""
        monkeypatch.delenv("ENCRYPTION_KEY", raising=False)

        with pytest.raises(ValueError) as exc_info:
            SecretsManager()

        assert "ENCRYPTION_KEY not found" in str(exc_info.value)

    def test_initialization_with_invalid_key_raises_error(self, monkeypatch):
        """Test SecretsManager raises error with invalid encryption key."""
        monkeypatch.setenv("ENCRYPTION_KEY", "invalid_key")

        with pytest.raises(ValueError) as exc_info:
            SecretsManager()

        assert "Invalid ENCRYPTION_KEY" in str(exc_info.value)

    def test_get_secret_success(self, encryption_key, encrypted_secret, monkeypatch):
        """Test successfully retrieving and decrypting a secret."""
        monkeypatch.setenv("ENCRYPTION_KEY", encryption_key)
        monkeypatch.setenv("TEST_SECRET", encrypted_secret)

        manager = SecretsManager()
        decrypted = manager.get_secret("TEST_SECRET")

        assert decrypted == "test_password_123"

    def test_get_secret_not_found(self, encryption_key, monkeypatch):
        """Test get_secret raises error when secret not found."""
        monkeypatch.setenv("ENCRYPTION_KEY", encryption_key)
        monkeypatch.delenv("MISSING_SECRET", raising=False)

        manager = SecretsManager()

        with pytest.raises(ValueError) as exc_info:
            manager.get_secret("MISSING_SECRET")

        assert "Secret 'MISSING_SECRET' not found" in str(exc_info.value)

    def test_get_secret_decryption_fails(self, encryption_key, monkeypatch):
        """Test get_secret raises error when decryption fails."""
        monkeypatch.setenv("ENCRYPTION_KEY", encryption_key)
        monkeypatch.setenv("BAD_SECRET", "not_encrypted_value")

        manager = SecretsManager()

        with pytest.raises(ValueError) as exc_info:
            manager.get_secret("BAD_SECRET")

        assert "Error decrypting 'BAD_SECRET'" in str(exc_info.value)

    def test_encrypt_secret_static_method(self, encryption_key):
        """Test static encrypt_secret method."""
        plain_text = "my_secret_password"

        encrypted = SecretsManager.encrypt_secret(plain_text, encryption_key)

        assert encrypted != plain_text
        assert isinstance(encrypted, str)

        # Verify can decrypt
        cipher = Fernet(encryption_key.encode())
        decrypted = cipher.decrypt(encrypted.encode()).decode()
        assert decrypted == plain_text

    def test_generate_key_static_method(self):
        """Test static generate_key method."""
        key1 = SecretsManager.generate_key()
        key2 = SecretsManager.generate_key()

        assert key1 != key2
        assert isinstance(key1, str)
        assert isinstance(key2, str)

        # Verify keys are valid Fernet keys
        Fernet(key1.encode())
        Fernet(key2.encode())

    def test_encrypt_decrypt_round_trip(self):
        """Test encrypting and decrypting a secret."""
        key = SecretsManager.generate_key()
        plain_text = "super_secret_value"

        # Encrypt
        encrypted = SecretsManager.encrypt_secret(plain_text, key)

        # Decrypt using SecretsManager
        with patch.dict("os.environ", {"ENCRYPTION_KEY": key, "MY_SECRET": encrypted}):
            manager = SecretsManager()
            decrypted = manager.get_secret("MY_SECRET")

        assert decrypted == plain_text

    def test_different_keys_cannot_decrypt(self):
        """Test that secrets encrypted with one key cannot be decrypted with another."""
        key1 = SecretsManager.generate_key()
        key2 = SecretsManager.generate_key()
        plain_text = "secret"

        encrypted = SecretsManager.encrypt_secret(plain_text, key1)

        # Try to decrypt with different key
        with patch.dict("os.environ", {"ENCRYPTION_KEY": key2, "SECRET": encrypted}):
            manager = SecretsManager()
            with pytest.raises(ValueError):
                manager.get_secret("SECRET")

    def test_multiple_secrets(self, encryption_key, monkeypatch):
        """Test retrieving multiple different secrets."""
        cipher = Fernet(encryption_key.encode())

        secret1 = cipher.encrypt(b"password1").decode()
        secret2 = cipher.encrypt(b"password2").decode()
        secret3 = cipher.encrypt(b"password3").decode()

        monkeypatch.setenv("ENCRYPTION_KEY", encryption_key)
        monkeypatch.setenv("SECRET1", secret1)
        monkeypatch.setenv("SECRET2", secret2)
        monkeypatch.setenv("SECRET3", secret3)

        manager = SecretsManager()

        assert manager.get_secret("SECRET1") == "password1"
        assert manager.get_secret("SECRET2") == "password2"
        assert manager.get_secret("SECRET3") == "password3"

    def test_unicode_secret(self, encryption_key, monkeypatch):
        """Test encrypting and decrypting unicode strings."""
        cipher = Fernet(encryption_key.encode())
        plain_text = "contraseña_española_123"
        encrypted = cipher.encrypt(plain_text.encode()).decode()

        monkeypatch.setenv("ENCRYPTION_KEY", encryption_key)
        monkeypatch.setenv("UNICODE_SECRET", encrypted)

        manager = SecretsManager()
        decrypted = manager.get_secret("UNICODE_SECRET")

        assert decrypted == plain_text

    def test_empty_secret(self, encryption_key, monkeypatch):
        """Test encrypting and decrypting empty string."""
        cipher = Fernet(encryption_key.encode())
        plain_text = ""
        encrypted = cipher.encrypt(plain_text.encode()).decode()

        monkeypatch.setenv("ENCRYPTION_KEY", encryption_key)
        monkeypatch.setenv("EMPTY_SECRET", encrypted)

        manager = SecretsManager()
        decrypted = manager.get_secret("EMPTY_SECRET")

        assert decrypted == ""

    def test_long_secret(self, encryption_key, monkeypatch):
        """Test encrypting and decrypting long strings."""
        cipher = Fernet(encryption_key.encode())
        plain_text = "x" * 10000  # 10KB string
        encrypted = cipher.encrypt(plain_text.encode()).decode()

        monkeypatch.setenv("ENCRYPTION_KEY", encryption_key)
        monkeypatch.setenv("LONG_SECRET", encrypted)

        manager = SecretsManager()
        decrypted = manager.get_secret("LONG_SECRET")

        assert decrypted == plain_text
        assert len(decrypted) == 10000
