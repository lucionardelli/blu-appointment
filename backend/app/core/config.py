from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # This key is used for encrypting/decrypting sensitive data like medical history.
    # It MUST be a 32-byte URL-safe base64-encoded string.
    # You can generate one with: `from cryptography.fernet import Fernet; Fernet.generate_key().decode()`
    FERNET_KEY: str = "your_super_secret_key_for_encryption"  # Default for dev, should be overridden by env var

    # This key is for signing JWTs
    SECRET_KEY: str = "your_super_secret_key_for_jwt"

    DATABASE_NAME: str = "blu.db"
    DATABASE_URL: str = f"sqlite:///db/{DATABASE_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
