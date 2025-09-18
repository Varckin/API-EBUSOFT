from fastapi import APIRouter, HTTPException
from urllib.parse import quote, unquote

from url_codec.models import (URLDecodeRequest, URLDecodeResponse,
                              URLEncodeRequest, URLEncodeResponse)


router = APIRouter(prefix="/urlcodec", tags=["urlcodec"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the urlcodec module."""
    return "ok"

@router.post("/encode", response_model=URLEncodeResponse)
async def encode_url(request: URLEncodeRequest):
    """
    Encodes a string into URL format.
    """
    try:
        encoded = quote(request.text, safe=request.safe)
        return URLEncodeResponse(encoded=encoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/decode", response_model=URLDecodeResponse)
async def decode_url(request: URLDecodeRequest):
    """
    Decodes a string from URL format.
    """
    try:
        decoded = unquote(request.text)
        return URLDecodeResponse(decoded=decoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
