from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Any

from angrybirds.constants import LEVEL_DIR, SAVED_LEVEL_DIR
from angrybirds.models import LevelSpec


BUILDER_SAVE_PATTERN = re.compile(r"builder_level_(\d+)\.json$")


def level_to_dict(level: LevelSpec) -> dict[str, Any]:
    return {
        "id": level.level_id,
        "name": level.name,
        "birds": list(level.birds),
        "pigs": deepcopy(level.pigs),
        "objects": deepcopy(level.objects),
        "stars": {
            "one": level.stars[0],
            "two": level.stars[1],
            "three": level.stars[2],
        },
    }


def level_from_dict(data: dict[str, Any]) -> LevelSpec:
    stars = data.get("stars", {})
    return LevelSpec(
        level_id=data["id"],
        name=data["name"],
        birds=list(data["birds"]),
        pigs=deepcopy(data["pigs"]),
        objects=deepcopy(data["objects"]),
        stars=(
            int(stars.get("one", 0)),
            int(stars.get("two", 0)),
            int(stars.get("three", 0)),
        ),
    )


def load_level_file(path: str | Path) -> LevelSpec:
    level_path = Path(path)
    data = json.loads(level_path.read_text())
    return level_from_dict(data)


def save_level(level: LevelSpec, path: str | Path) -> Path:
    level_path = Path(path)
    level_path.parent.mkdir(parents=True, exist_ok=True)
    level_path.write_text(json.dumps(level_to_dict(level), indent=2))
    return level_path


def builder_save_path(slot_number: int, directory: str | Path = SAVED_LEVEL_DIR) -> Path:
    return Path(directory) / f"builder_level_{slot_number:02d}.json"


def next_builder_save_path(directory: str | Path = SAVED_LEVEL_DIR) -> tuple[Path, int]:
    save_dir = Path(directory)
    save_dir.mkdir(parents=True, exist_ok=True)
    used_slots: set[int] = set()
    for save_path in save_dir.glob("builder_level_*.json"):
        match = BUILDER_SAVE_PATTERN.match(save_path.name)
        if match:
            used_slots.add(int(match.group(1)))

    slot_number = 1
    while slot_number in used_slots:
        slot_number += 1
    return builder_save_path(slot_number, save_dir), slot_number


def list_saved_builder_levels(
    directory: str | Path = SAVED_LEVEL_DIR,
) -> list[tuple[Path, LevelSpec]]:
    saved_levels: list[tuple[Path, LevelSpec]] = []
    save_dir = Path(directory)
    if not save_dir.exists():
        return saved_levels

    for save_path in sorted(save_dir.glob("builder_level_*.json")):
        try:
            saved_levels.append((save_path, load_level_file(save_path)))
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            continue
    return saved_levels


def delete_saved_builder_level(
    path: str | Path,
    directory: str | Path = SAVED_LEVEL_DIR,
) -> None:
    save_path = Path(path)
    save_dir = Path(directory)
    save_path.unlink(missing_ok=True)
    compact_builder_save_slots(save_dir)


def compact_builder_save_slots(directory: str | Path = SAVED_LEVEL_DIR) -> None:
    save_dir = Path(directory)
    saved_levels = list_saved_builder_levels(save_dir)
    if not saved_levels:
        return

    temp_paths: list[tuple[Path, LevelSpec]] = []
    for index, (old_path, level) in enumerate(saved_levels, start=1):
        temp_path = save_dir / f"__builder_compact_{index:02d}.json"
        old_path.replace(temp_path)
        temp_paths.append((temp_path, level))

    for index, (temp_path, level) in enumerate(temp_paths, start=1):
        level.level_id = f"builder_level_{index:02d}"
        save_level(level, builder_save_path(index, save_dir))
        temp_path.unlink(missing_ok=True)


def load_level(level_id: str) -> LevelSpec:
    level_path = LEVEL_DIR / f"{level_id}.json"
    return load_level_file(level_path)


def load_all_levels() -> dict[str, LevelSpec]:
    levels: dict[str, LevelSpec] = {}
    for level_path in sorted(LEVEL_DIR.glob("level*.json")):
        level = load_level(level_path.stem)
        levels[level.level_id] = level
    return levels
