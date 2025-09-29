import logging
import logging.handlers
from logger.settings import CONFIG


def get_logger(name: str = "api_log") -> logging.Logger:
    """
    Logger factory with rotation and optional console output.
    Protection against duplicate handlers when called repeatedly.
    """
    logger = logging.getLogger(name)
    logger.setLevel(CONFIG.level)
    logger.propagate = False

    if not logger.handlers:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=str(CONFIG.log_dir / CONFIG.file_template.format(name=name)),
            maxBytes=CONFIG.max_bytes,
            backupCount=CONFIG.backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(CONFIG.level)
        file_handler.setFormatter(logging.Formatter(CONFIG.fmt, datefmt=CONFIG.datefmt))
        logger.addHandler(file_handler)

        if getattr(CONFIG, "enable_console", False):
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(CONFIG.level)
            stream_handler.setFormatter(logging.Formatter(CONFIG.fmt, datefmt=CONFIG.datefmt))
            logger.addHandler(stream_handler)
    return logger
