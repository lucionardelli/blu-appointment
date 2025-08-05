from cryptography.fernet import Fernet

from .config import settings

branca = Fernet(settings.FERNET_KEY.encode())


def encrypt(data: str) -> str:
    if not data:
        return ""
    return branca.encrypt(data.encode()).decode()


def decrypt(encrypted_data: str) -> str:
    if not encrypted_data:
        return ""
    return branca.decrypt(encrypted_data.encode()).decode()
