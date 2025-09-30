from pydantic import BaseModel, Field
from datetime import datetime


class TotpCreateRequest(BaseModel):
    service_name: str = Field(..., max_length=50, description="Name service")
    secret_key: str = Field(..., max_length=255, description="Secret key TOTP")


class TotpCreateResponse(BaseModel):
    id: str
    service_name: str
    created_at: datetime


class TotpGenerateRequest(BaseModel):
    id: str = Field(..., description="ID recording TOTP")


class TotpGenerateResponse(BaseModel):
    id: str
    service_name: str
    code: str


class TotpDeleteRequest(BaseModel):
    id: str = Field(..., description="ID records to delete")


class TotpDeleteResponse(BaseModel):
    id: str
    status: str
