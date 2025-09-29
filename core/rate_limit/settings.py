from pydantic import BaseModel, Field
from os import getenv

class RateLimitSettings(BaseModel):
    max_requests: int = Field(100, description="Maximum number of requests per minute per IP")
    period_seconds: int = Field(60, description="Time period in seconds for the rate limit")
    redis_broker_url: str = Field(getenv("REDIS_BROKER_URL"), description="Redis broker URL for storage")


CONFIG = RateLimitSettings()
