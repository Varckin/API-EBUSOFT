from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional

class UUIDRequest(BaseModel):
    version: Literal["v3", "v4", "v5"] = Field(..., description="UUID type: v3, v4 or v5")
    count: int = Field(1, ge=1, le=100, description="Number of UUIDs to generate")
    text: Optional[str] = Field(None, description="String for UUID v3/v5")

    @model_validator(mode="after")
    def check_text_for_version(cls, model):
        if model.version in ["v3", "v5"] and (not model.text or not model.text.strip()):
            raise ValueError("For v3 and v5 versions, the 'text' field must be specified and non-empty")
        return model
