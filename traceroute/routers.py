from fastapi import APIRouter, HTTPException
from traceroute.models import TraceRequest, TraceResponse
from traceroute.service import traceroute_subprocess

router = APIRouter(prefix="/traceroute", tags=["traceroute"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the traceroute module."""
    return "ok"

@router.post("", response_model=TraceResponse)
async def traceroute_endpoint(request: TraceRequest):
    """
    Endpoint to trace the network path to a specified host,
    showing each hop's IP or '*' if unreachable.
    """
    try:
        hops = traceroute_subprocess(request.host, request.max_hops)
        return TraceResponse(hops=hops)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
