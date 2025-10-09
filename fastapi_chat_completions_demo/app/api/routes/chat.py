from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_service
from app.schemas.chat import ChatCreateResponse, ChatMessageRequest, ChatMessageResponse, ChatResource
from app.services.chat_service import ChatNotFoundError, ChatService


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "",
    response_model=ChatCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_chat(chat_service: ChatService = Depends(get_chat_service)) -> ChatCreateResponse:
    chat = chat_service.create_chat()
    resource = ChatResource.model_validate(chat, from_attributes=True)
    return ChatCreateResponse(chat=resource)


@router.post(
    "/{chat_id}",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_200_OK,
)
def send_message(
    chat_id: UUID,
    payload: ChatMessageRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatMessageResponse:
    try:
        message = chat_service.send_message(chat_id, payload.message)
    except ChatNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "message": "Failed to generate response from language model.",
                "reason": str(exc),
            },
        ) from exc
    return ChatMessageResponse(
        chat_id=UUID(message.chat_id),
        response=message.content,
        role=message.role,
        sent_at=message.created_at,
    )
