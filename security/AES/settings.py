from pydantic import BaseModel, Field

class Settings(BaseModel):
    MAX_FILE_SIZE_BYTES: int = Field(
        default=50 * 1024 * 1024,
        description="Maximum file size for upload in bytes"
    )
    AES_KEY_SIZE: int = Field(
        default=32,
        description="AES key size in bytes (256 bits)"
    )
    AES_NONCE_SIZE: int = Field(
        default=12,
        description="Nonce size for AES GCM in bytes (96 bits)"
    )

SETTINGS = Settings()
