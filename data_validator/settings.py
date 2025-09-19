from pydantic import BaseModel, Field
from typing import Dict, List

class ValidatorConfig(BaseModel):
    max_file_size: int = Field(default=2 * 1024 * 1024, description="Maximum file size in bytes (2 MB)")
    allowed_extensions: Dict[str, List[str]] = Field(
        default_factory=lambda: {
            "json": [".json"],
            "yaml": [".yaml", ".yml"],
            "xml": [".xml"],
            "xsd": [".xsd"]
        },
        description="Allowed file extensions for each format"
    )

CONFIG = ValidatorConfig()
