from enum import Enum
from pydantic import BaseModel, Field, conint, confloat


class ErrorCorrectionLevel(str, Enum):
    L = "L"
    M = "M"
    Q = "Q"
    H = "H"


class QRConfig(BaseModel):
    max_data_length: conint(ge=1) = Field(
        4000, description="Maximum number of characters in QR data"
    )
    max_box_size: conint(ge=1) = Field(
        40, description="Maximum pixel size per QR box"
    )
    max_border: conint(ge=0) = Field(
        50, description="Maximum border size in boxes"
    )
    max_pixel_dim: conint(ge=1) = Field(
        10000, description="Maximum total image dimension in pixels"
    )
    max_logo_ratio: confloat(gt=0.0, le=1.0) = Field(
        0.22, description="Max logo size as fraction of QR width"
    )


CONFIG = QRConfig()
