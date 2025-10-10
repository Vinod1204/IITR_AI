from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI, OpenAIError

from app.core.config import get_settings


class OpenAIResponsesClient:
    """Wrapper around the OpenAI Responses API for chat-style interactions."""

    def __init__(self) -> None:
        settings = get_settings()
        self._model = settings.openai_model
        self._max_output_tokens = settings.openai_max_output_tokens
        if not settings.openai_api_key:
            raise RuntimeError(
                "Missing OpenAI API key. Set the OPENAI_API_KEY environment variable or configure it in .env."
            )
        self._client = OpenAI(api_key=settings.openai_api_key)

    def create_response(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = self._client.responses.create(
                model=self._model,
                input=[self._format_message(message) for message in messages],
                max_output_tokens=self._max_output_tokens,
            )
        except OpenAIError as exc:  # pragma: no cover - external dependency errors
            raise RuntimeError(
                f"OpenAI API error ({exc.__class__.__name__}): {exc}") from exc

        return self._extract_text(response)

    @staticmethod
    def _format_message(message: Dict[str, str]) -> Dict[str, Any]:
        role = message.get("role", "user")
        text = message.get("content", "")
        content_type = "output_text" if role == "assistant" else "input_text"
        return {
            "role": role,
            "content": [
                {
                    "type": content_type,
                    "text": text,
                }
            ],
        }

    @staticmethod
    def _extract_text(response: Any) -> str:
        output_text = getattr(response, "output_text", None)
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        text_fragments: List[str] = []
        for output in getattr(response, "output", []) or []:
            content_items = getattr(output, "content", []) or []
            for item in content_items:
                text = getattr(item, "text", None)
                if text:
                    text_fragments.append(text)
                elif isinstance(item, dict):
                    candidate = item.get("text")
                    if candidate:
                        text_fragments.append(candidate)
        text = "".join(text_fragments).strip()
        if not text:
            raise RuntimeError("OpenAI response did not include text content.")
        return text
