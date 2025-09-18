from pydantic import BaseModel, Field
from typing import List


class HashConfig(BaseModel):
    supported_algorithms: List[str] = Field(
        default_factory=lambda: ["md5", "sha1", "sha256", "sha512"],
        description="List of supported hash algorithms"
    )
    default_algorithms: List[str] = Field(
        default_factory=lambda: ["md5", "sha256"],
        description="Default algorithms used if the user does not specify any"
    )
    max_file_size_mb: int = Field(
        default=50,
        description="Maximum size of uploaded file in megabytes"
    )


CONFIG = HashConfig()
