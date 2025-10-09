from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.chat_service import ChatService
from app.services.openai_service import OpenAIChatClient


@lru_cache
def _get_openai_client() -> OpenAIChatClient:
    return OpenAIChatClient()


def get_openai_client() -> OpenAIChatClient:
    return _get_openai_client()


def get_chat_service(
    db: Session = Depends(get_db),
    client: OpenAIChatClient = Depends(get_openai_client),
) -> ChatService:
    return ChatService(db=db, openai_client=client)
