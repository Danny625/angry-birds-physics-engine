from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from api import models
from api.schemas import LeaderboardEntry, ScoreCreate, ScoreResponse

router = APIRouter(tags=["scores"])


@router.post("/scores", response_model=ScoreResponse, status_code=201)
def create_score(payload: ScoreCreate, request: Request) -> dict:
    level = models.get_level(request.app.state.database_path, payload.level_id)
    if level is None:
        raise HTTPException(status_code=404, detail="Level not found")
    return models.create_score(
        request.app.state.database_path,
        level_id=payload.level_id,
        player=payload.player,
        score=payload.score,
    )


@router.get("/leaderboard/{level_id}", response_model=list[LeaderboardEntry])
def get_leaderboard(level_id: int, request: Request) -> list[dict]:
    return models.list_leaderboard(request.app.state.database_path, level_id)
