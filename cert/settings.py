from pydantic import BaseModel, AnyHttpUrl
from os import getenv


class CertSettings(BaseModel):
    crt_base: AnyHttpUrl = getenv('CRT_BASE')

    # Network settings
    connect_timeout_s: float = 5.0
    read_timeout_s: float = 20.0
    write_timeout_s: float = 10.0
    pool_timeout_s: float = 5.0

    max_keepalive_connections: int = 10
    max_connections: int = 20
    retries: int = 3
    initial_backoff_s: float = 0.5
    user_agent: str = "CertificateLookupService/1.0"

    max_records: int = 10000
    split_names: bool = True


settings = CertSettings()
