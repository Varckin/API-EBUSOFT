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


@router.post("/create", response_model=TotpCreateResponse)
async def create_totp_endpoint(data: TotpCreateRequest, db: AsyncSession = Depends(get_db)):
    result = await create_totp(
        db,
        data.service_name,
        data.secret_key
    )
    return result


@router.post("/generate", response_model=TotpGenerateResponse)
async def generate_totp_endpoint(data: TotpGenerateRequest, db: AsyncSession = Depends(get_db)):
    result = await generate_totp_code(
        db,
        data.id
    )
    if not result:
        raise HTTPException(status_code=404, detail="TOTP not found")
    return result


@router.delete("/delete", response_model=TotpDeleteResponse)
async def delete_totp_endpoint(data: TotpDeleteRequest, db: AsyncSession = Depends(get_db)):
    result = await delete_service(
        db,
        data.id
    )
    if not result:
        raise HTTPException(status_code=404, detail="TOTP not found")
    return result
