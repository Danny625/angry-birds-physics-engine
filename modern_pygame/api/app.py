from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from api.database import init_db, resolve_db_path
from api.routes.levels import router as levels_router
from api.routes.scores import router as scores_router
from api.schemas import HealthResponse


def create_app(database_path: str | Path | None = None) -> FastAPI:
    app = FastAPI(
        title="Physics Game API",
        version="1.0.0",
        description="Local-first API for saving levels and leaderboard scores.",
    )

    app.state.database_path = resolve_db_path(database_path)
    init_db(app.state.database_path)

    @app.get("/health", response_model=HealthResponse, tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(levels_router)
    app.include_router(scores_router)
    return app
