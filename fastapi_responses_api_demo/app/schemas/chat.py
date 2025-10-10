from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ChatResource(BaseModel):
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatCreateResponse(BaseModel):
    chat: ChatResource


class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096)


class ChatMessageResponse(BaseModel):
    chat_id: UUID
    response: str
    role: str = "assistant"
    sent_at: datetime
