from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from core.auth.database import refresh_token


router = APIRouter(prefix="/token", tags=["token"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the token module."""
    return "ok"

@router.post("/refresh")
async def refresh_token_endpoint(old_token: str, db: AsyncSession = Depends(get_db)):
    """Refresh an existing valid token."""
    new_token = await refresh_token(db, old_token)
    if not new_token:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {
        "token": new_token.token,
        "role": new_token.role,
        "expires_at": new_token.expires_at,
        "revoked": new_token.revoked
    }
