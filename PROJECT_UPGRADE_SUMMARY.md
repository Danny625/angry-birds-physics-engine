# Angry Birds Project Upgrade Summary

This document explains what changed from the original CMU Graphics school project to the upgraded software engineering project. It is written so you can use it while updating GitHub, writing resume bullets, or explaining the project in an interview.

## Short Version

The original project was a 2D Angry Birds-style physics game built with CMU Graphics. The upgraded project keeps the playable game idea, but reorganizes it into a more professional local-first software project.

The project now includes:

- A modern Pygame frontend instead of CMU Graphics.
- A separated game engine, data models, level serialization layer, UI renderer, API backend, and tests.
- JSON save/load for built-in and custom builder levels.
- A builder mode with named save slots, replace-save, load menu, clear-birds controls, and playtesting.
- Multiple bird types with different abilities.
- Local SQLite high scores shown in the game.
- A FastAPI backend for saving levels and leaderboard scores through API endpoints.
- A pytest test suite for engine behavior, level serialization, high scores, and API routes.
- A Dockerfile for packaging the backend API.
- A README with setup, architecture, API examples, test commands, and Docker commands.

## What The Original Project Was

The original version was preserved in `legacy_cmu/`.

That version was valuable because it proved you could build:

- An interactive game.
- A physics-style simulation.
- User controls with mouse and keyboard input.
- Visual gameplay using CMU Graphics.

The limitation was not that the original project was bad. The limitation was that it looked like a class project because most of the value was inside the game window. It did not strongly show backend development, persistent data, tests, packaging, or clean software layers.

## What The New Project Is

The active upgraded project lives in `modern_pygame/`.

The new project is best described as:

> A local-first 2D physics game with a modular Python game engine, Pygame renderer, JSON level serialization, SQLite persistence, FastAPI backend, pytest coverage, and Dockerized API setup.

That sentence matters because it turns the project from "I made a game" into "I built a complete software system around a game."

## Why Migrating Away From CMU Graphics Helped

CMU Graphics is useful for learning, but it can make a project look tied to a school assignment. Pygame is a more recognizable Python game framework, so the migrated version feels more independent and easier for other people to run.

The migration also helped because:

- The legacy CMU code could stay preserved instead of being overwritten.
- The modern project could use its own virtual environment.
- The game could be organized into modules instead of one large school-style script.
- The README can present the project as a standalone engineering project.

## Current Folder Structure

```text
Angry Birds/
  legacy_cmu/
    main.py
    objects.py
    images/
    HOW_TO_RUN.txt

  modern_pygame/
    angrybirds/
      constants.py
      engine.py
      levels.py
      models.py
      pygame_client.py
      scores.py

    api/
      app.py
      database.py
      models.py
      schemas.py
      routes/
        levels.py
        scores.py

    images/
    levels/
    tests/
    pygame_main.py
    requirements.txt
    run_api.bat
    run_pygame.bat
    run_tests.bat

  Dockerfile
  README.md
  PROJECT_UPGRADE_SUMMARY.md
```

## Clean Architecture

Clean architecture means each part of the program has a clear job.

In the upgraded project:

- `angrybirds/engine.py` controls game rules, physics updates, scoring, bird abilities, win/loss state, builder behavior, and save/load actions.
- `angrybirds/models.py` defines the core data objects, such as birds, pigs, physics bodies, levels, and game state.
- `angrybirds/pygame_client.py` handles drawing, buttons, menus, overlays, mouse input, keyboard input, and the playable Pygame window.
- `angrybirds/levels.py` handles JSON serialization and deserialization for level data.
- `angrybirds/scores.py` handles local SQLite high score storage for the game.
- `api/` handles the FastAPI backend and SQLite API persistence.
- `tests/` contains automated tests that verify important behavior.

This separation is important because it shows the project is not just a visual demo. It has layers, data flow, testable logic, and independent responsibilities.

## Pygame Frontend

The upgraded game runs through Pygame. The launcher is:

```powershell
cd "C:\Users\Danny\OneDrive\Desktop\15-112\TP3\Angry Birds\modern_pygame"
.\.venv\Scripts\python.exe pygame_main.py
```

The Pygame frontend is responsible for:

- Drawing the background, birds, pigs, blocks, menus, HUD, overlays, and builder palette.
- Handling mouse dragging and launching birds.
- Handling keyboard shortcuts.
- Handling clickable UI buttons.
- Showing score, best score, next bird queue, save/load dialogs, and help overlays.

The game still supports keyboard shortcuts, but it now has clickable buttons for common actions like Save, Replace, Load, Help, Replay, Edit, and Menu.

## Builder Mode

Builder mode was upgraded from a simple sandbox into a more complete level editor.

Builder mode now supports:

- Adding birds to the launch queue.
- Clearing only birds without deleting structures.
- Clearing only structures without deleting birds.
- Dragging pigs and blocks onto the field.
- Instantly playtesting the layout.
- Saving a custom level as a named JSON save slot.
- Loading saved builder levels from a menu.
- Replacing a loaded saved level with a new name or updated layout.
- Deleting saved builder levels.
- Automatically renumbering saved slots after deletion.
- Paging the saved-level list so many saved levels do not overflow the menu.

The important technical idea is that builder mode can turn the current in-memory layout into JSON, then rebuild the same layout later from that JSON.

## JSON Save/Load

JSON is a text format for storing structured data. In this project, JSON describes levels.

A level JSON file contains information like:

```json
{
  "id": "builder_level_01",
  "name": "Training Tower",
  "birds": ["red", "blue"],
  "pigs": [{ "x": 920, "y": 430, "angle": 0 }],
  "objects": [
    { "kind": "box", "x": 860, "y": 520, "angle": 0, "material": "wood" }
  ],
  "stars": {
    "one": 500,
    "two": 1000,
    "three": 1500
  }
}
```

The important software engineering terms are:

- Serialization: converting a Python level object into JSON text.
- Deserialization: reading JSON text and rebuilding a Python level object.

The project has both.

## Named Save Slots

The builder save system now uses numbered JSON files:

```text
builder_level_01.json
builder_level_02.json
builder_level_03.json
```

Each saved level also has a human-readable name, such as `Training Tower` or `Final Siege`.

The save workflow is:

1. Build a layout in builder mode.
2. Click `Save`.
3. Type a level name.
4. Click `Save New`.
5. The game creates the next numbered JSON save file.

The replace workflow is:

1. Click `Load`.
2. Choose a saved builder level.
3. Edit it.
4. Click `Replace`.
5. Change the name if needed.
6. The game overwrites that same saved JSON file.

The delete workflow is:

1. Click `Load`.
2. Click `Delete` next to a saved level.
3. The selected JSON file is removed.
4. The remaining saved levels are compacted so the numbering stays clean.

Example: if `builder_level_01.json`, `builder_level_02.json`, and `builder_level_03.json` exist, deleting level 1 makes the old level 2 become `builder_level_01.json` and the old level 3 become `builder_level_02.json`.

## Bird Types

The upgraded game includes multiple bird types:

- Red Bird: standard impact bird.
- Yellow Bird: speed burst ability.
- Blue Bird: splits into three lighter birds.
- Mighty Eagle: redirects downward into a vertical slam.

This gives the game more replay value and shows that the engine supports different entity behavior.

## Local High Scores

The game now saves local high scores in SQLite.

SQLite is a database that stores data in a local file. In this project, runtime data is stored under:

```text
%TEMP%\physics_game_engine\
```

High score behavior:

- When you win a built-in level, the game checks your score.
- If your score beats the previous best for that level, it saves the new best score.
- The best score appears on the home level menu.
- The best score also appears in the in-game HUD.

This makes persistence visible in the game itself.

## FastAPI Backend

FastAPI is a Python framework for building APIs. An API lets one program talk to another program through endpoints.

The backend lives in:

```text
modern_pygame/api/
```

The API currently supports:

- `GET /health`
- `POST /levels`
- `GET /levels`
- `GET /levels/{level_id}`
- `POST /scores`
- `GET /leaderboard/{level_id}`

The API is local-first. It does not require paid hosting.

To run it:

```powershell
cd "C:\Users\Danny\OneDrive\Desktop\15-112\TP3\Angry Birds\modern_pygame"
run_api.bat
```

Then open:

```text
http://127.0.0.1:8000/docs
```

That page is FastAPI's built-in interactive API documentation.

## SQLite Persistence

SQLite stores data in a local database file.

The project uses SQLite for:

- API level records.
- API leaderboard score records.
- Local game high scores.

The default database path is:

```text
%TEMP%\physics_game_engine\data\physics_game.db
```

This is free, local, and easy to reset. It also avoids paid hosting or cloud database maintenance.

## Pytest Tests

Pytest is the tool used to run automated tests.

Tests are small programs that check whether important parts of the project still work. Instead of manually checking every feature after every change, tests quickly verify the core behavior.

The tests currently cover:

- Level JSON round trips.
- Saving and loading level files.
- Numbered builder save slots.
- Builder save deletion and automatic slot compaction.
- Built-in level loading.
- Blue Bird split behavior.
- Mighty Eagle slam behavior.
- Builder save/load.
- Builder replace-save.
- Local high score behavior.
- API health route.
- API level creation and retrieval.
- API level listing.
- API leaderboard sorting.

To run the tests:

```powershell
cd "C:\Users\Danny\OneDrive\Desktop\15-112\TP3\Angry Birds\modern_pygame"
run_tests.bat
```

If the tests pass, you know the important engine, data, API, and persistence behavior is still working.

## Docker

Docker packages software so it can run in a consistent environment.

For this project, Docker is used for the FastAPI backend, not the Pygame game window.

The Dockerfile is already written:

```text
Dockerfile
```

What Docker does here:

- Starts from a Python base image.
- Copies the backend/game package files.
- Installs dependencies from `requirements.txt`.
- Runs the FastAPI server.

To use Docker, you need Docker Desktop installed on your computer.

After Docker Desktop is installed and running, build the backend image from the workspace root:

```powershell
cd "C:\Users\Danny\OneDrive\Desktop\15-112\TP3\Angry Birds"
docker build -t physics-game-api .
```

Then run the API container:

```powershell
docker run -p 8000:8000 physics-game-api
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Docker is not required to play the game. It is there to show that the backend can be packaged and run reproducibly.

## What Is Already Done

These resume bridge items are done:

- CMU legacy version preserved.
- Modern Pygame version created.
- Game logic separated from rendering/UI.
- JSON level save/load added.
- Named builder save slots added.
- Replace-save for builder levels added.
- Delete and pagination support for saved builder levels added.
- Local SQLite high scores added.
- FastAPI backend added.
- SQLite API persistence added.
- Pytest tests added.
- Dockerfile added.
- README added.
- Run scripts added.
- Project folder organization cleaned up.

## What Is Still Worth Polishing

The main remaining polish items are presentation-focused:

- Add real screenshots to the README.
- Add a short gameplay GIF.
- Test Docker after installing Docker Desktop.
- Optionally add a button that publishes a builder level from the game UI to the FastAPI API.
- Optionally add an in-game API status panel.

Those are nice improvements, but the core software engineering bridge is already in place.

## Resume Bullets

You could describe the project with bullets like these:

- Refactored a CMU Graphics physics game into a modular Pygame project with separated game engine, rendering, data models, serialization, and UI layers.
- Implemented JSON level serialization for custom builder levels, including named save slots, replace-save workflow, and load menu.
- Built a local-first FastAPI backend with SQLite persistence for user-created levels and leaderboard scores.
- Added local SQLite high score tracking integrated into the Pygame level menu and gameplay HUD.
- Developed pytest coverage for level serialization, builder save/load, bird abilities, high score persistence, and API endpoints.
- Dockerized the FastAPI backend for reproducible local execution without paid hosting.

## Interview Explanation

A good interview explanation would be:

> I started with an Angry Birds-inspired physics game from a class project and rebuilt it into a more complete software engineering project. I preserved the original CMU Graphics version, then created a modern Pygame version with cleaner separation between the engine, renderer, models, and persistence logic. I added JSON save/load for custom builder levels, local SQLite high scores, a FastAPI backend for levels and leaderboard scores, pytest coverage, Docker support for the API, and a README explaining the architecture and setup.

If asked why this matters:

> The original project showed interactive programming and physics logic. The upgraded version shows broader engineering skills: modular architecture, serialization, backend APIs, database persistence, automated testing, packaging, documentation, and user-facing polish.

## Commands To Remember

Run the game:

```powershell
cd "C:\Users\Danny\OneDrive\Desktop\15-112\TP3\Angry Birds\modern_pygame"
.\.venv\Scripts\python.exe pygame_main.py
```

Run the API:

```powershell
cd "C:\Users\Danny\OneDrive\Desktop\15-112\TP3\Angry Birds\modern_pygame"
run_api.bat
```

Run tests:

```powershell
cd "C:\Users\Danny\OneDrive\Desktop\15-112\TP3\Angry Birds\modern_pygame"
run_tests.bat
```

Build Docker image:

```powershell
cd "C:\Users\Danny\OneDrive\Desktop\15-112\TP3\Angry Birds"
docker build -t physics-game-api .
```

Run Docker container:

```powershell
docker run -p 8000:8000 physics-game-api
```
