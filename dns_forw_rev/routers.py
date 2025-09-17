from fastapi import APIRouter
from dns_forw_rev.models import DNSLookupRequest, DNSLookupResponse
from dns_forw_rev.service import dns_lookup


router = APIRouter(prefix="/dns", tags=["dns"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the dns module."""
    return "ok"

@router.post("", response_model=DNSLookupResponse)
async def dns_lookup_endpoint(request: DNSLookupRequest):
    """
    Perform DNS lookup: reverse if IP is given, forward if domain is given.
    """
    return dns_lookup(ip=str(request.ip) if request.ip else None, domain=request.domain)
