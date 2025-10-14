from pydantic import BaseModel, Field
from os import getenv

class TranslateSettings(BaseModel):
    TRANSLATE_BASE_URL: str = Field(
        default=getenv('TRNSLT_BASE'),
        description="Base URL for the Translate API"
    )
    timeout: int = Field(
        default=10,
        description="Request timeout in seconds"
    )


CONFIG = TranslateSettings()
