import pgpy
from fastapi import UploadFile, HTTPException
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm
from security.PGP.models import PGPKeyRequest
from security.PGP.settings import SETTINGS


def generate_pgp_key(request: PGPKeyRequest) -> tuple[str, str]:
    """
    Generate a new PGP keypair based on the request configuration.
    Returns (public_key, private_key) in ASCII-armored format.
    """
    if request.key_type == "RSA":
        if request.key_size not in (2048, 4096):
            raise ValueError("RSA key size must be either 2048 or 4096")
        key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, request.key_size)
    elif request.key_type == "ECC":
        # Example: Curve25519
        key = pgpy.PGPKey.new(PubKeyAlgorithm.ECDSA, 0)
    else:
        raise ValueError("Invalid key type. Use RSA or ECC.")

    uid = pgpy.PGPUID.new(request.name, email=request.email)

    key.add_uid(
        uid,
        usage={KeyFlags.Sign, KeyFlags.EncryptCommunications},
        hashes=[HashAlgorithm.SHA256],
        ciphers=[SymmetricKeyAlgorithm.AES256],
        compression=[CompressionAlgorithm.ZLIB],
    )

    private_key_str = str(key)
    if request.protect_passphrase:
        key.protect(request.protect_passphrase, SymmetricKeyAlgorithm.AES256, HashAlgorithm.SHA256)
        private_key_str = str(key)

    return str(key.pubkey), private_key_str

def encrypt_message(message: str, public_key_str: str) -> str:
    """
    Encrypt a text message using the provided public PGP key.
    """
    pub_key, _ = pgpy.PGPKey.from_blob(public_key_str)
    msg = pgpy.PGPMessage.new(message)
    encrypted_message = pub_key.encrypt(msg)
    return str(encrypted_message)

def decrypt_message(encrypted_text: str, private_key_str: str, passphrase: str | None = None) -> str:
    """
    Decrypt a text message using the provided private PGP key.
    """
    priv_key, _ = pgpy.PGPKey.from_blob(private_key_str)
    if passphrase:
        priv_key.unlock(passphrase)
    encrypted_message = pgpy.PGPMessage.from_blob(encrypted_text)
    decrypted_message = priv_key.decrypt(encrypted_message).message
    return decrypted_message

def encrypt_file(file: UploadFile, public_key_str: str) -> str:
    """
    Encrypt a file using the provided public PGP key.
    Validates file size against MAX_FILE_SIZE from settings.
    Returns an ASCII-armored PGP message.
    """
    file.file.seek(0, 2)  # move pointer to end
    file_size = file.file.tell()
    file.file.seek(0)  # reset pointer

    if file_size > SETTINGS.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum allowed size is {SETTINGS.MAX_FILE_SIZE} bytes"
        )

    pub_key, _ = pgpy.PGPKey.from_blob(public_key_str)
    content = file.file.read()
    message = pgpy.PGPMessage.new(content, file=True)  # file=True for binary data
    encrypted_message = pub_key.encrypt(message)
    return str(encrypted_message)

def decrypt_file(encrypted_file_str: str, private_key_str: str, passphrase: str | None = None) -> bytes:
    """
    Decrypt a previously encrypted file using the provided private PGP key.
    Returns the raw file content in bytes.
    """
    priv_key, _ = pgpy.PGPKey.from_blob(private_key_str)
    if passphrase:
        priv_key.unlock(passphrase)
    encrypted_message = pgpy.PGPMessage.from_blob(encrypted_file_str)
    decrypted = priv_key.decrypt(encrypted_message)
    return decrypted.message
