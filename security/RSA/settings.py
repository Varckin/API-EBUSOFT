from pydantic import BaseModel, Field


class Settings(BaseModel):
    ALLOWED_KEY_SIZES: list[int] = Field(
        default_factory=lambda: [2048, 3072, 4096],
        description="Allowed RSA key sizes"
    )


SETTINGS = Settings()
