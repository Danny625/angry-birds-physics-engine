from __future__ import annotations

import os
from pathlib import Path
import shutil
import tempfile
import uuid

import pytest


os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


@pytest.fixture
def tmp_path() -> Path:
    base_dir = Path(tempfile.gettempdir()) / "physics_game_pytest"
    path = base_dir / uuid.uuid4().hex
    path.mkdir(parents=True, exist_ok=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
