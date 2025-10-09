from typing import Any, Dict, List, Union

from openai import NotFoundError, OpenAI, OpenAIError

from app.core.config import get_settings


class OpenAIChatClient:
    """Wrapper around the OpenAI SDK that exposes a focused chat completion API."""

    def __init__(self) -> None:
        settings = get_settings()
        self._model = settings.openai_model
        self._temperature = settings.openai_temperature
        self._max_output_tokens = settings.openai_max_output_tokens
        self._fallback_model = settings.openai_fallback_model
        self._client = OpenAI(api_key=settings.openai_api_key)

    def create_completion(self, messages: List[Dict[str, str]]) -> str:
        last_not_found_error: RuntimeError | None = None

        for model_name in self._candidate_models():
            try:
                response = self._client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=self._temperature,
                    max_tokens=self._max_output_tokens,
                )
            except NotFoundError as exc:  # pragma: no cover - depends on external API state
                last_not_found_error = RuntimeError(
                    "The configured OpenAI model \"{}\" could not be found or is inaccessible. "
                    "Update `OPENAI_MODEL` or set `OPENAI_FALLBACK_MODEL` to a model your API key can use."
                    .format(model_name)
                )
                continue
            except OpenAIError as exc:  # pragma: no cover - depends on external API state
                raise RuntimeError(
                    f"OpenAI API error ({exc.__class__.__name__}): {exc}"
                ) from exc
            except Exception as exc:  # pragma: no cover - defensive guard
                raise RuntimeError(
                    f"Unexpected error while requesting OpenAI completion: {exc}"
                ) from exc

            if model_name != self._model:
                self._model = model_name
            return self._extract_text(response)

        if last_not_found_error:
            raise last_not_found_error

        raise RuntimeError(
            "Failed to obtain a completion from OpenAI without a specific error.")

    def _candidate_models(self) -> List[str]:
        candidates = [self._model]
        if self._fallback_model and self._fallback_model != self._model:
            candidates.append(self._fallback_model)
        return candidates

    def _extract_text(self, response: Any) -> str:
        message = response.choices[0].message
        if message is None or message.content is None:
            raise RuntimeError("Empty response from OpenAI chat completion.")
        content: Union[str, List[Any]] = message.content
        if isinstance(content, list):
            text = "".join(part.get("text", "")
                           for part in content if isinstance(part, dict))
        else:
            text = content
        text = text.strip()
        if not text:
            raise RuntimeError("OpenAI response did not contain text content.")
        return text
