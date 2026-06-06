from __future__ import annotations

from angrybirds.levels import (
    delete_saved_builder_level,
    list_saved_builder_levels,
    level_from_dict,
    level_to_dict,
    load_level,
    load_level_file,
    next_builder_save_path,
    save_level,
)
from angrybirds.models import LevelSpec


def test_level_dict_round_trip_preserves_fields() -> None:
    level = LevelSpec(
        level_id="roundtrip",
        name="Round Trip",
        birds=["red", "blue"],
        pigs=[{"x": 800, "y": 400, "angle": 0}],
        objects=[{"kind": "box", "material": "wood", "x": 760, "y": 520, "angle": 0}],
        stars=(100, 200, 300),
    )

    restored = level_from_dict(level_to_dict(level))

    assert restored.level_id == level.level_id
    assert restored.name == level.name
    assert restored.birds == level.birds
    assert restored.pigs == level.pigs
    assert restored.objects == level.objects
    assert restored.stars == level.stars


def test_save_and_load_level_file(tmp_path) -> None:
    level = LevelSpec(
        level_id="saved",
        name="Saved Level",
        birds=["yellow", "eagle"],
        pigs=[{"x": 900, "y": 420, "angle": 0}],
        objects=[{"kind": "column", "material": "stone", "x": 940, "y": 600, "angle": 0}],
        stars=(250, 500, 750),
    )
    output_path = tmp_path / "saved_level.json"

    save_level(level, output_path)
    loaded = load_level_file(output_path)

    assert loaded == level


def test_builder_save_slots_are_numbered_and_listable(tmp_path) -> None:
    first_path, first_slot = next_builder_save_path(tmp_path)
    second_path, second_slot = next_builder_save_path(tmp_path)

    assert first_slot == 1
    assert second_slot == 1

    first_level = LevelSpec(
        level_id="builder_level_01",
        name="Builder Level 01",
        birds=["red"],
        pigs=[],
        objects=[],
        stars=(500, 1000, 1500),
    )
    save_level(first_level, first_path)

    second_path, second_slot = next_builder_save_path(tmp_path)
    second_level = LevelSpec(
        level_id="builder_level_02",
        name="Builder Level 02",
        birds=["blue", "eagle"],
        pigs=[{"x": 900, "y": 430, "angle": 0}],
        objects=[],
        stars=(500, 1000, 1500),
    )
    save_level(second_level, second_path)

    saved_levels = list_saved_builder_levels(tmp_path)

    assert second_slot == 2
    assert [level.name for _path, level in saved_levels] == [
        "Builder Level 01",
        "Builder Level 02",
    ]


def test_deleting_builder_save_compacts_remaining_slots(tmp_path) -> None:
    levels = [
        LevelSpec(
            level_id=f"builder_level_{index:02d}",
            name=f"Custom {index}",
            birds=["red"],
            pigs=[],
            objects=[],
            stars=(500, 1000, 1500),
        )
        for index in range(1, 4)
    ]
    for index, level in enumerate(levels, start=1):
        save_level(level, tmp_path / f"builder_level_{index:02d}.json")

    delete_saved_builder_level(tmp_path / "builder_level_01.json", tmp_path)
    saved_levels = list_saved_builder_levels(tmp_path)
    saved_paths = [path.name for path, _level in saved_levels]
    saved_ids = [level.level_id for _path, level in saved_levels]
    saved_names = [level.name for _path, level in saved_levels]

    assert saved_paths == ["builder_level_01.json", "builder_level_02.json"]
    assert saved_ids == ["builder_level_01", "builder_level_02"]
    assert saved_names == ["Custom 2", "Custom 3"]


def test_builtin_level_loads_expected_structure() -> None:
    level = load_level("level1")

    assert level.level_id == "level1"
    assert level.name == "Level 1"
    assert level.birds
    assert level.pigs
    assert level.objects
