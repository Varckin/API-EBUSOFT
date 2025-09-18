from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from gen_hash.models import HashRequest
from gen_hash.service import compute_hashes
from gen_hash.settings import CONFIG


router = APIRouter(prefix="/hash", tags=["hash"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the hash module."""
    return "ok"

@router.post("/text")
async def hash_text(request: HashRequest):
    """
    Generate hashes for text with the option to choose algorithms.
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    algorithms = request.algorithms or CONFIG.default_algorithms
    try:
        result = compute_hashes(request.text.encode("utf-8"), algorithms)
        return {"hashes": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/file")
async def hash_file(
    file: UploadFile = File(...),
    algorithms: Optional[List[str]] = Form(None)
):
    """
    Generate hashes for an uploaded file with the option to choose algorithms.
    """
    try:
        content = await file.read()
        size_mb = len(content) / (1024 * 1024)
        if size_mb > CONFIG.max_file_size_mb:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size is {CONFIG.max_file_size_mb} MB"
            )
        algo_list = algorithms or CONFIG.default_algorithms
        result = compute_hashes(content, algo_list)
        return {"filename": file.filename, "hashes": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
