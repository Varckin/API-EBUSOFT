from pydantic import BaseModel
from os import getenv


class ClamAVSettings(BaseModel):
    clamav_host: str = getenv('CLAMAV_HOST','127.0.0.1')
    clamav_port: int = int(getenv('CLAMAV_PORT','3310'))
    max_file_size_mb: int = 50


CONFIG = ClamAVSettings()
