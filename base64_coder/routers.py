from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse

from base64_coder.settings import CONFIG
from base64_coder.models import StringRequest, StringResponse
from base64_coder.service import (
    encode_string,
    decode_string,
    encode_file,
    decode_file,
)

router = APIRouter(prefix="/base64", tags=["base64"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the Base64 module."""
    return "ok"


@router.post("/string", response_model=StringResponse)
async def string_action(request: StringRequest):
    """
    Encode or decode a string using Base64.
    """
    action = request.action.lower()
    try:
        if action == "encode":
            return StringResponse(result=encode_string(request.data))
        elif action == "decode":
            return StringResponse(result=decode_string(request.data))
        else:
            raise HTTPException(status_code=400, detail="action must be either 'encode' or 'decode'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while processing string: {str(e)}")


@router.post("/file")
async def file_action(
    action: str = Form(...),
    file: UploadFile = File(None),
    data: str = Form(None),
    filename: str = Form(None),
):
    """
    Handle file encoding/decoding in Base64.
    """
    action = action.lower()
    if action == "encode":
        if file is None:
            raise HTTPException(status_code=400, detail="File is required for encoding")
        try:
            content = await file.read()

            if len(content) > CONFIG.max_file_size:
                raise HTTPException(
                    status_code=413,
                    detail=f"File size exceeds the maximum allowed limit of {CONFIG.max_file_size} bytes"
                )
            
            return {"result": encode_file(content)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while encoding file: {str(e)}")

    elif action == "decode":
        if data is None or filename is None:
            raise HTTPException(status_code=400, detail="data and filename are required for decoding")
        try:
            file_path = decode_file(data, filename, CONFIG.temp_dir)

            if file_path.stat().st_size > CONFIG.max_file_size:
                file_path.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=413,
                    detail=f"Decoded file size exceeds the maximum allowed limit of {CONFIG.max_file_size} bytes"
                )
            
            return FileResponse(path=file_path, filename=file_path.name, media_type="application/octet-stream")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while decoding file: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="action must be either 'encode' or 'decode'")
