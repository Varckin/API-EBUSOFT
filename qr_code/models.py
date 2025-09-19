from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from qr_code.settings import CONFIG, ErrorCorrectionLevel


class ImageFormat(str, Enum):
    png = "PNG"
    svg = "SVG"


class QRPostParams(BaseModel):
    data: str = Field(..., min_length=1, description="String encoded into QR")
    format: ImageFormat = Field(ImageFormat.png, description="Output format: PNG or SVG")
    error: ErrorCorrectionLevel = Field(ErrorCorrectionLevel.M, description="Error correction level (L/M/Q/H)")
    box_size: int = Field(10, description="Pixel size of each QR box")
    border: int = Field(4, description="Border boxes count")
    fill_color: str = Field("black", description="Fill color (PIL color string or hex)")
    back_color: str = Field("white", description="Background color (PIL color string or hex)")
    logo: Optional[bytes] = Field(None, description="Optional logo image bytes")

    @field_validator("data")
    @classmethod
    def check_data_length(cls, v: str) -> str:
        if len(v) > CONFIG.max_data_length:
            raise ValueError(f"data length exceeds maximum of {CONFIG.max_data_length} characters")
        return v

    @field_validator("box_size")
    @classmethod
    def check_box_size(cls, v: int) -> int:
        if v < 1 or v > CONFIG.max_box_size:
            raise ValueError(f"box_size must be between 1 and {CONFIG.max_box_size}")
        return v

    @field_validator("border")
    @classmethod
    def check_border(cls, v: int) -> int:
        if v < 0 or v > CONFIG.max_border:
            raise ValueError(f"border must be between 0 and {CONFIG.max_border}")
        return v
