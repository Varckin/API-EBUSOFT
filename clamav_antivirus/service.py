import clamd, io
from fastapi import UploadFile, HTTPException

from clamav_antivirus.settings import CONFIG
from clamav_antivirus.models import ScanResponse


def get_clamd_client() -> clamd.ClamdNetworkSocket:
    """Initialize ClamAV client."""
    try:
        client = clamd.ClamdNetworkSocket(
            host=CONFIG.clamav_host,
            port=CONFIG.clamav_port,
        )
        client.ping()
        return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ClamAV is not available: {e}")

async def scan_file(file: UploadFile) -> ScanResponse:
    """Scan an uploaded file for viruses using ClamAV instream mode."""
    contents = await file.read()
    file_size_mb = len(contents) / (1024 * 1024)
    if file_size_mb > CONFIG.max_file_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum allowed size of {CONFIG.max_file_size_mb} MB",
        )

    try:
        client = get_clamd_client()
        file_stream = io.BytesIO(contents)
        result = client.instream(file_stream)

        if not result:
            return ScanResponse(filename=file.filename, is_infected=False)

        # result format: {"stream": ("FOUND"/"OK", "VirusName")}
        status, signature = result.get("stream", ("OK", None))
        return ScanResponse(
            filename=file.filename,
            is_infected=(status == "FOUND"),
            signature=signature if status == "FOUND" else None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ClamAV scan error: {e}")

async def health_check() -> str:
    """Check ClamAV availability."""
    try:
        client = get_clamd_client()
        return client.ping()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ClamAV health error: {e}")
