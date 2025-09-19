from pydantic import BaseModel
from typing import Optional


class ValidateResponse(BaseModel):
    valid: bool
    message: str
    errors: Optional[str] = None
    format: str
