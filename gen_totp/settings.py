from pydantic import BaseModel, Field
from os import getenv


class Settings(BaseModel):
    DATABASE_URL: str = Field("sqlite+aiosqlite:///./database.db", description="DataBase URL")
    FERNET_KEY: str = Field(getenv("FERNET_KEY"), description="FERNET KEY for cryptography")


CONFIG = Settings()
