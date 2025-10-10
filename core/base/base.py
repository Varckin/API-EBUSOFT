from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"
Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """Provide a database session for dependency injection."""
    async with AsyncSessionLocal() as session:
        yield session
