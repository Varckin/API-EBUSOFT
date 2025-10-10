import asyncio
from alembic import command
from alembic.config import Config
from contextlib import suppress
from pathlib import Path
from logger.init_logger import get_logger


logger = get_logger('db_migration')

def get_alembic_config() -> Config:
    """
    Returns an Alembic configuration object pointing to alembic.ini
    and the migrations directory.
    """
    base_dir = Path(__file__).resolve().parent
    alembic_ini = base_dir / "alembic.ini"

    if not alembic_ini.exists():
        logger.error("File alembic.ini not founded!")
        raise FileNotFoundError("File alembic.ini not founded!")

    cfg = Config(str(alembic_ini))
    cfg.set_main_option("script_location", str(base_dir))
    return cfg


async def run_migrations():
    """
    Checks and applies migrations at application startup.
    """
    logger.info("Checking for Alembic migrations...")
    cfg = get_alembic_config()

    loop = asyncio.get_running_loop()
    with suppress(Exception):
        await loop.run_in_executor(None, lambda: command.upgrade(cfg, "head"))
        
    logger.info("Migration verification completed.")
