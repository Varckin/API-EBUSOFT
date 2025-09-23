from pydantic import BaseModel, Field


class Settings(BaseModel):
    MAX_FILE_SIZE: int = Field(
        50 * 1024 * 1024,
        description="Maximum allowed file size in bytes (default: 50 MB)"
    )


SETTINGS = Settings()
