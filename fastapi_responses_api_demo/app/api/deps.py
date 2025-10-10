from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.chat_service import ChatService
from app.services.openai_service import OpenAIResponsesClient


def get_db_session() -> Generator[Session, None, None]:
    yield from get_db()


def get_chat_service(db: Session = Depends(get_db_session)) -> ChatService:
    openai_client = OpenAIResponsesClient()
    return ChatService(db=db, openai_client=openai_client)
