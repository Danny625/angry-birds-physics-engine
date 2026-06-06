# Screenshot Guide

This guide explains how to capture README screenshots for the Angry Birds Physics Engine + Level Sharing API project.

The screenshots should make the project look like a complete software engineering project, not just a game clone. The best set is:

1. Gameplay
2. Builder Mode
3. Saved builder levels
4. FastAPI docs
5. Tests passing

Save all screenshots here:

```text
docs/screenshots/
```

## Current Repo Layout

The active GitHub layout is:

```text
angry-birds-physics-engine/
├── README.md
├── LICENSE
├── requirements.txt
├── Dockerfile
├── play_game.bat
├── play_screenshot_mode.bat
└── game/
    ├── pygame_main.py
    ├── pytest.ini
    ├── angrybirds/
    ├── api/
    ├── images/
    ├── levels/
    ├── data/
    ├── saved_levels/
    └── tests/
```

## Before You Start

Use a clean runtime folder so old saves and scores do not clutter the screenshots.

From the project root:

```powershell
$env:PHYSICS_GAME_HOME="$env:TEMP\physics_game_screenshots"
Remove-Item -Recurse -Force $env:PHYSICS_GAME_HOME -ErrorAction SilentlyContinue
```

Then launch the game:

```powershell
.\play_screenshot_mode.bat
```

You can also use:

```powershell
.\play_game.bat
```

The screenshot launcher is mostly the same as `play_game.bat`, but it sets:

```text
PHYSICS_GAME_HOME=%TEMP%\physics_game_screenshots
```

That keeps screenshot saves and high scores isolated from your normal local game data.

## Exact Controls

- Launch a bird: click and hold the active bird on the slingshot, drag backward, then release.
- Use bird ability: press `Space` while a bird is flying.
- Enter Builder Mode: click `Builder Mode` on the main menu, or press `B` from the main menu.
- Start built-in levels: click a level button, or press `1` through `5` from the main menu.
- Replay a built-in level: click `Replay`, or press `R`.
- Return to main menu: click `Menu`, click the home icon, or press `Esc`.
- Open help: click `Help`, or press `H`.
- Builder playtest: click `Play Test`, or press `P` while editing a builder layout.
- Builder replay playtest: click `Replay`, or press `R` while playtesting.
- Builder edit playtest: click `Edit`, or press `E` while playtesting.
- Save builder level: click `Save`, or press `S` while editing; type a name; press `Enter` or click `Save New`.
- Load builder level: click `Load`, or press `L` while editing; click a saved level row.
- Replace builder level: load a saved builder level first, then click `Replace`.
- Delete builder level: open `Load`, then click `Delete` beside a saved level.

## Screenshot 1: Gameplay

Suggested filename:

```text
docs/screenshots/gameplay.png
```

What should be visible:

- A built-in level running
- Slingshot and active bird
- Pigs and blocks
- HUD with level name, score, controls, and bird queue
- Ideally a trajectory line or bird in flight

Recommended steps:

1. Run `.\play_screenshot_mode.bat`.
2. On the main menu, click `Level 5` or press `5`.
3. Click and drag the first bird backward from the slingshot.
4. Pause while the trajectory dots are visible.
5. Press `Win + Shift + S`.
6. Capture the Pygame window.
7. Save as:

```text
docs/screenshots/gameplay.png
```

Why Level 5:

- It includes Yellow, Blue, Mighty Eagle, and Red birds.
- It has several pigs and structures on screen.
- It gives the screenshot a stronger "physics sandbox" look.

Optional action shot:

1. Launch the Yellow bird.
2. Press `Space` mid-flight for the speed burst.
3. Screenshot the bird in flight or the collision aftermath.

Manual screenshots are easier here than automated capture because the best frame depends on timing.

## Screenshot 2: Builder Mode

Suggested filename:

```text
docs/screenshots/builder-mode.png
```

What should be visible:

- Builder Mode title/HUD
- Top-right buttons: `Save`, `Replace`, `Load`, `Help`, `Menu`
- Builder action panel: `Clear Blocks`, `Clear Birds`, `Play Test`
- Palette showing placeable items
- At least one custom pig/block/bird placed or queued

Recommended steps:

1. From the main menu, click `Builder Mode` or press `B`.
2. Click `Birds`.
3. Click `Blue / Split` or `Eagle / Slam` to add a bird to the queue.
4. Click the back arrow near the bottom palette.
5. Click `Pigs`.
6. Drag the pig from the palette onto the field above the grass.
7. Click the back arrow.
8. Click `Blocks`.
9. Click `Boxes`.
10. Drag a wood or stone box onto the field near the pig.
11. Take the screenshot with `Win + Shift + S`.
12. Save as:

```text
docs/screenshots/builder-mode.png
```

Tip:

Do not overcrowd the scene. One pig, one box, and one queued bird is enough to show the feature clearly.

## Screenshot 3: Saved Levels

Suggested filename:

```text
docs/screenshots/saves-or-highscores.png
```

Use the saved builder levels menu. It is more visually clear than high scores for the README because it shows named saves, slot details, and Delete buttons.

What should be visible:

- `Saved Builder Levels` overlay
- A named saved level row
- Details like number of birds, pigs, and objects
- `Delete` button
- Previous/Next paging controls if visible

Recommended steps:

1. In Builder Mode, make a tiny layout:
   - Add one bird.
   - Place one pig.
   - Place one box.
2. Click `Save`.
3. Rename the level to something clean, such as:

```text
Demo Builder Level
```

4. Press `Enter` or click `Save New`.
5. Click `Load`.
6. Screenshot the saved-level overlay.
7. Save as:

```text
docs/screenshots/saves-or-highscores.png
```

Optional:

After this screenshot, click the saved level row to prove loading works, then click `Replace` if you want to test the edit/replace workflow. You do not need to screenshot every step.

## Screenshot 4: FastAPI Docs

Suggested filename:

```text
docs/screenshots/api-docs.png
```

What should be visible:

- Browser open to `http://127.0.0.1:8000/docs`
- Endpoints:
  - `GET /health`
  - `POST /levels`
  - `GET /levels`
  - `GET /levels/{level_id}`
  - `POST /scores`
  - `GET /leaderboard/{level_id}`

Start the API from the project root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.app:create_app --factory --host 127.0.0.1 --port 8000 --app-dir game
```

Alternative from inside the `game/` folder:

```powershell
cd game
..\.venv\Scripts\python.exe -m uvicorn api.app:create_app --factory --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Take the screenshot and save as:

```text
docs/screenshots/api-docs.png
```

Tip:

Leave the docs collapsed if all endpoints are visible. Expand one endpoint only if it still fits cleanly on screen.

## Screenshot 5: Tests Passing

Suggested filename:

```text
docs/screenshots/tests-passing.png
```

What should be visible:

- Terminal command
- Passing pytest summary
- Ideally the command prompt location showing the project

From the project root:

```powershell
cd game
..\.venv\Scripts\python.exe -m pytest tests -q
```

Expected result:

```text
14 passed
```

Take a screenshot after the test run finishes and save as:

```text
docs/screenshots/tests-passing.png
```

## Recommended Screenshot Order

Use this order to minimize setup friction:

1. Clean runtime data.
2. Launch game.
3. Capture `gameplay.png`.
4. Enter Builder Mode.
5. Capture `builder-mode.png`.
6. Save a builder level.
7. Capture `saves-or-highscores.png`.
8. Close the game.
9. Start FastAPI.
10. Capture `api-docs.png`.
11. Run pytest.
12. Capture `tests-passing.png`.

## README Snippet

After you create the screenshots, paste the contents of:

```text
docs/README_SCREENSHOT_SNIPPET.md
```

into your README.

Do not add the screenshot section before the image files exist unless you are okay with broken image placeholders on GitHub.

## Docker Note

Docker is included for the backend API, but it should not be part of the screenshot set unless you have Docker installed and have verified:

```powershell
docker build -t physics-game-api .
docker run -p 8000:8000 physics-game-api
```

The game itself does not need Docker.
