from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional

class UUIDRequest(BaseModel):
    version: Literal["v3", "v4", "v5"] = Field(..., description="UUID type: v3, v4 or v5")
    count: int = Field(1, ge=1, le=100, description="Number of UUIDs to generate")
    text: Optional[str] = Field(None, description="String for UUID v3/v5")

    @field_validator("text")
    def validate_text(cls, v, values):
        if values["version"] in ["v3", "v5"] and not v:
            raise ValueError("For v3 and v5 versions, the 'text' field must be specified")
        return v
