from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
from security.AES.settings import SETTINGS


def generate_key() -> str:
    """Generate a random AES key in Base64"""
    key = os.urandom(SETTINGS.AES_KEY_SIZE)
    return base64.b64encode(key).decode()

def encrypt_aes(plaintext: bytes, key_b64: str) -> dict:
    """Encrypt data using AES-GCM"""
    key = base64.b64decode(key_b64)
    nonce = os.urandom(SETTINGS.AES_NONCE_SIZE)

    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce),
        backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "tag": base64.b64encode(encryptor.tag).decode()
    }

def decrypt_aes(ciphertext_b64: str, key_b64: str, nonce_b64: str, tag_b64: str) -> bytes:
    """Decrypt data using AES-GCM"""
    key = base64.b64decode(key_b64)
    nonce = base64.b64decode(nonce_b64)
    tag = base64.b64decode(tag_b64)
    ciphertext = base64.b64decode(ciphertext_b64)

    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(nonce, tag),
        backend=default_backend()
    ).decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext
