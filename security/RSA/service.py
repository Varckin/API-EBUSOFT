from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding, PrivateFormat, PublicFormat, BestAvailableEncryption, NoEncryption
)
import base64


def generate_private_key(key_size: int, public_exponent: int) -> rsa.RSAPrivateKey:
    """
    Generate an RSA private key with given size and public exponent.
    """
    return rsa.generate_private_key(public_exponent=public_exponent, key_size=key_size)

def serialize_private_key(key: rsa.RSAPrivateKey, fmt: str, passphrase: str | None) -> bytes:
    """
    Serialize the private key to PEM format.
    Optionally encrypt with a passphrase.
    """
    private_format = PrivateFormat.PKCS8 if fmt == "pkcs8" else PrivateFormat.TraditionalOpenSSL
    encryption = BestAvailableEncryption(passphrase.encode()) if passphrase else NoEncryption()
    return key.private_bytes(Encoding.PEM, private_format, encryption)

def serialize_public_key(key: rsa.RSAPrivateKey, fmt: str) -> bytes:
    """
    Serialize the public key to PEM format.
    """
    pub = key.public_key()
    public_format = PublicFormat.SubjectPublicKeyInfo if fmt == "spki" else PublicFormat.PKCS1
    return pub.public_bytes(Encoding.PEM, public_format)

def encode_base64(data: bytes) -> str:
    """
    Encode bytes to base64 string.
    """
    return base64.b64encode(data).decode("ascii")
