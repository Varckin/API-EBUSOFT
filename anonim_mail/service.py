import httpx
from anonim_mail.settings import CONFIG
from anonim_mail.models import (
    CreateInboxResponse,
    GetInboxResponse,
    SetActiveResponse,
    GetMessagesResponse,
    SetPublicKeyResponse,
    CreateMessageResponse,
)


class AnonMail:
    """Async client for AnonMail API."""

    def __init__(self):
        self.base_url = CONFIG.anonmail_base_url
        self.timeout = CONFIG.timeout

    async def create_inbox(self) -> CreateInboxResponse:
        """Create a new inbox and return its private key."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            r = await client.post("/inbox/")
            r.raise_for_status()
            return CreateInboxResponse(**r.json())

    async def delete_inbox(self, private_key: str) -> str:
        """Delete an existing inbox by private key."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            r = await client.delete(f"/inbox/{private_key}")
            r.raise_for_status()
            return r.text

    async def get_inbox(self, private_key: str) -> GetInboxResponse:
        """Retrieve inbox details by private key."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            r = await client.get(f"/inbox/{private_key}")
            r.raise_for_status()
            return GetInboxResponse(**r.json())

    async def set_active(self, private_key: str, status: bool) -> SetActiveResponse:
        """Set inbox active status (True or False)."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            r = await client.post(f"/inbox/{private_key}/active", params={"status": status})
            r.raise_for_status()
            return SetActiveResponse(**r.json())

    async def delete_message(self, private_key: str, message_id: int) -> str:
        """Delete a message from the inbox by message ID."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            payload = {"message_id": message_id}
            r = await client.delete(f"/inbox/{private_key}/message", json=payload)
            r.raise_for_status()
            return r.text

    async def get_messages(self, private_key: str) -> GetMessagesResponse:
        """Get all messages for a specific inbox."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            r = await client.get(f"/inbox/{private_key}/messages")
            r.raise_for_status()
            return GetMessagesResponse(**r.json())

    async def remove_public_key(self, private_key: str) -> str:
        """Remove the public key from an inbox."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            r = await client.post(f"/inbox/{private_key}/remove-public-key")
            r.raise_for_status()
            return r.text

    async def set_public_key(self, private_key: str) -> SetPublicKeyResponse:
        """Add or reset a public key for the inbox."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            r = await client.post(f"/inbox/{private_key}/set-public-key")
            r.raise_for_status()
            return SetPublicKeyResponse(**r.json())

    async def send_message(self, key: str, content: str) -> CreateMessageResponse:
        """Send a text message to an inbox using its key."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            headers = {"Content-Type": "text/plain"}
            r = await client.post(f"/send/{key}", content=content, headers=headers)
            r.raise_for_status()
            return CreateMessageResponse(**r.json())
