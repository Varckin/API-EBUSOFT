from fastapi import APIRouter
from id_generator.models import IDRequest, IDResponse
from id_generator.service import generate_identifier


router = APIRouter(prefix="/idgen", tags=["idgen"])

@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the idgen module."""
    return "ok"

@router.post("", response_model=IDResponse)
async def generate_id(request: IDRequest):
    """
    Generate a ShortID or NanoID.  
    """
    sid = generate_identifier(request.type, request.length, request.alphabet)
    return IDResponse(id=sid)
