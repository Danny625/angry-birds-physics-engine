from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from api.database import get_connection


def _row_to_level(row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "name": row["name"],
        "author": row["author"],
        "level_json": json.loads(row["level_json"]),
        "created_at": row["created_at"],
    }


def _row_to_score(row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "level_id": row["level_id"],
        "player": row["player"],
        "score": row["score"],
        "created_at": row["created_at"],
    }


def create_level(
    database_path: str | Path,
    *,
    name: str,
    author: str,
    level_json: dict[str, Any],
) -> dict[str, Any]:
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO levels (name, author, level_json)
            VALUES (?, ?, ?)
            """,
            (name, author, json.dumps(level_json)),
        )
        level_id = cursor.lastrowid
        row = connection.execute(
            "SELECT id, name, author, level_json, created_at FROM levels WHERE id = ?",
            (level_id,),
        ).fetchone()
    return _row_to_level(row)


def list_levels(database_path: str | Path) -> list[dict[str, Any]]:
    with get_connection(database_path) as connection:
        rows = connection.execute(
            """
            SELECT id, name, author, level_json, created_at
            FROM levels
            ORDER BY id ASC
            """
        ).fetchall()
    return [_row_to_level(row) for row in rows]


def get_level(database_path: str | Path, level_id: int) -> dict[str, Any] | None:
    with get_connection(database_path) as connection:
        row = connection.execute(
            """
            SELECT id, name, author, level_json, created_at
            FROM levels
            WHERE id = ?
            """,
            (level_id,),
        ).fetchone()
    if row is None:
        return None
    return _row_to_level(row)


def create_score(
    database_path: str | Path,
    *,
    level_id: int,
    player: str,
    score: int,
) -> dict[str, Any]:
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO scores (level_id, player, score)
            VALUES (?, ?, ?)
            """,
            (level_id, player, score),
        )
        score_id = cursor.lastrowid
        row = connection.execute(
            """
            SELECT id, level_id, player, score, created_at
            FROM scores
            WHERE id = ?
            """,
            (score_id,),
        ).fetchone()
    return _row_to_score(row)


def list_leaderboard(
    database_path: str | Path, level_id: int
) -> list[dict[str, Any]]:
    with get_connection(database_path) as connection:
        rows = connection.execute(
            """
            SELECT player, score, created_at
            FROM scores
            WHERE level_id = ?
            ORDER BY score DESC, id ASC
            """,
            (level_id,),
        ).fetchall()
    return [
        {"player": row["player"], "score": row["score"], "created_at": row["created_at"]}
        for row in rows
    ]
