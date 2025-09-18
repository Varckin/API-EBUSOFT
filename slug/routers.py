from fastapi import APIRouter, HTTPException
from slugify import slugify
from slug.models import SlugRequest, SlugResponse


router = APIRouter(prefix="/slug", tags=["slug"])

@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the slug module."""
    return "ok"

@router.post("", response_model=SlugResponse)
async def generate_slug(request: SlugRequest):
    """
    Slug generation from text with multilingual support.
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        result = slugify(
            request.text,
            max_length=request.max_length,
            lowercase=request.lowercase,
            separator=request.separator,
            language_code=request.language,
            allow_unicode=request.allow_unicode
        )
        return SlugResponse(slug=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
