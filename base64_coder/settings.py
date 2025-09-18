from pathlib import Path
from pydantic import BaseModel, Field


class Base64Config(BaseModel):
    temp_dir: Path = Field(
        default=Path("tmp/base64"),
        description="Directory for temporary files"
    )
    max_file_size: int = Field(
        default=50 * 1024 * 1024,
        description="Maximum allowed file size in bytes"
    )


CONFIG = Base64Config()

CONFIG.temp_dir.mkdir(parents=True, exist_ok=True)
