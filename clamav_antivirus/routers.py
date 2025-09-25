from fastapi import APIRouter, UploadFile, File
from clamav_antivirus.models import HealthResponse, ScanResponse
from clamav_antivirus.service import scan_file, health_check


router = APIRouter(prefix="/clamav", tags=["clamav"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Check the status of ClamAV."""
    status = await health_check()
    return HealthResponse(status=status)

@router.post("", response_model=ScanResponse)
async def scan(uploaded_file: UploadFile = File(...)) -> ScanResponse:
    """Scan an uploaded file for viruses."""
    return await scan_file(uploaded_file)
