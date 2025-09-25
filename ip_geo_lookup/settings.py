from pydantic import BaseModel, Field
from os import getenv


class Settings(BaseModel):
    CITY_DB_PATH: str = Field(default_factory=lambda: getenv("CITY_DB_PATH"))
    ASN_DB_PATH: str = Field(default_factory=lambda: getenv("ASN_DB_PATH"))
    COUNTRY_DB_PATH: str = Field(default_factory=lambda: getenv("COUNTRY_DB_PATH"))


SETTINGS = Settings()
