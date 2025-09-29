from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class LoggerSettings(BaseModel):
    """
    Logger configuration with validation.
    """
    log_dir: Path = Field(
        default=Path("./logs"),
        description="Directory for logs. Will be created automatically.",
    )
    file_template: str = Field(
        default="{name}.log",
        description="Filename template. Supports {name} substitution. "
                    "If path is relative — will be automatically prefixed with log_dir.",
    )
    max_bytes: int = Field(
        default=5 * 1024 * 1024,
        ge=1,
        description="Maximum log file size before rotation (bytes). Default is 5 MB.",
    )
    backup_count: int = Field(
        default=5,
        ge=0,
        description="Number of rotations (how many archive files to keep).",
    )
    fmt: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format.",
    )
    datefmt: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="Date format for asctime (by default without milliseconds).",
    )
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="DEBUG",
        description="Logging level.",
    )
    enable_console: bool = Field(
        default=False,
        description="Additionally log to console (stdout).",
    )

CONFIG = LoggerSettings()
CONFIG.log_dir.mkdir(parents=True, exist_ok=True)
