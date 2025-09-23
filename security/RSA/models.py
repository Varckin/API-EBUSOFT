from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
from security.RSA.settings import SETTINGS


class RSAKeyRequest(BaseModel):
    key_size: int = Field(2048, description="Key size in bits: 2048, 3072, or 4096")
    public_exponent: int = Field(65537, description="Public exponent, usually 65537")
    encrypt_private: bool = Field(False, description="Encrypt private key with a passphrase")
    passphrase: Optional[str] = Field(None, description="Passphrase for encrypting the private key")
    private_format: Literal["pkcs8", "traditional"] = Field("pkcs8", description="Private key format")
    public_format: Literal["spki", "pkcs1"] = Field("spki", description="Public key format")
    output_base64: bool = Field(False, description="Return keys in base64 instead of PEM")
    output_type: Literal["json", "download"] = Field("json", description="Return format: JSON or download file")

    @field_validator("key_size")
    def validate_key_size(cls, v):
        if v not in SETTINGS.ALLOWED_KEY_SIZES:
            raise ValueError(f"key_size must be one of: {SETTINGS.ALLOWED_KEY_SIZES}")
        return v

    @field_validator("passphrase", mode="before")
    def validate_passphrase(cls, v, info):
        if info.data.get("encrypt_private") and not v:
            raise ValueError("passphrase is required if encrypt_private is True")
        return v


class RSAKeyResponse(BaseModel):
    private_key: str = Field(..., description="Private key in PEM or base64")
    public_key: str = Field(..., description="Public key in PEM or base64")
    key_size: int
    public_exponent: int
