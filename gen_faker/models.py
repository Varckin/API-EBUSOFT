from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FakerRequest(BaseModel):
    provider: str = Field(..., description="Name of the generator (e.g., 'name', 'email')")
    locale: Optional[str] = Field(None, description="Faker locale, e.g., 'en_US'")
    seed: Optional[int] = Field(None, description="Optional seed value for reproducibility")
    quantity: int = Field(1, ge=1, description="Number of values to generate")
    provider_kwargs: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional keyword arguments passed directly to the Faker provider method"
    )


class FakerResponse(BaseModel):
    provider: str = Field(..., description="Name of the generator used")
    locale: str = Field(..., description="Locale applied for the generation")
    seed: Optional[int] = Field(None, description="Seed value used for reproducibility (if provided)")
    quantity: int = Field(..., description="Number of generated results")
    results: List[Any] = Field(..., description="List of generated values")
