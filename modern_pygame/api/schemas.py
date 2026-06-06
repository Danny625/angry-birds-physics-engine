from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class StarThresholds(BaseModel):
    one: int = Field(ge=0)
    two: int = Field(ge=0)
    three: int = Field(ge=0)


class LevelPayload(BaseModel):
    id: str
    name: str
    birds: list[str]
    pigs: list[dict[str, Any]]
    objects: list[dict[str, Any]]
    stars: StarThresholds


class LevelCreate(BaseModel):
    name: str
    author: str = "local"
    level_json: LevelPayload


class LevelResponse(BaseModel):
    id: int
    name: str
    author: str
    level_json: LevelPayload
    created_at: str


class ScoreCreate(BaseModel):
    level_id: int
    player: str
    score: int = Field(ge=0)


class ScoreResponse(BaseModel):
    id: int
    level_id: int
    player: str
    score: int
    created_at: str


class LeaderboardEntry(BaseModel):
    player: str
    score: int
    created_at: str
