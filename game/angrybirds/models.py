from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Optional, Tuple

from angrybirds.constants import FLOOR_Y, GRAVITY, SPRITE_SIZES


def sprite_key_for_body(kind: str, material: str) -> str:
    if kind == "pig":
        return "pig"
    if kind == "bird":
        return f"bird_{material}"
    return f"{kind}_{material}"


@dataclass
class BirdState:
    bird_type: str
    x: float
    y: float
    velocity_x: float = 0
    velocity_y: float = 0
    velocity_t: float = 0
    material: str = "bird"
    floor: float = FLOOR_Y
    grounded: bool = False
    weight: float = 0.5
    ability_used: bool = False
    trajectory: list[tuple[float, float, float]] = field(default_factory=list)

    @property
    def sprite_key(self) -> str:
        return sprite_key_for_body("bird", self.bird_type)

    def generate_trajectory(
        self,
        init_x: float,
        init_y: float,
        gravity: float = GRAVITY,
        floor_y: float = FLOOR_Y,
        dt: float = 1 / 3,
    ) -> list[tuple[float, float, float]]:
        self.velocity_x = init_x - self.x
        self.velocity_y = init_y - self.y
        t = 0.0
        velocity_t = self.velocity_t
        traj_x = self.x
        traj_y = self.y
        points: list[tuple[float, float, float]] = []

        while traj_y + 30 <= floor_y:
            points.append((traj_x, traj_y, velocity_t))
            t += dt
            traj_x = self.x + t * self.velocity_x
            traj_y = self.y + t * self.velocity_y + ((gravity / 2) * (t**2))
            velocity_t = (
                self.velocity_x**2 + (self.velocity_y + gravity * t) ** 2
            ) ** 0.5

        points.append((traj_x, floor_y - 30, velocity_t))
        return points

    @property
    def ability_name(self) -> str:
        if self.bird_type == "yellow":
            return "Speed Burst"
        if self.bird_type == "blue":
            return "Triple Split"
        if self.bird_type == "eagle":
            return "Sky Slam"
        return "Standard"

    @property
    def display_name(self) -> str:
        if self.bird_type == "blue":
            return "Blue Bird"
        if self.bird_type == "eagle":
            return "Mighty Eagle"
        return self.bird_type.title()


@dataclass
class BodyState:
    kind: str
    x: float
    y: float
    angle: float
    material: str
    weight: float = 1
    floor: float = FLOOR_Y
    hp: float = 100
    velocity_x: float = 0
    velocity_y: float = 0
    is_rotating: bool = False
    rotate_info: tuple[int, int] = (0, 0)
    rotate_count: int = 0
    elevation: float = 0
    grounded: bool = False
    friction: float = 10
    width: float = 0
    height: float = 0
    angle_width: float = 0
    angle_height: float = 0

    def __post_init__(self) -> None:
        if self.material == "flesh":
            self.hp = 50
            self.weight = 0.5
        elif self.material == "wood":
            self.hp = 100
            self.weight = 1
        elif self.material == "stone":
            self.hp = 500
            self.weight = 3

        if self.kind == "wheel":
            self.friction = 2

        sprite_key = self.sprite_key
        self.width, self.height = SPRITE_SIZES[sprite_key]
        self.angle_width = self.width
        self.angle_height = self.height

    @property
    def sprite_key(self) -> str:
        return sprite_key_for_body(self.kind, self.material)

    def obey_gravity(self, dt: float) -> None:
        if self.kind == "pig":
            if self.y < self.floor:
                if self.y + self.velocity_y * dt < self.floor - 30:
                    self.y += self.velocity_y * dt
                    self.velocity_y += GRAVITY * self.weight * dt
                else:
                    self.y = self.floor - 30
                    self.velocity_y = 0
            return

        if self.kind == "box":
            self.elevation = self.height / 2 + abs(
                (
                    (self.height / 2 * (2**0.5))
                    - self.height / 2
                )
                * math.sin(math.radians(2 * self.angle))
            )
        elif self.kind == "column":
            self.elevation = (self.width / 2) * abs(
                math.sin(math.radians(self.angle))
            ) + (self.height / 2) * abs(math.cos(math.radians(self.angle)))
        elif self.kind == "wheel":
            self.elevation = self.height / 2 + abs(
                (
                    (self.height / 2 * (2**0.5))
                    - self.height / 2
                )
                * math.sin(math.radians(2 * self.angle))
            )

        if self.y < self.floor:
            if self.y + self.velocity_y * dt < self.floor - self.elevation:
                self.y += self.velocity_y * dt
                self.velocity_y += GRAVITY * self.weight * dt
            else:
                self.y = self.floor - self.elevation
                self.velocity_y = GRAVITY

    def spin_wheel(self) -> None:
        if self.kind != "wheel":
            return
        if self.velocity_x > 0:
            self.angle += 3
        elif self.velocity_x < 0:
            self.angle -= 3
        else:
            self.angle = 0

    def rotate(self, rotate_speed: int, rotate_angle: int) -> None:
        if self.rotate_count == rotate_angle:
            self.is_rotating = False
            self.rotate_count = 0
            return

        self.angle += rotate_speed
        self.rotate_count += rotate_speed
        self.x += (
            self.height / 2 * math.sin(math.radians(self.angle))
            - self.height / 2 * math.sin(math.radians(self.angle - rotate_speed))
        )

        if self.kind == "column":
            self.angle_width = self.width * abs(math.cos(math.radians(self.angle))) + (
                self.height * abs(math.sin(math.radians(self.angle)))
            )
            self.angle_height = self.width * abs(math.sin(math.radians(self.angle))) + (
                self.height * abs(math.cos(math.radians(self.angle)))
            )

    def move(self, dt: float) -> None:
        self.x += self.velocity_x * dt
        if self.kind == "wheel":
            threshold = (self.friction * self.weight * dt) / 2
            if self.velocity_x > threshold:
                self.velocity_x -= threshold
            elif self.velocity_x < -threshold:
                self.velocity_x += threshold
            else:
                self.velocity_x = 0
            return

        threshold = self.friction * self.weight * dt
        if self.velocity_x > threshold:
            self.velocity_x -= threshold
        elif self.velocity_x < -threshold:
            self.velocity_x += threshold
        else:
            self.velocity_x = 0


@dataclass
class LevelSpec:
    level_id: str
    name: str
    birds: list[str]
    pigs: list[dict]
    objects: list[dict]
    stars: tuple[int, int, int]


@dataclass
class GameState:
    level_id: Optional[str] = None
    level_name: str = ""
    birds_waiting: list[BirdState] = field(default_factory=list)
    birds_in_flight: list[BirdState] = field(default_factory=list)
    pigs: list[BodyState] = field(default_factory=list)
    objects: list[BodyState] = field(default_factory=list)
    score: int = 0
    dragging: bool = False
    flying: bool = False
    won: bool = False
    lost: bool = False
    drag_point: Optional[Tuple[float, float]] = None
    trajectory: list[tuple[float, float, float]] = field(default_factory=list)
    stars: tuple[int, int, int] = (0, 0, 0)
    builder_mode: bool = False
    builder_playing: bool = False
    builder_menu: str = "main"
    builder_menu_stack: list[str] = field(default_factory=list)
    dragging_palette_item: Optional[str] = None
    builder_mouse: Tuple[float, float] = (0, 0)
