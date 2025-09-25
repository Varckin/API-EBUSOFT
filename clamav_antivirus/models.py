from pydantic import BaseModel, Field


class ScanResponse(BaseModel):
    filename: str = Field(..., description="Name of the file")
    is_infected: bool = Field(..., description="Infection flag")
    signature: str | None = Field(None, description="Virus signature (if detected)")


class HealthResponse(BaseModel):
    status: str = Field(..., description="ClamAV status (PONG/OK/ERROR)")
