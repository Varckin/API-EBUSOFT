from data_converter.models import ConversionResponse
from fastapi import HTTPException, UploadFile
from pathlib import Path
import markdown, html2text, bleach
from data_converter.settings import CONFIG


def clean_html(html: str) -> str:
    """Sanitize HTML for safety using bleach"""
    return bleach.clean(html, tags=CONFIG.allowed_tags, attributes=CONFIG.allowed_attributes, strip=True)

def detect_format(text: str) -> str:
    """Simple auto-detection of text format: markdown or html"""
    if "<" in text and ">" in text:
        return "html"
    return "markdown"

def process_text(text: str) -> ConversionResponse:
    """Main logic for converting text between Markdown and HTML"""
    detected_format = detect_format(text)

    if detected_format == "markdown":
        html_output = markdown.markdown(text, extensions=["extra", "codehilite"])
        converted = clean_html(html_output)
        converted_format = "html"
    else:  # html
        safe_html = clean_html(text)
        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = False
        converter.body_width = 0
        converted = converter.handle(safe_html)
        converted_format = "markdown"

    return ConversionResponse(
        original=text,
        converted=converted.strip(),
        detected_format=detected_format,
        converted_format=converted_format
    )

async def process_file(file: UploadFile) -> ConversionResponse:
    """Read file and check its extension"""
    ext = Path(file.filename).suffix.lower()
    if ext not in CONFIG.allowed_file_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {CONFIG.allowed_file_extensions}"
        )
    
    content = await file.read()
    
    if len(content) > CONFIG.max_file_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is {CONFIG.max_file_size // 1024} KB"
        )
    
    text = (await file.read()).decode("utf-8")
    return process_text(text)
