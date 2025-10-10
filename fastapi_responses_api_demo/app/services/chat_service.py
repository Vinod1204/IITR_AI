from __future__ import annotations

from typing import TYPE_CHECKING, List, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import models

if TYPE_CHECKING:
    from app.services.openai_service import OpenAIResponsesClient


class ChatNotFoundError(Exception):
    """Raised when attempting to access a non-existent chat."""


class ChatService:
    def __init__(self, db: Session, openai_client: "OpenAIResponsesClient") -> None:
        self._db = db
        self._openai = openai_client

    def create_chat(self) -> models.Chat:
        chat = models.Chat()
        self._db.add(chat)
        self._db.commit()
        self._db.refresh(chat)
        return chat

    def _load_chat(self, chat_id: UUID | str) -> models.Chat:
        chat = self._db.get(models.Chat, str(chat_id))
        if chat is None:
            raise ChatNotFoundError(f"Chat {chat_id} not found.")
        return chat

    def _chat_history(self, chat_id: str) -> Sequence[models.Message]:
        stmt = (
            select(models.Message)
            .where(models.Message.chat_id == chat_id)
            .order_by(models.Message.created_at.asc())
        )
        return self._db.execute(stmt).scalars().all()

    def send_message(self, chat_id: UUID | str, content: str) -> models.Message:
        chat = self._load_chat(chat_id)
        chat_id_str = str(chat.id)

        history_payload: List[dict[str, str]] = [
            {"role": message.role, "content": message.content}
            for message in self._chat_history(chat_id_str)
        ]
        history_payload.append({"role": "user", "content": content})

        response_text = self._openai.create_response(history_payload)

        user_message = models.Message(
            chat_id=chat_id_str, role="user", content=content)
        assistant_message = models.Message(
            chat_id=chat_id_str, role="assistant", content=response_text)

        self._db.add_all([user_message, assistant_message])
        self._db.commit()
        self._db.refresh(assistant_message)

        return assistant_message
