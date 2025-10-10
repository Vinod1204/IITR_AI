# FastAPI Responses API Demo

A minimal GPT-style backend built with FastAPI, SQLite, and the OpenAI Responses API.

## Features
- `POST /chat` creates a new chat and returns its identifier.
- `POST /chat/{chat_id}` sends a message within a chat and returns the assistant response from `gpt-5-nano-2025-08-07`.
- Conversation history is persisted in SQLite so each reply is grounded in prior messages.

## Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (optional, recommended)
- An OpenAI API key with access to `gpt-5-nano-2025-08-07`

## Setup
```bash
cd fastapi_responses_api_demo
uv sync  # or: pip install -e .[dev]
```

Copy `.env.example` to `.env` and set the variables:
```bash
cp .env.example .env
```

## Running the application
```bash
uvicorn app.main:app --reload
```

## API quickstart
- `POST /chat`
  ```json
  {}
  ```
- `POST /chat/{chat_id}`
  ```json
  {
    "message": "Write a Python function that reverses a string."
  }
  ```

## Testing
```bash
uv run pytest
```
