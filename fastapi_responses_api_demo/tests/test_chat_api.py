from app.services.chat_service import ChatService
from app.main import create_app
from app.db.session import get_db
from app.db.models import Base
from app.api.deps import get_chat_service
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import StaticPool, create_engine
from fastapi.testclient import TestClient
from fastapi import Depends
import pytest
from uuid import UUID
from typing import Dict, List
from collections.abc import Generator
import os
os.environ.setdefault("OPENAI_API_KEY", "test-api-key")

os.environ.setdefault("OPENAI_API_KEY", "test-api-key")


class FakeOpenAIResponsesClient:
    def __init__(self, response_text: str = "Hello from test bot!") -> None:
        self._response_text = response_text
        self.last_messages: List[Dict[str, str]] = []

    def create_response(self, messages: List[Dict[str, str]]) -> str:
        self.last_messages = messages
        return self._response_text


@pytest.fixture()
def test_app():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

    Base.metadata.create_all(bind=engine)

    app = create_app()

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    fake_client = FakeOpenAIResponsesClient()

    # type: ignore[arg-type]
    def override_get_chat_service(db: Session = Depends(override_get_db)) -> ChatService:
        return ChatService(db=db, openai_client=fake_client)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_chat_service] = override_get_chat_service

    yield app, fake_client

    app.dependency_overrides.clear()


@pytest.fixture()
def client(test_app):
    app, _ = test_app
    with TestClient(app) as test_client:
        yield test_client


def test_create_chat_returns_identifier(client):
    response = client.post("/chat")
    assert response.status_code == 201
    data = response.json()
    assert "chat" in data
    assert UUID(data["chat"]["id"])  # validates UUID format


def test_send_message_returns_assistant_reply(client, test_app):
    app, fake_client = test_app
    response = client.post("/chat")
    chat_id = response.json()["chat"]["id"]

    reply = client.post(f"/chat/{chat_id}", json={"message": "Test message"})
    assert reply.status_code == 200
    payload = reply.json()
    assert payload["response"] == fake_client._response_text
    assert UUID(payload["chat_id"]) == UUID(chat_id)


def test_send_message_unknown_chat_returns_404(client):
    response = client.post(
        "/chat/00000000-0000-0000-0000-000000000000", json={"message": "Hello"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
