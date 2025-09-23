from pydantic import BaseModel, Field
from typing import Literal


class PGPKeyRequest(BaseModel):
    name: str = Field(..., description="Owner's name for the key")
    email: str = Field(..., description="Owner's email address for the key")
    key_type: Literal["RSA", "ECC"] = Field(
        "RSA",
        description="Type of key to generate: RSA or ECC"
    )
    key_size: int = Field(
        2048,
        description="RSA key size (2048 or 4096). Ignored for ECC."
    )
    protect_passphrase: str | None = Field(
        None,
        description="Optional passphrase to protect the private key"
    )


class PGPKeyResponse(BaseModel):
    public_key: str
    private_key: str


class PGPEncryptResponse(BaseModel):
    encrypted_data: str
    type: Literal["text", "file"] = Field(
        ...,
        description="Specifies whether the encrypted data is text or file"
    )


class PGPDecryptResponse(BaseModel):
    decrypted_data: str
    type: Literal["text", "file"] = Field(
        ...,
        description="Specifies whether the decrypted data is text or file"
    )
