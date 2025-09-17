from pydantic import BaseModel, Field
from traceroute.settings import SETTINGS

class TraceRequest(BaseModel):
    host: str = Field(..., description="Target hostname or IP address")
    max_hops: int = Field(SETTINGS.DEFAULT_MAX_HOPS, description="Maximum number of hops to trace")


class TraceResponse(BaseModel):
    hops: list[str] = Field(..., description="List of IP addresses for each hop")
