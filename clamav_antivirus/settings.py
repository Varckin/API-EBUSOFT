from pydantic import BaseModel, Field
from os import getenv


class ClamAVSettings(BaseModel):
    clamav_host: str = Field(default_factory=lambda: getenv('CLAMAV_HOST', '127.0.0.1'))
    clamav_port: int = Field(default_factory=lambda: int(getenv('CLAMAV_PORT', '3310')))
    max_file_size_mb: int = 50


CONFIG = ClamAVSettings()
