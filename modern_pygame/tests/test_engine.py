from __future__ import annotations

from angrybirds.engine import GameEngine
from angrybirds.levels import load_all_levels, load_level_file


def test_blue_bird_split_creates_three_flight_paths() -> None:
    engine = GameEngine(load_all_levels())
    engine.start_level("level5")
    engine.state.birds_waiting = [
        bird for bird in engine.state.birds_waiting if bird.bird_type == "blue"
    ] + [bird for bird in engine.state.birds_waiting if bird.bird_type != "blue"]
    engine.state.birds_waiting[0].x = 120
    engine.state.birds_waiting[0].y = 550
    engine.state.dragging = True
    engine.release_bird()

    for _ in range(5):
        engine.tick()
    engine.activate_ability()

    assert len(engine.state.birds_in_flight) == 3
    heads = [[(x, y) for x, y, _ in bird.trajectory[:2]] for bird in engine.state.birds_in_flight]
    assert heads[1][0][1] < heads[0][0][1]
    assert heads[2][0][1] > heads[0][0][1]


def test_eagle_ability_redirects_to_vertical_drop() -> None:
    engine = GameEngine(load_all_levels())
    engine.start_level("level5")
    engine.state.birds_waiting = [
        bird for bird in engine.state.birds_waiting if bird.bird_type == "eagle"
    ] + [bird for bird in engine.state.birds_waiting if bird.bird_type != "eagle"]
    engine.state.birds_waiting[0].x = 120
    engine.state.birds_waiting[0].y = 550
    engine.state.dragging = True
    engine.release_bird()

    for _ in range(5):
        engine.tick()
    engine.activate_ability()

    trajectory_head = engine.state.birds_in_flight[0].trajectory[:4]
    xs = {round(x, 2) for x, _y, _v in trajectory_head}
    assert len(xs) == 1


def test_builder_level_can_be_saved_and_loaded(tmp_path) -> None:
    engine = GameEngine(load_all_levels())
    engine.start_builder()
    engine.add_builder_bird("red")
    engine.add_builder_bird("blue")
    engine.place_builder_item("wood_box", 860, 520)
    engine.place_builder_item("pig1", 920, 430)

    save_path = tmp_path / "builder_level.json"
    saved_level = engine.save_builder_level(save_path)
    loaded_level = load_level_file(save_path)

    assert loaded_level == saved_level

    engine.clear_builder_world()
    engine.clear_builder_birds()
    engine.load_builder_level(save_path)

    assert [bird.bird_type for bird in engine.state.birds_waiting] == ["red", "blue"]
    assert len(engine.state.pigs) == 1
    assert len(engine.state.objects) == 1


def test_loaded_builder_level_can_be_replaced_with_new_name(tmp_path) -> None:
    engine = GameEngine(load_all_levels())
    engine.start_builder()
    engine.add_builder_bird("red")
    save_path = tmp_path / "builder_level_01.json"
    engine.save_builder_level(save_path, name="First Draft", level_id="builder_level_01")

    engine.load_builder_level(save_path)
    engine.add_builder_bird("eagle")
    replaced_level, replaced_path = engine.replace_current_builder_level(
        name="Final Siege"
    )
    loaded_level = load_level_file(save_path)

    assert replaced_path == save_path
    assert replaced_level.name == "Final Siege"
    assert loaded_level.name == "Final Siege"
    assert loaded_level.birds == ["red", "eagle"]
