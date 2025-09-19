from fastapi import APIRouter, HTTPException, Body, UploadFile, File
from data_converter.models import ConversionRequest, ConversionResponse
from data_converter.service import process_file, process_text


router = APIRouter(prefix="/converter", tags=["converter"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the converter module."""
    return "ok"

@router.post("", response_model=ConversionResponse)
async def convert_markdown_html(
    data: ConversionRequest = Body(None),
    file: UploadFile | None = File(None)
):
    """
    Convert text between Markdown and HTML.

    The format of the input is automatically detected:
    - Markdown will be converted to sanitized HTML.
    - HTML will be converted to Markdown.
    """
    if file:
        return await process_file(file)
    elif data and data.text:
        return process_text(data.text)
    else:
        raise HTTPException(status_code=400, detail="No input provided. Use 'text' or upload a file.")
