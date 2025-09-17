from pydantic import BaseModel


class TracerouteSettings(BaseModel):
    DEFAULT_MAX_HOPS: int = 30
    DEFAULT_TIMEOUT: float = 300.0


SETTINGS = TracerouteSettings()
