from __future__ import annotations

import math
from pathlib import Path
from typing import Optional, Union

from angrybirds.constants import (
    DEFAULT_BUILDER_LEVEL_PATH,
    FLOOR_Y,
    INIT_BIRD_X,
    INIT_BIRD_Y,
    PHYSICS_SUBSTEPS,
    SIMULATION_DT,
    SLING_MAX,
    TRAJECTORY_DT,
)
from angrybirds.levels import load_level_file, next_builder_save_path, save_level
from angrybirds.models import BirdState, BodyState, GameState, LevelSpec


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


class GameEngine:
    def __init__(self, levels: dict[str, LevelSpec]) -> None:
        self.levels = levels
        self.state = GameState()
        self.builder_blueprint: Optional[LevelSpec] = None
        self.current_builder_save_path: Optional[Path] = None

    def _state_from_spec(
        self,
        level: LevelSpec,
        *,
        builder_mode: bool = False,
        builder_playing: bool = False,
    ) -> GameState:
        birds_waiting: list[BirdState] = []
        for index, bird_type in enumerate(level.birds):
            if index == 0:
                x, y = INIT_BIRD_X, INIT_BIRD_Y
            else:
                x, y = INIT_BIRD_X - 50 * index, FLOOR_Y - 20
            birds_waiting.append(BirdState(bird_type=bird_type, x=x, y=y))

        pigs = [
            BodyState(
                kind="pig",
                x=pig["x"],
                y=pig["y"],
                angle=pig.get("angle", 0),
                material="flesh",
            )
            for pig in level.pigs
        ]
        objects = [
            BodyState(
                kind=obj["kind"],
                x=obj["x"],
                y=obj["y"],
                angle=obj.get("angle", 0),
                material=obj["material"],
            )
            for obj in level.objects
        ]

        level_name = "Builder Mode" if builder_mode else level.name
        level_id = "builder" if builder_mode else level.level_id

        return GameState(
            level_id=level_id,
            level_name=level_name,
            birds_waiting=birds_waiting,
            birds_in_flight=[],
            pigs=pigs,
            objects=objects,
            score=0,
            dragging=False,
            flying=False,
            won=False,
            lost=False,
            drag_point=None,
            trajectory=[],
            stars=level.stars,
            builder_mode=builder_mode,
            builder_playing=builder_playing,
            builder_menu="main",
            builder_menu_stack=[],
            dragging_palette_item=None,
            builder_mouse=(0, 0),
        )

    def _serialize_builder_state(self) -> LevelSpec:
        return LevelSpec(
            level_id="builder",
            name="Builder Mode",
            birds=[bird.bird_type for bird in self.state.birds_waiting],
            pigs=[
                {"x": pig.x, "y": pig.y, "angle": pig.angle}
                for pig in self.state.pigs
            ],
            objects=[
                {
                    "kind": obj.kind,
                    "x": obj.x,
                    "y": obj.y,
                    "angle": obj.angle,
                    "material": obj.material,
                }
                for obj in self.state.objects
            ],
            stars=(0, 0, 0),
        )

    def _clone_level_spec(self, level: LevelSpec) -> LevelSpec:
        return LevelSpec(
            level_id=level.level_id,
            name=level.name,
            birds=list(level.birds),
            pigs=[dict(pig) for pig in level.pigs],
            objects=[dict(obj) for obj in level.objects],
            stars=tuple(level.stars),
        )

    def export_builder_level(
        self,
        *,
        name: str = "Custom Builder Level",
        level_id: str = "builder_saved",
        stars: tuple[int, int, int] = (500, 1000, 1500),
    ) -> LevelSpec:
        if self.state.builder_mode and self.state.builder_playing and self.builder_blueprint:
            base_level = self.builder_blueprint
        else:
            base_level = self._serialize_builder_state()

        exported_stars = stars
        if any(base_level.stars):
            exported_stars = tuple(base_level.stars)

        return LevelSpec(
            level_id=level_id,
            name=name,
            birds=list(base_level.birds),
            pigs=[dict(pig) for pig in base_level.pigs],
            objects=[dict(obj) for obj in base_level.objects],
            stars=exported_stars,
        )

    def save_builder_level(
        self,
        path: str | Path = DEFAULT_BUILDER_LEVEL_PATH,
        *,
        name: str = "Custom Builder Level",
        level_id: str = "builder_saved",
    ) -> LevelSpec:
        level = self.export_builder_level(name=name, level_id=level_id)
        save_level(level, path)
        self.current_builder_save_path = Path(path)
        return level

    def save_builder_level_to_next_slot(
        self, *, name: Optional[str] = None
    ) -> tuple[LevelSpec, Path]:
        path, slot_number = next_builder_save_path()
        level = self.save_builder_level(
            path,
            name=name or f"Builder Level {slot_number:02d}",
            level_id=f"builder_level_{slot_number:02d}",
        )
        return level, path

    def replace_current_builder_level(self, *, name: str) -> tuple[LevelSpec, Path]:
        if self.current_builder_save_path is None:
            return self.save_builder_level_to_next_slot(name=name)

        level_id = self.current_builder_save_path.stem
        level = self.save_builder_level(
            self.current_builder_save_path,
            name=name,
            level_id=level_id,
        )
        return level, self.current_builder_save_path

    def load_builder_level(self, path=DEFAULT_BUILDER_LEVEL_PATH) -> LevelSpec:
        level = load_level_file(path)
        self.current_builder_save_path = Path(path)
        self.builder_blueprint = self._clone_level_spec(level)
        self.state = self._state_from_spec(
            self.builder_blueprint, builder_mode=True, builder_playing=False
        )
        return self._clone_level_spec(level)

    def start_level(self, level_id: str) -> None:
        level = self.levels[level_id]
        self.builder_blueprint = None
        self.current_builder_save_path = None
        self.state = self._state_from_spec(level)
        self._settle_world()

    def start_builder(self) -> None:
        self.builder_blueprint = None
        self.current_builder_save_path = None
        self.state = GameState(
            level_id="builder",
            level_name="Builder Mode",
            stars=(0, 0, 0),
            builder_mode=True,
            builder_playing=False,
            builder_menu="main",
            builder_menu_stack=[],
            dragging_palette_item=None,
            builder_mouse=(0, 0),
        )

    def reset_level(self) -> None:
        if self.state.level_id is not None:
            self.start_level(self.state.level_id)

    def clear_builder_world(self) -> None:
        if not self.state.builder_mode:
            return
        self.state.pigs = []
        self.state.objects = []
        self.state.dragging_palette_item = None

    def clear_builder_birds(self) -> None:
        if not self.state.builder_mode:
            return
        self.state.birds_waiting = []
        self.state.birds_in_flight = []
        self.state.dragging = False
        self.state.flying = False
        self.state.trajectory = []

    def add_builder_bird(self, bird_type: str) -> None:
        if not self.state.builder_mode or self.state.builder_playing:
            return
        index = len(self.state.birds_waiting)
        if index == 0:
            x, y = INIT_BIRD_X, INIT_BIRD_Y
        else:
            x, y = INIT_BIRD_X - 50 * index, FLOOR_Y - 20
        self.state.birds_waiting.append(BirdState(bird_type=bird_type, x=x, y=y))

    def push_builder_menu(self, menu_name: str) -> None:
        if not self.state.builder_mode or self.state.builder_playing:
            return
        self.state.builder_menu_stack.append(self.state.builder_menu)
        self.state.builder_menu = menu_name

    def pop_builder_menu(self) -> None:
        if not self.state.builder_mode or self.state.builder_playing:
            return
        if self.state.builder_menu_stack:
            self.state.builder_menu = self.state.builder_menu_stack.pop()

    def set_builder_mouse(self, mouse_x: float, mouse_y: float) -> None:
        if not self.state.builder_mode:
            return
        self.state.builder_mouse = (mouse_x, mouse_y)

    def begin_palette_drag(self, item_key: str) -> None:
        if not self.state.builder_mode or self.state.builder_playing:
            return
        self.state.dragging_palette_item = item_key

    def finish_palette_drag(self) -> None:
        if not self.state.builder_mode:
            return
        self.state.dragging_palette_item = None

    def place_builder_item(self, item_key: str, x: float, y: float) -> bool:
        if not self.state.builder_mode or self.state.builder_playing:
            return False

        if item_key == "pig1":
            if y >= FLOOR_Y - 30:
                return False
            self.state.pigs.append(
                BodyState(kind="pig", x=x, y=y, angle=0, material="flesh")
            )
            return True

        item_map = {
            "wood_box": ("box", "wood"),
            "stone_box": ("box", "stone"),
            "wood_wheel": ("wheel", "wood"),
            "stone_wheel": ("wheel", "stone"),
            "wood_column": ("column", "wood"),
            "stone_column": ("column", "stone"),
        }
        if item_key not in item_map:
            return False

        kind, material = item_map[item_key]
        body = BodyState(kind=kind, x=x, y=y, angle=0, material=material)
        if y >= FLOOR_Y - body.height / 2:
            return False
        self.state.objects.append(body)
        return True

    def begin_builder_play(self) -> None:
        if not self.state.builder_mode or self.state.builder_playing:
            return
        self.builder_blueprint = self._serialize_builder_state()
        self.state = self._state_from_spec(
            self.builder_blueprint, builder_mode=True, builder_playing=True
        )
        self._settle_world()

    def restart_builder_play(self) -> None:
        if self.builder_blueprint is None:
            return
        self.state = self._state_from_spec(
            self.builder_blueprint, builder_mode=True, builder_playing=True
        )
        self._settle_world()

    def restore_builder_editor(self) -> None:
        if self.builder_blueprint is None:
            self.start_builder()
            return
        self.state = self._state_from_spec(
            self.builder_blueprint, builder_mode=True, builder_playing=False
        )

    def begin_drag(self, mouse_x: float, mouse_y: float) -> bool:
        if (
            not self.state.level_id
            or not self.state.birds_waiting
            or self.state.flying
            or self.state.won
            or self.state.lost
        ):
            return False

        if distance(INIT_BIRD_X, INIT_BIRD_Y, mouse_x, mouse_y) < 50:
            self.state.dragging = True
            self.state.drag_point = (mouse_x, mouse_y)
            return True
        return False

    def update_drag(self, mouse_x: float, mouse_y: float) -> None:
        if not self.state.dragging or not self.state.birds_waiting:
            return

        bird = self.state.birds_waiting[0]
        self.state.trajectory = []

        dx = mouse_x - INIT_BIRD_X
        dy = mouse_y - INIT_BIRD_Y
        drag_distance = (dx**2 + dy**2) ** 0.5
        if drag_distance <= SLING_MAX:
            bird.x = mouse_x
            bird.y = mouse_y
        elif drag_distance != 0:
            scale = SLING_MAX / drag_distance
            bird.x = INIT_BIRD_X + dx * scale
            bird.y = INIT_BIRD_Y + dy * scale

        self.state.drag_point = (bird.x, bird.y)
        bird.trajectory = bird.generate_trajectory(
            INIT_BIRD_X, INIT_BIRD_Y, dt=TRAJECTORY_DT
        )
        self.state.trajectory = list(bird.trajectory)

    def release_bird(self) -> None:
        if (
            not self.state.dragging
            or not self.state.birds_waiting
            or self.state.won
            or self.state.lost
        ):
            return

        self.state.dragging = False
        self.state.flying = True
        bird = self.state.birds_waiting.pop(0)
        bird.trajectory = bird.generate_trajectory(
            INIT_BIRD_X, INIT_BIRD_Y, dt=TRAJECTORY_DT
        )
        self.state.birds_in_flight.append(bird)
        self.state.trajectory = []
        self.state.score -= 200

    def activate_ability(self) -> None:
        if not self.state.birds_in_flight or not self.state.flying:
            return

        bird = self.state.birds_in_flight[-1]
        if bird.bird_type == "yellow" and not bird.ability_used:
            filtered_points: list[tuple[float, float, float]] = []
            for index, point in enumerate(bird.trajectory):
                if index % 5 == 0:
                    filtered_points.append(point)
            bird.trajectory = filtered_points
            bird.ability_used = True
        elif bird.bird_type == "blue" and not bird.ability_used:
            center_points = list(bird.trajectory)
            upper_points = self._build_split_trajectory(
                center_points,
                origin_x=bird.x,
                origin_y=bird.y,
                side=-1,
            )
            lower_points = self._build_split_trajectory(
                center_points,
                origin_x=bird.x,
                origin_y=bird.y,
                side=1,
            )

            upper_bird = BirdState(
                bird_type="blue",
                x=bird.x,
                y=bird.y,
                velocity_x=bird.velocity_x * 1.06,
                velocity_y=bird.velocity_y - 8,
                velocity_t=bird.velocity_t,
                grounded=False,
                weight=0.3,
                ability_used=True,
                trajectory=upper_points,
            )
            lower_bird = BirdState(
                bird_type="blue",
                x=bird.x,
                y=bird.y,
                velocity_x=bird.velocity_x * 1.06,
                velocity_y=bird.velocity_y + 8,
                velocity_t=bird.velocity_t,
                grounded=False,
                weight=0.3,
                ability_used=True,
                trajectory=lower_points,
            )
            bird.weight = 0.3
            bird.trajectory = center_points
            bird.ability_used = True
            self.state.birds_in_flight.extend([upper_bird, lower_bird])
        elif bird.bird_type == "eagle" and not bird.ability_used:
            redirected_points: list[tuple[float, float, float]] = []
            start_x = bird.x
            start_y = bird.y
            for index, (_x, _y, velocity_t) in enumerate(bird.trajectory):
                redirected_points.append(
                    (
                        start_x,
                        min(FLOOR_Y - 30, start_y + 18 + index * 22),
                        velocity_t * 1.55,
                    )
                )
            bird.trajectory = redirected_points
            bird.velocity_x = 0
            bird.velocity_y = max(abs(bird.velocity_y), 18)
            bird.ability_used = True

    def _build_split_trajectory(
        self,
        center_points: list[tuple[float, float, float]],
        *,
        origin_x: float,
        origin_y: float,
        side: int,
    ) -> list[tuple[float, float, float]]:
        split_points: list[tuple[float, float, float]] = []
        last_dir_x = 1.0
        last_dir_y = 0.0

        for index, (x, y, velocity_t) in enumerate(center_points):
            if index + 1 < len(center_points):
                dir_x = center_points[index + 1][0] - x
                dir_y = center_points[index + 1][1] - y
            else:
                dir_x = x - origin_x
                dir_y = y - origin_y

            direction_length = (dir_x**2 + dir_y**2) ** 0.5
            if direction_length > 0.001:
                last_dir_x = dir_x / direction_length
                last_dir_y = dir_y / direction_length

            normal_x = -last_dir_y
            normal_y = last_dir_x
            lateral_offset = min(120, 18 + index * 4.5)
            forward_offset = min(26, index * 0.8)
            split_x = x + normal_x * lateral_offset * side + last_dir_x * forward_offset
            split_y = y + normal_y * lateral_offset * side + last_dir_y * forward_offset
            split_y = min(FLOOR_Y - 30, max(0, split_y))
            split_points.append((split_x, split_y, velocity_t * 0.88))

        return split_points

    def tick(self) -> None:
        if not self.state.level_id:
            return

        if not self.state.pigs:
            self.state.won = True
            self.state.birds_in_flight = []
            self.state.flying = False
        elif not self.state.birds_waiting and not self.state.flying and self.state.pigs:
            moving_count = sum(1 for pig in self.state.pigs if pig.velocity_y > 0)
            moving_count += sum(
                1
                for obj in self.state.objects
                if obj.velocity_x != 0 or obj.is_rotating
            )
            if moving_count == 0:
                self.state.lost = True
                self.state.birds_in_flight = []

        if self.state.won or self.state.lost:
            self.state.dragging = False

        step_dt = SIMULATION_DT / PHYSICS_SUBSTEPS
        for _ in range(PHYSICS_SUBSTEPS):
            if self.state.flying:
                if self.state.birds_in_flight:
                    for bird in list(self.state.birds_in_flight):
                        self._advance_bird(bird)
                else:
                    self._shift_waiting_birds()

            for active_bird in list(self.state.birds_in_flight):
                for pig in list(self.state.pigs):
                    self._resolve_collision(pig, active_bird)
                for obj in list(self.state.objects):
                    self._resolve_collision(obj, active_bird)
            self._simulate_environment_step(step_dt)

    def _advance_bird(self, bird: BirdState) -> None:
        if not bird.trajectory:
            bird.velocity_t = 0
            self._remove_flying_bird(bird)
            return
        if bird.grounded:
            bird.y = bird.floor
            bird.trajectory = []
            self._remove_flying_bird(bird)
            return

        bird.x, bird.y, velocity_t = bird.trajectory.pop(0)
        if bird.bird_type == "yellow" and bird.ability_used:
            bird.velocity_t = velocity_t * 10
            bird.velocity_x *= 2
            bird.velocity_y *= 2
        elif bird.bird_type == "eagle" and bird.ability_used:
            bird.velocity_t = velocity_t * 2
            bird.velocity_x = 0
            bird.velocity_y = max(abs(bird.velocity_y), 18)
        else:
            bird.velocity_t = velocity_t

    def _shift_waiting_birds(self) -> None:
        self.state.flying = False
        for index, bird in enumerate(self.state.birds_waiting):
            if index == 0:
                bird.x = INIT_BIRD_X
                bird.y = INIT_BIRD_Y
            else:
                bird.x = INIT_BIRD_X - 50 * index
                bird.y = FLOOR_Y - 20

    def _remove_flying_bird(self, bird: BirdState) -> None:
        if bird in self.state.birds_in_flight:
            self.state.birds_in_flight.remove(bird)
        if not self.state.birds_in_flight:
            self.state.trajectory = []
            self._shift_waiting_birds()

    def _stabilize_box_supports(self) -> None:
        for obj in self.state.objects:
            if obj.kind == "box":
                self._apply_box_support(obj)

    def _settle_world(self, steps: int = 40) -> None:
        step_dt = SIMULATION_DT / PHYSICS_SUBSTEPS
        for _ in range(steps):
            self._simulate_environment_step(step_dt)

    def _simulate_environment_step(self, step_dt: float) -> None:
        if self.state.pigs and self.state.objects:
            for pig in list(self.state.pigs):
                collision_count = 0
                for obj in list(self.state.objects):
                    if self._resolve_collision(pig, obj):
                        collision_count += 1
                if collision_count < 1:
                    pig.grounded = False
                    pig.floor = FLOOR_Y

        if len(self.state.objects) > 1:
            for object1 in list(self.state.objects):
                collision_count = 0
                for object2 in list(self.state.objects):
                    if object1 is object2:
                        continue
                    if (
                        self._resolve_collision(object1, object2)
                        and object1.y < object2.y
                    ):
                        collision_count += 1
                if collision_count < 1:
                    object1.grounded = False
                    object1.floor = FLOOR_Y
        else:
            for object1 in self.state.objects:
                object1.grounded = False
                object1.floor = FLOOR_Y

        for obj in self.state.objects:
            if obj.is_rotating:
                obj.rotate(obj.rotate_info[0], obj.rotate_info[1])
            obj.move(step_dt)

        for pig in self.state.pigs:
            pig.obey_gravity(step_dt)
        for obj in self.state.objects:
            obj.obey_gravity(step_dt)
            obj.spin_wheel()

        self._resolve_persistent_overlaps()
        self._stabilize_box_supports()

    def _apply_box_support(self, box: BodyState) -> None:
        box_bottom = box.y + box.height / 2
        supports: list[tuple[BodyState, float, float, float]] = []

        for support in self.state.objects:
            if support is box:
                continue
            support_profile = self._support_profile(support)
            if support_profile is None:
                continue

            support_top, support_half_width = support_profile
            if abs(box_bottom - support_top) > 18:
                continue

            overlap_left = max(box.x - box.width / 2, support.x - support_half_width)
            overlap_right = min(box.x + box.width / 2, support.x + support_half_width)
            if overlap_right - overlap_left < 8:
                continue

            supports.append((support, support_top, overlap_left, overlap_right))

        if not supports:
            box.grounded = False
            box.floor = FLOOR_Y
            return

        best_top = min(support[1] for support in supports)
        active_supports = [
            support for support in supports if abs(support[1] - best_top) <= 8
        ]
        left_edge = min(support[2] for support in active_supports)
        right_edge = max(support[3] for support in active_supports)
        support_center = (left_edge + right_edge) / 2
        support_span = right_edge - left_edge
        wheel_support = any(support[0].kind == "wheel" for support in active_supports)
        stable_offset = (
            min(6, support_span * 0.25)
            if wheel_support
            else max(8, support_span * 0.35)
        )

        if abs(box.x - support_center) <= stable_offset:
            box.floor = best_top
            box.grounded = True
            box.y = min(box.y, best_top - box.height / 2)
            if len(active_supports) == 1 and active_supports[0][0].kind == "wheel":
                box.velocity_x += active_supports[0][0].velocity_x * 0.15
            return

        self._apply_unstable_support_response(
            box, support_center, wheel_support=wheel_support
        )

    def _support_profile(self, support: BodyState) -> Optional[tuple[float, float]]:
        if support.kind == "box":
            if abs(support.angle) > 10:
                return None
            return support.y - support.height / 2, max(12, support.width / 2 - 6)

        if support.kind == "column":
            if support.is_rotating or abs(support.angle) > 10:
                return None
            return support.y - support.height / 2, max(8, support.width / 2)

        if support.kind == "wheel":
            return support.y - support.height / 2 + 8, 10

        return None

    def _support_balance_offset(
        self, support_span: float, *, wheel_support: bool
    ) -> float:
        if wheel_support:
            return min(6, support_span * 0.25)
        return max(8, support_span * 0.35)

    def _apply_unstable_support_response(
        self, box: BodyState, support_center: float, *, wheel_support: bool
    ) -> None:
        box.grounded = False
        box.floor = FLOOR_Y
        slip_direction = -1 if box.x < support_center else 1
        target_slide = 6 if wheel_support else 3
        if abs(box.velocity_x) < target_slide:
            box.velocity_x = slip_direction * target_slide
        else:
            box.velocity_x += slip_direction * 1.2
        if wheel_support:
            box.x += slip_direction * 3
            if box.velocity_y < 6:
                box.velocity_y = 6
        elif box.velocity_y < 2:
            box.velocity_y = 2

    def _box_support_contact(
        self, box: BodyState, support: BodyState
    ) -> Optional[tuple[bool, float, float, bool]]:
        support_profile = self._support_profile(support)
        if support_profile is None:
            return None

        support_top, support_half_width = support_profile
        overlap_left = max(box.x - box.width / 2, support.x - support_half_width)
        overlap_right = min(box.x + box.width / 2, support.x + support_half_width)
        support_span = overlap_right - overlap_left
        if support_span < 8:
            return None

        wheel_support = support.kind == "wheel"
        stable_offset = self._support_balance_offset(
            support_span, wheel_support=wheel_support
        )
        stable = abs(box.x - support.x) <= stable_offset
        return stable, support_top, support.x, wheel_support

    def _unstable_support_pair(
        self, body: BodyState, other: BodyState
    ) -> Optional[tuple[BodyState, BodyState, float, bool]]:
        if body.kind == "box" and other.kind in {"box", "column", "wheel"}:
            top_box, support = body, other
        elif other.kind == "box" and body.kind in {"box", "column", "wheel"}:
            top_box, support = other, body
        else:
            return None

        if top_box.y >= support.y:
            return None

        contact = self._box_support_contact(top_box, support)
        if contact is None:
            return top_box, support, support.x, support.kind == "wheel"

        stable, _, support_center, wheel_support = contact
        if stable:
            return None
        return top_box, support, support_center, wheel_support

    def _separate_from_support(
        self,
        top_box: BodyState,
        support: BodyState,
        overlap_x: float,
        support_center: float,
    ) -> None:
        direction = -1 if top_box.x < support_center else 1
        top_box.x += direction * (overlap_x + 0.75)
        if support.kind == "wheel":
            top_box.velocity_x = direction * max(abs(top_box.velocity_x), 4)
        else:
            top_box.velocity_x = direction * max(abs(top_box.velocity_x), 2.5)

    def _body_half_extents(self, body: BodyState) -> tuple[float, float]:
        if body.kind == "column" and body.angle != 0:
            return body.angle_width / 2, body.angle_height / 2
        return body.width / 2, body.height / 2

    def _resolve_persistent_overlaps(self) -> None:
        for index, body in enumerate(self.state.objects):
            for other in self.state.objects[index + 1 :]:
                half_w1, half_h1 = self._body_half_extents(body)
                half_w2, half_h2 = self._body_half_extents(other)
                dx = other.x - body.x
                dy = other.y - body.y
                overlap_x = half_w1 + half_w2 - abs(dx)
                overlap_y = half_h1 + half_h2 - abs(dy)

                if overlap_x <= 0 or overlap_y <= 0:
                    continue

                if overlap_y <= overlap_x:
                    unstable_pair = self._unstable_support_pair(body, other)
                    if unstable_pair is not None:
                        top_box, support, support_center, wheel_support = unstable_pair
                        self._separate_from_support(
                            top_box, support, overlap_x, support_center
                        )
                        self._apply_unstable_support_response(
                            top_box,
                            support_center,
                            wheel_support=wheel_support,
                        )
                        continue
                    self._separate_vertically(body, other, overlap_y)
                else:
                    self._separate_horizontally(body, other, overlap_x)

    def _separate_vertically(
        self, body: BodyState, other: BodyState, overlap_y: float
    ) -> None:
        if body.y <= other.y:
            top_body, bottom_body = body, other
        else:
            top_body, bottom_body = other, body

        top_half_h = self._body_half_extents(top_body)[1]
        bottom_half_h = self._body_half_extents(bottom_body)[1]
        separation = overlap_y + 0.5

        top_body.y -= separation
        top_body.floor = min(top_body.floor, bottom_body.y - bottom_half_h)
        top_body.grounded = True
        top_body.velocity_y = min(top_body.velocity_y, 0)
        bottom_body.velocity_y = max(bottom_body.velocity_y, 0)

    def _separate_horizontally(
        self, body: BodyState, other: BodyState, overlap_x: float
    ) -> None:
        direction = -1 if body.x <= other.x else 1
        separation = overlap_x / 2 + 0.5
        body.x -= direction * separation
        other.x += direction * separation
        body.velocity_x *= 0.7
        other.velocity_x *= 0.7

    def _resolve_collision(
        self, body: BodyState, other: Union[BirdState, BodyState]
    ) -> bool:
        if isinstance(other, BirdState):
            return self._resolve_bird_collision(body, other)
        return self._resolve_body_collision(body, other)

    def _resolve_bird_collision(self, body: BodyState, bird: BirdState) -> bool:
        if body.kind == "pig" and distance(body.x, body.y, bird.x, bird.y) < 60:
            if body in self.state.pigs:
                self.state.pigs.remove(body)
                self.state.score += 500
            return True

        if body.kind == "box":
            if abs(body.x - bird.x) <= 30 + body.width / 2 and abs(body.y - bird.y) <= 30 + body.height / 2:
                if (
                    bird.x <= body.x - body.width / 2
                    or body.x + body.width / 2 <= bird.x
                ) and bird.velocity_t != 0:
                    body.velocity_x += bird.velocity_x / body.weight
                    bird.velocity_x -= body.hp * abs(bird.velocity_x / bird.velocity_t)
                    if bird.velocity_x < 0:
                        bird.velocity_x = 0
                elif (
                    bird.y <= body.y - body.height / 2
                    or body.y + body.height / 2 <= bird.y
                ) and bird.velocity_t != 0:
                    body.velocity_y -= bird.velocity_y / body.weight
                    bird.velocity_y -= body.hp * abs(bird.velocity_y / bird.velocity_t)
                    if bird.velocity_y < 0:
                        bird.velocity_y = 0
                body.hp, bird.velocity_t = body.hp - bird.velocity_t, bird.velocity_t - body.hp
                if bird.velocity_t < 0:
                    bird.velocity_t = 0
                if body.hp <= 0:
                    if body in self.state.objects:
                        self.state.objects.remove(body)
                        self.state.score += 100
                else:
                    self._remove_flying_bird(bird)
                return True

        if body.kind == "column":
            if abs(body.x - bird.x) <= 30 + body.width / 2 and abs(body.y - bird.y) <= 30 + body.height / 2:
                if body.angle == 0:
                    if bird.y > body.y:
                        body.is_rotating = True
                        body.rotate_info = (-5, -90)
                    elif bird.y < body.y:
                        body.is_rotating = True
                        body.rotate_info = (5, 90)
                    body.velocity_x += bird.velocity_x / body.weight
                    if bird.velocity_t != 0:
                        bird.velocity_x -= body.hp * abs(bird.velocity_x / bird.velocity_t)
                        bird.velocity_y -= body.hp * abs(bird.velocity_y / bird.velocity_t)
                body.hp -= bird.velocity_t
                if body.hp <= 0:
                    if body in self.state.objects:
                        self.state.objects.remove(body)
                        self.state.score += 100
                else:
                    self._remove_flying_bird(bird)
                return True

        if body.kind == "wheel":
            if abs(body.x - bird.x) <= 30 + body.width / 2 and abs(body.y - bird.y) <= 30 + body.height / 2:
                body.velocity_x += bird.velocity_x / body.weight
                if bird.velocity_t != 0:
                    bird.velocity_x -= body.hp * abs(bird.velocity_x / bird.velocity_t)
                    if bird.velocity_x < 0:
                        bird.velocity_x = 0
                    body.velocity_y -= bird.velocity_y / body.weight
                    bird.velocity_y -= body.hp * abs(bird.velocity_y / bird.velocity_t)
                if bird.velocity_y < 0:
                    bird.velocity_y = 0
                body.hp, bird.velocity_t = body.hp - bird.velocity_t, bird.velocity_t - body.hp
                if bird.velocity_t < 0:
                    bird.velocity_t = 0
                if body.hp <= 0:
                    if body in self.state.objects:
                        self.state.objects.remove(body)
                        self.state.score += 100
                else:
                    self._remove_flying_bird(bird)
                return True

        return False

    def _resolve_body_collision(self, body: BodyState, other: BodyState) -> bool:
        if body.kind == "pig":
            return self._resolve_pig_collision(body, other)
        if body.kind == "box":
            return self._resolve_box_collision(body, other)
        if body.kind == "column":
            return self._resolve_column_collision(body, other)
        if body.kind == "wheel":
            return self._resolve_wheel_collision(body, other)
        return False

    def _resolve_pig_collision(self, pig: BodyState, other: BodyState) -> bool:
        if other.kind == "box":
            if abs(other.x - pig.x) <= 30 + other.width / 2 and abs(other.y - pig.y) <= 30 + other.height / 2:
                if pig.y < other.y:
                    pig.floor = other.y - other.height / 2
                    pig.grounded = True
                elif pig.y > other.y and pig in self.state.pigs:
                    self.state.pigs.remove(pig)
                    self.state.score += 500
                return True

        if other.kind == "column":
            if other.is_rotating:
                floor_point = (
                    other.x
                    - (other.height / 2 * abs(math.sin(math.radians(other.angle))))
                    + other.width / 2 * abs(math.cos(math.radians(other.angle)))
                )
                if abs(pig.x - floor_point) <= other.height + 30:
                    x_collision = floor_point + (pig.x - floor_point) * abs(
                        math.sin(math.radians(other.angle))
                    )
                    y_collision = other.y - (
                        pig.x - floor_point - other.height / 2
                    ) * abs(math.cos(math.radians(other.angle)))
                    if abs(distance(x_collision, y_collision, pig.x, pig.y)) < other.width / 2 + 30:
                        if y_collision < pig.y and pig in self.state.pigs:
                            self.state.pigs.remove(pig)
                            self.state.score += 500
                        return True
            elif other.angle == 0:
                if abs(other.x - pig.x) <= 30 + other.width / 2 and abs(other.y - pig.y) <= 30 + other.height / 2:
                    if pig.y < other.y:
                        pig.floor = other.y - other.height / 2
                        pig.grounded = True
                    elif pig.y > other.y and pig in self.state.pigs:
                        self.state.pigs.remove(pig)
                        self.state.score += 500
                    return True
            else:
                if abs(other.x - pig.x) <= pig.width / 2 + other.angle_width / 2 and abs(other.y - pig.y) <= pig.height / 2 + other.angle_height / 2:
                    if pig.y + pig.height / 2 <= other.y - (other.angle_height / 2 - pig.velocity_y / 3):
                        pig.floor = other.y - other.angle_height / 2
                        pig.grounded = True
                    return True

        if other.kind == "wheel":
            if abs(other.x - pig.x) <= 30 + other.width / 2 and abs(other.y - pig.y) <= 30 + other.height / 2:
                if pig.y > other.y and pig in self.state.pigs:
                    self.state.pigs.remove(pig)
                    self.state.score += 500
                    return True
                if pig.x < other.x:
                    other.velocity_x += pig.velocity_y / 10
                    pig.velocity_y -= pig.velocity_y / 10
                else:
                    other.velocity_x -= pig.velocity_y / 10
                    pig.velocity_y -= pig.velocity_y / 10
                return True
        return False

    def _resolve_box_collision(self, box: BodyState, other: BodyState) -> bool:
        if other.kind == "box":
            if abs(other.x - box.x) <= box.width / 2 + other.width / 2 and abs(other.y - box.y) <= box.height / 2 + other.height / 2:
                if box.y + box.height / 2 <= other.y - (other.height / 2 - box.velocity_y / 3):
                    contact = self._box_support_contact(box, other)
                    if contact is None:
                        return False
                    box.velocity_y = min(box.velocity_y, 0)
                else:
                    if box.x <= other.x - other.width / 2 + box.velocity_x - box.width / 2:
                        new_velocity = (box.velocity_x + other.velocity_x) / (box.weight + other.weight)
                        box.velocity_x = new_velocity
                        other.velocity_x = new_velocity
                        box.x = other.x - other.width / 2 - box.width / 2 - 1
                return True

        if other.kind == "column":
            if other.angle == 0:
                if abs(other.x - box.x) <= box.width / 2 + other.width / 2 and abs(other.y - box.y) <= box.height / 2 + other.height / 2:
                    if box.y + box.height / 2 <= other.y - (other.height / 2 - box.velocity_y / 3):
                        contact = self._box_support_contact(box, other)
                        if contact is None:
                            return False
                        box.velocity_y = min(box.velocity_y, 0)
                    else:
                        if box.x <= other.x - other.width / 2 + box.velocity_x - box.width / 2:
                            new_velocity = (box.velocity_x + other.velocity_x) / (box.weight + other.weight)
                            box.velocity_x = new_velocity
                            other.velocity_x = new_velocity
                            box.x = other.x - other.width / 2 - box.width / 2 - 1
                    return True
            else:
                if abs(other.x - box.x) <= box.width / 2 + other.angle_width / 2 and abs(other.y - box.y) <= box.height / 2 + other.angle_height / 2:
                    if box.y + box.height / 2 <= other.y - (other.angle_height / 2 - box.velocity_y / 3):
                        contact = self._box_support_contact(box, other)
                        if contact is None:
                            return False
                        box.velocity_y = min(box.velocity_y, 0)
                    else:
                        if box.x <= other.x - other.angle_width / 2 + box.velocity_x - box.width / 2:
                            new_velocity = (box.velocity_x + other.velocity_x) / (box.weight + other.weight)
                            box.velocity_x = new_velocity
                            other.velocity_x = new_velocity
                            box.x = other.x - other.angle_width / 2 - box.width / 2 - 1
                    return True

        if other.kind == "wheel":
            if abs(other.x - box.x) <= box.width / 2 + other.angle_width / 2 and abs(other.y - box.y) <= box.height / 2 + other.angle_height / 2:
                if box.y < other.y:
                    contact = self._box_support_contact(box, other)
                    if contact is None:
                        return False
                    if contact[0]:
                        if box.x < other.x:
                            other.velocity_x += box.velocity_y / 10
                            box.velocity_y -= box.velocity_y / 10
                        elif box.x > other.x:
                            other.velocity_x -= box.velocity_y / 10
                            box.velocity_y -= box.velocity_y / 10
                    else:
                        box.velocity_y = min(box.velocity_y, 0)
                return True
        return False

    def _resolve_column_collision(self, column: BodyState, other: BodyState) -> bool:
        if other.kind not in {"column", "box"}:
            return False

        if column.angle == 0:
            other_width = other.width
            other_height = other.height
        else:
            other_width = other.angle_width
            other_height = other.angle_height

        if other.kind == "column" and other.angle != 0:
            other_width = other.angle_width
            other_height = other.angle_height

        if other.kind == "box" and column.angle == 0:
            hit = (
                abs(other.x - column.x) <= column.width / 2 + other.width / 2
                and abs(other.y - column.y) <= column.height / 2 + other.height / 2
            )
        else:
            hit = (
                abs(other.x - column.x) <= column.width / 2 + other_width / 2
                and abs(other.y - column.y) <= column.height / 2 + other_height / 2
            )

        if not hit:
            return False

        if column.angle == 0:
            if column.y + column.height / 2 <= other.y - (other_height / 2 - column.velocity_y / 3):
                column.floor = other.y - other_height / 2
                column.grounded = True
            else:
                if column.x <= other.x - other_width / 2 + column.velocity_x - column.width / 2:
                    new_velocity = (column.velocity_x + other.velocity_x) / (column.weight + other.weight)
                    column.velocity_x = new_velocity
                    other.velocity_x = new_velocity
                    column.x = other.x - other_width / 2 - column.width / 2 - 1
            return True

        if column.y + column.height / 2 <= other.y - (other_height / 2 - column.velocity_y / 3):
            column.floor = other.y - other_height / 2
            column.grounded = True
        else:
            if column.x <= other.x - other_width / 2 + column.velocity_x - column.width / 2:
                new_velocity = (column.velocity_x + other.velocity_x) / (column.weight + other.weight)
                column.velocity_x = new_velocity
                other.velocity_x = new_velocity
                column.x = other.x - other_width / 2 - column.width / 2 - 1
        return True

    def _resolve_wheel_collision(self, wheel: BodyState, other: BodyState) -> bool:
        if other.kind == "wheel":
            if abs(other.x - wheel.x) <= wheel.width / 2 + other.width / 2 and abs(other.y - wheel.y) <= wheel.height / 2 + other.height / 2:
                if wheel.x < other.x and abs(wheel.y - other.y) < other.height / 2:
                    wheel.x = other.x - other.width / 2 - wheel.width / 2
                    new_velocity = (wheel.velocity_x + other.velocity_x) / 2
                    wheel.velocity_x = new_velocity
                    other.velocity_x = new_velocity
                elif wheel.x > other.x and abs(wheel.y - other.y) < other.height / 2:
                    wheel.x = other.x + other.width / 2 + wheel.width / 2
                    new_velocity = (wheel.velocity_x + other.velocity_x) / 2
                    wheel.velocity_x = new_velocity
                    other.velocity_x = new_velocity
                return True

        if other.kind == "box":
            if abs(other.x - wheel.x) <= wheel.width / 2 + other.width / 2 and abs(other.y - wheel.y) <= wheel.height / 2 + other.height / 2:
                if wheel.x < other.x and abs(wheel.y - other.y) < other.height / 2:
                    wheel.x = other.x - other.width / 2 - wheel.width / 2 - 1
                    new_velocity = (wheel.velocity_x + other.velocity_x) / 2
                    wheel.velocity_x = new_velocity
                    other.velocity_x = new_velocity
                elif wheel.x > other.x and abs(wheel.y - other.y) < other.height / 2:
                    wheel.x = other.x + other.width / 2 + wheel.width / 2 + 1
                    new_velocity = (wheel.velocity_x + other.velocity_x) / 2
                    wheel.velocity_x = new_velocity
                    other.velocity_x = new_velocity
                elif wheel.y < other.y and abs(wheel.x - other.x) < other.width / 2 + wheel.width / 2:
                    wheel.floor = other.y - other.height / 2
                    wheel.grounded = True
                    if wheel.x > other.x + other.width / 2:
                        wheel.velocity_x += wheel.velocity_y / 2
                    elif wheel.x < other.x - other.width / 2:
                        wheel.velocity_x -= wheel.velocity_y / 2
                return True
        return False
