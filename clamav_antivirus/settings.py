from pydantic import BaseModel
from os import getenv


class ClamAVSettings(BaseModel):
    clamav_host: str = getenv('CLAMAV_HOST')
    clamav_port: int = int(getenv('CLAMAV_PORT'))
    max_file_size_mb: int = 50


CONFIG = ClamAVSettings()
