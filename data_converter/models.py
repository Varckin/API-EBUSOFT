from pydantic import BaseModel, Field


class ConversionRequest(BaseModel):
    text: str | None = Field(None, description="Text to convert")


class ConversionResponse(BaseModel):
    original: str
    converted: str
    detected_format: str
    converted_format: str
