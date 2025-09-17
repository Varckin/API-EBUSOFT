from fastapi import APIRouter, HTTPException, Depends

from cert.models import CrtShItem, SearchQuery
from cert.service import fetch_crtsh

router = APIRouter(prefix="/cert", tags=["certificates"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the cert module."""
    return "ok"


@router.get("/search", response_model=list[CrtShItem])
async def crtsh_search(query: SearchQuery = Depends()) -> list[CrtShItem]:
    """
    Fetch JSON, normalize and return list of certificates.
    Parameters are taken from query string and validated by SearchQuery model.
    """
    try:
        items = await fetch_crtsh(
            domain=query.domain,
            exact=query.exact,
            include_expired=query.include_expired,
        )
        return items
    except Exception as e:
        # Convert 5xx/network upstream errors and timeouts to 502
        raise HTTPException(status_code=502, detail=f"Upstream error: {e!s}") from e
