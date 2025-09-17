from fastapi import APIRouter, HTTPException
from typing import List
from gen_uuid.models import UUIDRequest
from gen_uuid.service import UUID

router = APIRouter(prefix="/uuid", tags=["uuid"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the uuid module."""
    return "ok"

@router.post("", response_model=List[str])
async def gen_uuid(request: UUIDRequest) -> List[str]:
    """Generating UUIDs of Different Versions"""
    result: List[str] = []
    uuid = UUID()

    for _ in range(request.count):
        if request.version == 'v3':
            result.append(uuid.create_uuid3(request.text))
        elif request.version == 'v4':
            result.append(uuid.create_uuid4())
        elif request.version == 'v5':
            result.append(uuid.create_uuid5(request.text))
        else:
            raise HTTPException(status_code=400, detail="Invalid UUID version")
        
    return result
