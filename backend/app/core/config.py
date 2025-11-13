import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory for the backend application
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(APP_DIR)

class Settings(BaseSettings):
    # Security keys. These MUST be set in the environment for production.
    # You can generate them with:
    # FERNET_KEY: from cryptography.fernet import Fernet; Fernet.generate_key().decode()
    # SECRET_KEY: openssl rand -hex 32
    FERNET_KEY: str
    SECRET_KEY: str

    # Database URL.
    # Defaults to a local SQLite database in the .app//db/ directory.
    DATABASE_URL: str = f"sqlite:///{os.path.join(APP_DIR, 'db', 'blu.sqlite3')}"

    ENV: str = "production"

    # Cookie domain for security (e.g., ".bluroom.com.ar" to include subdomains or "bluroom.com.ar" for exact domain)
    # Set to None for development (allows localhost)
    COOKIE_DOMAIN: str | None = None

    # Pydantic settings configuration
    # It will load variables from a .env file and the system environment.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
