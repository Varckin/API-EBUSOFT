from fastapi import APIRouter, Form, UploadFile, File
from fastapi.responses import Response

from qr_code.models import QRPostParams, ImageFormat
from qr_code.service import generate_qr_image


router = APIRouter(prefix="/qr", tags=["qr"])

@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the qr module."""
    return "ok"

@router.post("")
async def generate_qr(
    data: str = Form(..., description="String encoded into QR"),
    format: str = Form("png", description="Output format: png or svg"),
    error: str = Form("M", description="Error correction level: L/M/Q/H"),
    box_size: int = Form(10, description="Pixel size of each QR box"),
    border: int = Form(4, description="Border size in boxes"),
    fill_color: str = Form("black", description="Fill color"),
    back_color: str = Form("white", description="Background color"),
    logo: UploadFile | None = File(None, description="Optional logo image"),
):
    """
    Generate a QR code as PNG or SVG with optional logo overlay.
    """
    logo_bytes = await logo.read() if logo else None

    params = QRPostParams(
        data=data,
        format=ImageFormat(format.upper()),
        error=error,
        box_size=box_size,
        border=border,
        fill_color=fill_color,
        back_color=back_color,
        logo=logo_bytes,
    )

    buffer, media_type = generate_qr_image(params)

    filename = f"qrcode.{params.format.lower()}"
    return Response(
        content=buffer.getvalue(),
        media_type=media_type,
        headers={"Content-Disposition": f'inline; filename="{filename}"'},
    )
