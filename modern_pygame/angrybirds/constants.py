import os
from pathlib import Path
import tempfile


ROOT_DIR = Path(__file__).resolve().parent.parent
ASSET_DIR = ROOT_DIR / "images"
LEVEL_DIR = ROOT_DIR / "levels"

RUNTIME_ROOT = Path(
    os.environ.get(
        "PHYSICS_GAME_HOME",
        str(Path(tempfile.gettempdir()) / "physics_game_engine"),
    )
)
DATA_DIR = RUNTIME_ROOT / "data"
SAVED_LEVEL_DIR = RUNTIME_ROOT / "saved_levels"
DEFAULT_BUILDER_LEVEL_PATH = SAVED_LEVEL_DIR / "builder_autosave.json"
DEFAULT_DATABASE_PATH = DATA_DIR / "physics_game.db"

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 900
TILE_SIZE = 50
FLOOR_Y = 700
GRAVITY = 9.81
FPS = 60
SIMULATION_DT = 1 / 3
PHYSICS_SUBSTEPS = 2
TRAJECTORY_DT = SIMULATION_DT / PHYSICS_SUBSTEPS

SLING_X = 200
SLING_Y = 600
SLING_MAX = 150
INIT_BIRD_X = SLING_X - 10
INIT_BIRD_Y = SLING_Y - 75

HOME_BUTTON_CENTER = (50, 50)
HOME_MENU_BUTTON_WIDTH = 340
HOME_MENU_BUTTON_HEIGHT = 110
HOME_MENU_TOP = 170
HOME_MENU_GAP = 120

SPRITE_PATHS = {
    "background": "background.png",
    "title": "Title.png",
    "home_button": "home_button.png",
    "back_button": "back_button.png",
    "sling": "sling.png",
    "one_star": "one_star.png",
    "two_star": "two_star.png",
    "three_star": "three_star.png",
    "bird_red": "red-bird.png",
    "bird_yellow": "yellow-bird.png",
    "bird_blue": "blue-bird.png",
    "bird_eagle": "eagle-bird.png",
    "pig": "pig.png",
    "pig_failed": "pig_failed.png",
    "box_wood": "wood_box.png",
    "box_stone": "stone_box.png",
    "column_wood": "wood_column.png",
    "column_stone": "stone_column.png",
    "wheel_wood": "wood_wheel.png",
    "wheel_stone": "stone_wheel.png",
}

SPRITE_SIZES = {
    "bird_red": (90, 90),
    "bird_yellow": (70, 54),
    "bird_blue": (62, 62),
    "bird_eagle": (78, 52),
    "pig": (66, 64),
    "box_wood": (82, 82),
    "box_stone": (82, 82),
    "column_wood": (21, 160),
    "column_stone": (20, 159),
    "wheel_wood": (75, 75),
    "wheel_stone": (75, 75),
}

SKY_BLUE = (179, 219, 255)
DARK_TEXT = (34, 34, 34)
BUTTON_FILL = (70, 87, 117)
BUTTON_HIGHLIGHT = (95, 117, 153)
BUTTON_TEXT = (245, 245, 245)
PANEL_FILL = (198, 227, 255)
PANEL_OUTLINE = (74, 96, 124)
SUCCESS_GREEN = (78, 177, 96)
WARNING_RED = (217, 89, 89)
ACCENT_GOLD = (247, 197, 72)
PANEL_DARK = (39, 52, 80)
PANEL_SOFT = (247, 249, 255)
TEXT_MUTED = (86, 95, 116)
TRAJECTORY_BLUE = (66, 135, 245)
FLOOR_GREEN = (64, 113, 65)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_LINE = (255, 255, 255, 28)

PALETTE_CENTERS = [
    (WINDOW_WIDTH - 525, WINDOW_HEIGHT - 75),
    (WINDOW_WIDTH - 375, WINDOW_HEIGHT - 75),
    (WINDOW_WIDTH - 225, WINDOW_HEIGHT - 75),
    (WINDOW_WIDTH - 75, WINDOW_HEIGHT - 75),
]
PALETTE_BOX_SIZE = 125
UNDO_BUTTON_CENTER = (WINDOW_WIDTH - 650, WINDOW_HEIGHT - 75)
BUILDER_RESET_CENTER = (WINDOW_WIDTH - 500, WINDOW_HEIGHT - 170)
BUILDER_PLAY_CENTER = (WINDOW_WIDTH - 250, WINDOW_HEIGHT - 170)
BIRD_RESET_CENTER = (422, 638)
