from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from gen_totp.database import get_db
from gen_totp.database import (
    create_totp, generate_totp_code,
    delete_service
)
from gen_totp.models import (
    TotpCreateRequest,
    TotpCreateResponse,
    TotpGenerateRequest,
    TotpGenerateResponse,
    TotpDeleteRequest,
    TotpDeleteResponse,
)

router = APIRouter(prefix="/totp", tags=["TOTP"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the totp module."""
    return "ok"

@router.post("/create", response_model=TotpCreateResponse)
async def create_totp_endpoint(data: TotpCreateRequest, db: AsyncSession = Depends(get_db)):
    """
    Create a new TOTP entry with service name and secret key.
    Returns the created record with ID and creation timestamp.
    """
    result = await create_totp(
        db,
        data.service_name,
        data.secret_key
    )
    return result


@router.post("/generate", response_model=TotpGenerateResponse)
async def generate_totp_endpoint(data: TotpGenerateRequest, db: AsyncSession = Depends(get_db)):
    """
    Generate a TOTP code for the given TOTP ID.
    Returns the current TOTP code or 404 if not found.
    """
    result = await generate_totp_code(
        db,
        data.id
    )
    if not result:
        raise HTTPException(status_code=404, detail="TOTP not found")
    return result


@router.delete("/delete", response_model=TotpDeleteResponse)
async def delete_totp_endpoint(data: TotpDeleteRequest, db: AsyncSession = Depends(get_db)):
    """
    Delete a TOTP entry by ID.
    Returns deletion status or 404 if TOTP not found.
    """
    result = await delete_service(
        db,
        data.id
    )
    if not result:
        raise HTTPException(status_code=404, detail="TOTP not found")
    return result
