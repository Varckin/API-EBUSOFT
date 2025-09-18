from pydantic import BaseModel, Field, field_validator


class IDRequest(BaseModel):
    type: str = Field(..., description="ID type: 'shortid' or 'nanoid'")
    length: int = Field(8, gt=0, le=64, description="ID length")
    alphabet: str | None = Field(None, description="Custom alphabet for generation (optional)")

    @field_validator("type")
    @classmethod
    def check_type(cls, v: str) -> str:
        v_lower = v.lower()
        if v_lower not in {"shortid", "nanoid"}:
            raise ValueError("type must be 'shortid' or 'nanoid'")
        return v_lower


class IDResponse(BaseModel):
    id: str
