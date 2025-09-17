from pydantic import BaseModel
from typing import Optional


class IPRequest(BaseModel):
    ip: str


class IPResponse(BaseModel):
    ip: str
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    asn: Optional[str] = None
    provider: Optional[str] = None
