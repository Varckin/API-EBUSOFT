from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from logger.init_logger import get_logger
from pathlib import Path


logger = get_logger('base_config')

DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"
Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """Provide a database session for dependency injection."""
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """Initialize database tables if not present (checks SQLite file)."""
    if DATABASE_URL.startswith("sqlite"):
        db_path = DATABASE_URL.replace("sqlite+aiosqlite:///", "")
        if Path(db_path).exists():
            logger.info(f"Database {db_path} exists. Skiping initialization")
            return

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initilized.")
