from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from angrybirds.constants import DEFAULT_DATABASE_PATH


def resolve_db_path(database_path: str | Path | None = None) -> Path:
    raw_path = database_path or os.environ.get(
        "PHYSICS_GAME_DB_PATH", str(DEFAULT_DATABASE_PATH)
    )
    path = Path(raw_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_connection(database_path: str | Path | None = None) -> sqlite3.Connection:
    db_path = resolve_db_path(database_path)
    db_dir = os.path.dirname(str(db_path))
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(database_path: str | Path | None = None) -> Path:
    db_path = resolve_db_path(database_path)
    with get_connection(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                author TEXT NOT NULL,
                level_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level_id INTEGER NOT NULL,
                player TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(level_id) REFERENCES levels(id) ON DELETE CASCADE
            );
            """
        )
    return db_path
