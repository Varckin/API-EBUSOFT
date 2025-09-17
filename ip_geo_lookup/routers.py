from fastapi import APIRouter, HTTPException
from ip_geo_lookup.models import IPRequest, IPResponse
from ip_geo_lookup.service import IPGeoService

router = APIRouter(prefix="/ip_lookup", tags=["ip_lookup"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the ip_lookup module."""
    return "ok"

@router.post("", response_model=IPResponse)
async def ip_lookup(request: IPRequest):
    """
    Lookup IP address information (country, region, city, ASN, provider).
    """
    try:
        geo_service = IPGeoService()
        return geo_service.lookup(request.ip)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
