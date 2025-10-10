from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pyotp import TOTP
from logger.init_logger import get_logger
from gen_totp.db_models import TotpTable
from gen_totp.models import (
    TotpCreateResponse,
    TotpGenerateResponse,
    TotpDeleteResponse,
)
from gen_totp.security import encrypt_secret, decrypt_secret


logger = get_logger('totp')

# CRUD func

async def create_totp(session: AsyncSession, service_name: str, secret_key: str) -> TotpCreateResponse:
    """
    Create a new TOTP entry with a service name and secret key.
    Returns the created TOTP record with ID and creation timestamp.
    """
    encrypted_secret = encrypt_secret(secret_key)
    db_obj = TotpTable(
        service_name=service_name,
        secret_key=encrypted_secret,
    )
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)

    logger.info(f"Totp created: {db_obj.id}")

    return TotpCreateResponse(
        id=db_obj.id,
        service_name=db_obj.service_name,
        created_at=db_obj.created_at,
    )


async def get_service(session: AsyncSession, service_id: str) -> TotpTable | None:
    """
    Retrieve a TOTP entry by its ID.
    Returns the TOTP record or None if not found.
    """
    result = await session.execute(
        select(TotpTable).where(TotpTable.id == service_id)
    )
    return result.scalar_one_or_none()


async def delete_service(session: AsyncSession, service_id: str) -> TotpDeleteResponse | None:
    """
    Delete a TOTP entry by ID.
    Returns a deletion status response or None if the TOTP was not found.
    """
    db_obj = await get_service(session, service_id)
    if not db_obj:
        return None
    
    await session.delete(db_obj)
    await session.commit()
    logger.info(f"Totp deleted: {service_id}")

    return TotpDeleteResponse(
        id=service_id,
        status="deleted",
    )


async def generate_totp_code(session: AsyncSession, service_id: str) -> TotpGenerateResponse | None:
    """
    Generate the current TOTP code for a given TOTP ID.
    Updates the last_used_at timestamp and returns the code.
    Returns None if TOTP entry not found.
    """
    db_obj = await get_service(session, service_id)
    if not db_obj:
        return None
    
    db_obj.touch()
    await session.commit()
    await session.refresh(db_obj)

    secret = decrypt_secret(db_obj.secret_key)
    totp = TOTP(secret)
    code = totp.now()

    logger.info(f"Totp generated for: {db_obj.id}")

    return TotpGenerateResponse(
        id=db_obj.id,
        service_name=db_obj.service_name,
        code=code,
    )
