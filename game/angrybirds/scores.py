from __future__ import annotations

from pathlib import Path
import sqlite3

from angrybirds.constants import DEFAULT_DATABASE_PATH


def _connect(database_path: str | Path = DEFAULT_DATABASE_PATH) -> sqlite3.Connection:
    db_path = Path(database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS local_high_scores (
            level_id TEXT PRIMARY KEY,
            score INTEGER NOT NULL,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return connection


def get_high_score(level_id: str, database_path: str | Path = DEFAULT_DATABASE_PATH) -> int:
    with _connect(database_path) as connection:
        row = connection.execute(
            "SELECT score FROM local_high_scores WHERE level_id = ?",
            (level_id,),
        ).fetchone()
    if row is None:
        return 0
    return int(row["score"])


def save_high_score(
    level_id: str,
    score: int,
    database_path: str | Path = DEFAULT_DATABASE_PATH,
) -> bool:
    previous_best = get_high_score(level_id, database_path)
    if score <= previous_best:
        return False

    with _connect(database_path) as connection:
        connection.execute(
            """
            INSERT INTO local_high_scores (level_id, score, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(level_id) DO UPDATE SET
                score = excluded.score,
                updated_at = CURRENT_TIMESTAMP
            """,
            (level_id, score),
        )
    return True
