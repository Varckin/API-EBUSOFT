import asyncio
from alembic import command
from alembic.config import Config
from pathlib import Path
from logger.init_logger import get_logger

from core.auth.models import Token
from gen_totp.db_models import TotpTable


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
    cfg.set_main_option("version_locations", str(base_dir / "versions"))
    cfg.set_main_option("prepend_sys_path", ".")

    return cfg


async def run_migrations():
    """
    Checks and applies migrations at application startup.
    """
    logger.info("Checking for Alembic migrations...")

    try:
        cfg = get_alembic_config()
        loop = asyncio.get_running_loop()

        def _run_migrations():
            try:
                logger.info("Creating an auto-generated migration...")
                command.revision(cfg, message="auto migration", autogenerate=True)
            except Exception as e:
                logger.warning(f"Auto-generation of migration failed: {e}")
            
            logger.info("Applying migrations...")
            command.upgrade(cfg, "head")
            logger.info("Migrations applied successfully")
        
        await loop.run_in_executor(None, _run_migrations)
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise
