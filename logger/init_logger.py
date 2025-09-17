import logging
import logging.handlers
from logger.settings import logger_settings


def get_logger(name: str = "api_log") -> logging.Logger:
    """
    Logger factory with rotation and optional console output.
    Protection against duplicate handlers when called repeatedly.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logger_settings.level)
    logger.propagate = False

    if not logger.handlers:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=str(logger_settings.log_dir / logger_settings.file_template.format(name=name)),
            maxBytes=logger_settings.max_bytes,
            backupCount=logger_settings.backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(logger_settings.level)
        file_handler.setFormatter(logging.Formatter(logger_settings.fmt))
        logger.addHandler(file_handler)

        if getattr(logger_settings, "enable_console", False):
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logger_settings.level)
            stream_handler.setFormatter(logging.Formatter(logger_settings.fmt))
            logger.addHandler(stream_handler)
    return logger
