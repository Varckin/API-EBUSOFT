from io import BytesIO
from fastapi import HTTPException
from PIL import Image, ImageDraw
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from qrcode.image.svg import SvgImage

from qr_code.settings import CONFIG, ErrorCorrectionLevel
from qr_code.models import QRPostParams


ERROR_MAP = {
    ErrorCorrectionLevel.L: ERROR_CORRECT_L,
    ErrorCorrectionLevel.M: ERROR_CORRECT_M,
    ErrorCorrectionLevel.Q: ERROR_CORRECT_Q,
    ErrorCorrectionLevel.H: ERROR_CORRECT_H,
}


def choose_error_correction(code: str) -> int:
    """Map error correction letter to qrcode constant."""
    try:
        return ERROR_MAP[ErrorCorrectionLevel(code.upper())]
    except Exception:
        return ERROR_CORRECT_M


def validate_image_size(box_size: int, border: int, matrix_size: int):
    """Ensure image dimensions do not exceed configured maximum."""
    total_px = (matrix_size + border * 2) * box_size
    if total_px > CONFIG.max_pixel_dim:
        raise HTTPException(
            status_code=400,
            detail=f"Image too large ({total_px}px). Reduce box_size or border.",
        )


def generate_qr_image(params: QRPostParams):
    """
    Generate QR code (PNG or SVG) from QRPostParams.
    Supports optional logo overlay with white rounded background.
    """
    ec = choose_error_correction(params.error)
    qr = qrcode.QRCode(error_correction=ec, box_size=params.box_size, border=params.border)
    qr.add_data(params.data)
    qr.make(fit=True)

    matrix_size = len(qr.get_matrix())
    validate_image_size(params.box_size, params.border, matrix_size)

    # SVG output
    if params.format.lower() == "svg":
        img = qr.make_image(
            image_factory=SvgImage,
            fill_color=params.fill_color,
            back_color=params.back_color,
        )
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)
        return buffer, "image/svg+xml"

    # PNG output
    pil_img = qr.make_image(
        fill_color=params.fill_color,
        back_color=params.back_color
    ).convert("RGBA")

    # Optional logo overlay
    if params.logo:
        try:
            logo_img = Image.open(BytesIO(params.logo)).convert("RGBA")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not read logo image: {e}")

        qr_width, qr_height = pil_img.size

        # Scale logo conservatively based on error correction
        ec_ratio = {
            ERROR_CORRECT_L: 0.15,
            ERROR_CORRECT_M: 0.20,
            ERROR_CORRECT_Q: 0.25,
            ERROR_CORRECT_H: 0.30
        }.get(ec, CONFIG.max_logo_ratio)

        max_logo_size = int(min(qr_width, qr_height) * ec_ratio)
        logo_img.thumbnail((max_logo_size, max_logo_size), Image.Resampling.LANCZOS)

        # Create white circular background
        bg_size = max(logo_img.width, logo_img.height)
        background = Image.new("RGBA", (bg_size, bg_size), (255, 255, 255, 0))
        mask = Image.new("L", (bg_size, bg_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, bg_size, bg_size), fill=255)
        background.paste(logo_img, ((bg_size - logo_img.width)//2, (bg_size - logo_img.height)//2), logo_img)
        background.putalpha(mask)

        # Center background + logo on QR
        pos = ((qr_width - bg_size)//2, (qr_height - bg_size)//2)
        overlay = Image.new("RGBA", pil_img.size)
        overlay.paste(background, pos, background)
        pil_img = Image.alpha_composite(pil_img, overlay)

    buffer = BytesIO()
    pil_img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer, "image/png"
