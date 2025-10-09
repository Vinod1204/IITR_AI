# FastAPI Chat Completions Demo

A minimal GPT-style backend built with FastAPI, SQLite, and the OpenAI Chat Completions API.

## Features
- `POST /chat` creates a new chat and returns its identifier.
- `POST /chat/{chat_id}` sends a message within a chat and streams the response from `gpt-5-codex-preview`.
- Conversation history is persisted in SQLite for grounded responses.

## Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (optional, recommended)
- An OpenAI API key with access to `gpt-5-nano-2025-08-07`

## Setup
```bash
cd fastapi_chat_completions_demo
uv sync  # or: pip install -e .[dev]
```


Copy `.env.example` to `.env` and populate the values:
```bash
cp .env.example .env
```

Update the `.env` file with your OpenAI key and confirm `OPENAI_MODEL=gpt-5-codex-preview` (or override with another model if needed). Optionally set `OPENAI_FALLBACK_MODEL` (defaults to `gpt-4o-mini`) to automatically retry with a model you can access. If both fail, the API response will include the upstream error reason.

## Running the application
```bash
uvicorn app.main:app --reload
```

## Testing
```bash
uv run pytest
```
