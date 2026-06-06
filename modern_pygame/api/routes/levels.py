from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from api import models
from api.schemas import LevelCreate, LevelResponse

router = APIRouter(prefix="/levels", tags=["levels"])


@router.post("", response_model=LevelResponse, status_code=201)
def create_level(payload: LevelCreate, request: Request) -> dict:
    return models.create_level(
        request.app.state.database_path,
        name=payload.name,
        author=payload.author,
        level_json=payload.level_json.model_dump(),
    )


@router.get("", response_model=list[LevelResponse])
def list_levels(request: Request) -> list[dict]:
    return models.list_levels(request.app.state.database_path)


@router.get("/{level_id}", response_model=LevelResponse)
def get_level(level_id: int, request: Request) -> dict:
    level = models.get_level(request.app.state.database_path, level_id)
    if level is None:
        raise HTTPException(status_code=404, detail="Level not found")
    return level
