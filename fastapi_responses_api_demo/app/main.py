from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat as chat_routes
from app.core.config import get_settings
from app.db.session import init_db


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="FastAPI Responses API Demo",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(chat_routes.router)

    @app.get("/", tags=["health"])
    def healthcheck() -> dict[str, str]:
        return {"status": "ok", "model": settings.openai_model}

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    return app


app = create_app()
