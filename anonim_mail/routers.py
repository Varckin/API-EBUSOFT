from fastapi import APIRouter, HTTPException, Body
from anonim_mail.service import AnonMail
from anonim_mail.models import (
    CreateInboxResponse,
    GetInboxResponse,
    GetMessagesResponse,
    CreateMessageResponse,
    SetActiveResponse,
)


router = APIRouter(prefix="/anonmail", tags=["anonmail"])
service = AnonMail()


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the anonmail module."""
    return "ok"


@router.post("/inbox", response_model=CreateInboxResponse)
async def create_inbox():
    """Create a new anonymous inbox."""
    try:
        return await service.create_inbox()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/inbox/{private_key}", response_model=GetInboxResponse)
async def get_inbox(private_key: str):
    """Retrieve inbox details by private key."""
    try:
        return await service.get_inbox(private_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/inbox/{private_key}")
async def delete_inbox(private_key: str):
    """Delete an inbox by private key."""
    try:
        return await service.delete_inbox(private_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/inbox/{private_key}/active", response_model=SetActiveResponse)
async def set_active(private_key: str, status: bool):
    """Enable or disable an inbox."""
    try:
        return await service.set_active(private_key, status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/inbox/{private_key}/messages", response_model=GetMessagesResponse)
async def get_messages(private_key: str):
    """Fetch all messages from an inbox."""
    try:
        return await service.get_messages(private_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send/{key}", response_model=CreateMessageResponse)
async def send_message(key: str, content: str = Body(..., embed=False)):
    """Send a plaintext message to a recipient key."""
    try:
        return await service.send_message(key, content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
