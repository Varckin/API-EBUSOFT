from datetime import datetime, timedelta, timezone
from base64_coder.settings import CONFIG
from celery_conf import celery_app
from logger.init_logger import get_logger


logger = get_logger('base64_celery')

@celery_app.task
def clean_temp_files():
    """
    Deletes all files in TEMP_DIR older than 1 day.
    """
    now = datetime.now(timezone.utc)
    for file_path in CONFIG.temp_dir.iterdir():
        if file_path.is_file():
            modified_time = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
            if now - modified_time > timedelta(days=1):
                try:
                    file_path.unlink()
                    logger.info(f"Deleted old temp file: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to delete file {file_path}: {e}")
