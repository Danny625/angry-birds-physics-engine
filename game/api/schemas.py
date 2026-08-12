from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


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
    player: str = Field(min_length=1, max_length=80)
    score: int = Field(ge=0)

    @field_validator("player", mode="before")
    @classmethod
    def strip_player_name(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


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
