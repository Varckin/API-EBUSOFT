from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Token
from core.auth.dependencies import verify_admin_master
from core.auth.database import add_token, delete_token


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the admin module."""
    return "ok"

@router.post("/add-token")
async def add_token_endpoint(role: str,
                             admin=Depends(verify_admin_master),
                             db: AsyncSession = Depends(get_db)):
    """Create a new token with the specified role."""
    token = add_token(db, role)
    return {"token": token.token, "role": token.role, "expires_at": token.expires_at}

@router.delete("/remove-token")
async def remove_token_endpoint(token: str,
                                admin=Depends(verify_admin_master),
                                db: AsyncSession = Depends(get_db)):
    """Delete an existing token by its string value."""
    success = delete_token(db, token)
    if not success:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"msg": f"Token {token} removed"}

@router.get("/list-tokens")
async def list_tokens_endpoint(admin=Depends(verify_admin_master),
                               db: AsyncSession = Depends(get_db)):
    """List all tokens with their ID, role, expiry date, and revoked status."""
    result = await db.execute(select(Token))
    tokens = result.scalars().all()
    
    return [
        {
            "id": t.id,
            "token": t.token,
            "role": t.role,
            "expires_at": t.expires_at,
            "revoked": t.revoked
        }
        for t in tokens
    ]
