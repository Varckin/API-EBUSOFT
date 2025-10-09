from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from core.auth.settings import CONFIG
from pathlib import Path
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.auth.models import Token
import secrets
from logger.init_logger import get_logger
from core.base.base import Base


logger = get_logger('auth_db')

engine = create_async_engine(CONFIG.DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """Provide a database session for dependency injection."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    """Initialize database tables if not present (checks SQLite file)."""
    if CONFIG.DATABASE_URL.startswith("sqlite"):
        db_path = CONFIG.DATABASE_URL.replace("sqlite+aiosqlite:///", "")
        if Path(db_path).exists():
            logger.info(f"Database {db_path} exists. Skiping initialization")
            return

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initilized.")


# Token func

async def add_token(db: AsyncSession, role: str, ttl_minutes: int = CONFIG.TOKEN_TTL_MINUTES) -> Token:
    """Create and store a new token with a given role and TTL."""
    token_str = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)

    token = Token(
        token=token_str,
        role=role,
        expires_at=expires_at,
        revoked=False,
    )

    db.add(token)
    await db.commit()
    await db.refresh(token)

    logger.info(f"Token create: token - {token.token}, role - {token.role}, expires - {token.expires_at}, revoked - {token.revoked}")
    return token


async def get_valid_token(db: AsyncSession, token_str: str) -> Token | None:
    """Return a valid (not revoked, not expired) token by its string value."""
    stmt = select(Token).where(Token.token == token_str, Token.revoked == False)
    result = await db.execute(stmt)
    token = result.scalar_one_or_none()

    if token and token.expires_at > datetime.now(timezone.utc):
        return token
    return None


async def revoke_token(db: AsyncSession, token: Token):
    """Mark a token as revoked."""
    token.revoked = True
    logger.info(f"Token revoked: token - {token.token}, role - {token.role}, expires - {token.expires_at}, revoked - {token.revoked}")
    await db.commit()


async def delete_token(db: AsyncSession, token_str: str) -> bool:
    """Delete a token by its string value. Returns True if deleted."""
    stmt = select(Token).where(Token.token == token_str)
    result = await db.execute(stmt)
    token = result.scalar_one_or_none()

    if not token:
        logger.info(f"Token {token_str} not found")
        return False
    
    await db.delete(token)
    await db.commit()
    logger.info(f"Token delete: token - {token.token}, role - {token.role}, expires - {token.expires_at}, revoked - {token.revoked}")
    return True


async def update_token_role(db: AsyncSession, token_str: str, new_role: str) -> bool:
    """Update the role of a token by its string value. Returns True if updated."""
    stmt = select(Token).where(Token.token == token_str)
    result = await db.execute(stmt)
    token = result.scalar_one_or_none()

    if not token:
        logger.info(f"Token {token_str} not found")
        return False
    
    token.role = new_role
    await db.commit()
    logger.info(f"Token role update: token - {token.token}, role - {token.role}, expires - {token.expires_at}, revoked - {token.revoked}")
    return True


async def refresh_token(db: AsyncSession, old_token_str: str) -> Token | None:
    """Revoke the old token and create a new one with the same role. Returns the new token."""
    token = await get_valid_token(db, old_token_str)
    if not token:
        return None

    role = token.role
    await revoke_token(db, token)
    new_token = await add_token(db, role)
    logger.info(f"Token refresh: token - {new_token.token}, role - {new_token.role}, expires - {new_token.expires_at}, revoked - {new_token.revoked}")
    return new_token
