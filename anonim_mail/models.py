from typing import List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    id: int
    content: str
    created_at: int


class Inbox(BaseModel):
    private_key: str
    public_key: Optional[str] = None
    active: Optional[bool] = True
    message_count: Optional[int] = 0


class CreateInboxResponse(BaseModel):
    private_key: str


class GetInboxResponse(BaseModel):
    active: bool
    message_count: int
    private_key: str
    public_key: Optional[str] = None


class SetActiveResponse(BaseModel):
    active: bool


class GetMessagesResponse(BaseModel):
    messages: List[Message]


class SetPublicKeyResponse(BaseModel):
    public_key: str


class CreateMessageResponse(BaseModel):
    message: Message
