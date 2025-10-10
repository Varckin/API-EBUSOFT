from pydantic import BaseModel, Field
from os import getenv


class Settings(BaseModel):
    FERNET_KEY: str = Field(getenv("FERNET_KEY"), description="FERNET KEY for cryptography")


CONFIG = Settings()
