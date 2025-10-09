from pydantic import BaseModel, Field
from os import getenv


class WeatherSettings(BaseModel):
    wtr_base_url: str = Field(getenv("WTR_BASE"), description="Base URL")
    default_lang: str = Field("en", description="Default response language (ru/en/etc.)")
    default_format: str = Field("j2", description="Default response format (j1/j2 — JSON)")
    redis_broker_url: str = Field(getenv("REDIS_BROKER_URL"), description="Redis broker URL for storage")
    cache_ttl: int = Field(3600, description="TTL for weather cache in seconds")


CONFIG = WeatherSettings()
