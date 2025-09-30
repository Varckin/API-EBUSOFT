from cryptography.fernet import Fernet
from gen_totp.settings import CONFIG
from logger.init_logger import get_logger

logger = get_logger("totp_security")

if not CONFIG.FERNET_KEY:
    logger.info(f"FERNET_KEY is not set! Add it to environment variables.")
    raise RuntimeError("FERNET_KEY is not set! Add it to environment variables.")

try:
    fernet = Fernet(CONFIG.FERNET_KEY)
except ValueError:
    logger.info(f"FERNET_KEY is invalid! Must be a 32-byte URL-safe base64-encoded key.")
    raise RuntimeError("FERNET_KEY is invalid! Must be a 32-byte URL-safe base64-encoded key.")

def encrypt_secret(secret: str) -> str:
    return fernet.encrypt(secret.encode()).decode()

def decrypt_secret(encrypted_secret: str) -> str:
    return fernet.decrypt(encrypted_secret.encode()).decode()
