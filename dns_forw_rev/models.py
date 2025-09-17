from pydantic import BaseModel, IPvAnyAddress
from typing import Optional, List


class DNSLookupRequest(BaseModel):
    ip: Optional[IPvAnyAddress] = None
    domain: Optional[str] = None


class DNSLookupResponse(BaseModel):
    ip: Optional[str] = None
    domain: Optional[str] = None
    ips: Optional[List[str]] = None
