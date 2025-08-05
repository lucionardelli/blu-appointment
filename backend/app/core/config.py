from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # This key is used for encrypting/decrypting sensitive data like medical history.
    # It MUST be a 32-byte URL-safe base64-encoded string.
    # You can generate one with: `from cryptography.fernet import Fernet; Fernet.generate_key().decode()`
    FERNET_KEY: Final[str] = "N3mB8BZBCH0ROIT7PUy4d7dG50ED5N1Wse0t5WgB88g="

    # This key is for signing JWTs
    SECRET_KEY: Final[str] = "your_super_secret_key_for_jwt"  # noqa: S105

    DATABASE_NAME: Final[str] = "blu.db"
    DATABASE_URL: Final[str] = f"sqlite:///db/{DATABASE_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
