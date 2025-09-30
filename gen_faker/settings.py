from pydantic import BaseModel

class FakerSettings(BaseModel):
    default_locale: str = "en_US"
    max_bulk: int = 1000


CONFIG = FakerSettings()
