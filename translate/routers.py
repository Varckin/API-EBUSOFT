from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from translate.service import TranslateService
from translate.models import TranslateRequest, TranslateResponse


router = APIRouter(prefix="/translate", tags=["translate"])
service = TranslateService()


@router.get("", response_model=TranslateResponse)
async def translate_text(
    dl: str = Query(..., description="Destination language code (e.g. 'tr')"),
    text: str = Query(..., description="Text to translate"),
    sl: Optional[str] = Query(None, description="Source language code (optional)")
):
    """
    Translates a given text using the Translate API.
    If source language is omitted, it will be auto-detected.
    """
    try:
        request = TranslateRequest(sl=sl, dl=dl, text=text)
        return await service.translate(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/languages", response_model=dict)
async def get_supported_languages():
    """
    Returns a dictionary of supported languages.
    """
    try:
        return await service.get_languages()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
