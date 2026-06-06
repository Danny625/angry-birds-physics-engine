# 🐦 Angry Birds Physics Engine + Level Sharing API

A local-first 2D physics game upgraded from an Angry Birds-inspired class project into a more complete Python software engineering project.

The current version uses **Pygame** for the playable frontend, a separated game engine for physics and game state, **JSON** for custom level save/load, **SQLite** for local persistence, **FastAPI** for level and leaderboard endpoints, **pytest** for automated tests, and **Docker** for reproducible backend execution.

## Contents

- [Demo](#-demo)
- [Quick Start](#-quick-start)
- [What This Project Shows](#-what-this-project-shows)
- [Technologies](#-technologies)
- [Features](#-features)
- [How to Play](#-how-to-play)
- [How to Run the Game](#-how-to-run-the-game)
- [How to Run the API](#-how-to-run-the-api)
- [How to Run Tests](#-how-to-run-tests)
- [Docker](#-docker)
- [Architecture](#-architecture)
- [Example API Payloads](#-example-api-payloads)
- [Runtime Data](#-runtime-data)
- [Design Decisions](#-design-decisions)
- [What I Learned](#-what-i-learned)
- [Future Improvements](#-future-improvements)
- [Asset Credits](#-asset-credits)

## 🍿 Demo

[![Angry Birds Physics Engine Demo](https://img.youtube.com/vi/O0r57TcT31w/maxresdefault.jpg)](https://www.youtube.com/watch?v=O0r57TcT31w)

Alternative link: https://youtu.be/O0r57TcT31w

> Note: this video shows an earlier gameplay demo. The current version now includes the Pygame frontend, builder save/load, local high scores, FastAPI backend, automated tests, and Docker setup.

## 🚀 Quick Start

### Easiest way on Windows

From the project root, run:

```powershell
play_game.bat
```

This script creates a local virtual environment, installs dependencies, and launches the game.

### Manual setup

```bash
git clone https://github.com/Danny625/angry-birds-physics-engine.git
cd angry-birds-physics-engine
python -m pip install -r requirements.txt
cd game
python pygame_main.py
```

## 🧠 What This Project Shows

This started as a playable game, but I upgraded it to show broader software engineering skills:

- Modular Python architecture
- Game logic separated from rendering and input
- JSON serialization/deserialization for reusable levels
- SQLite persistence for local high scores and backend data
- FastAPI backend for level and leaderboard data
- Pytest coverage for engine, persistence, serialization, and API behavior
- Dockerized backend setup for reproducible local execution
- Clean project layout with the playable game, backend, assets, and tests organized under `game/`

## 📦 Technologies

- Python
- Pygame
- FastAPI
- SQLite
- pytest
- Docker
- JSON

## ✨ Features

### 🎮 Modern Pygame Game

The active version runs in Pygame and keeps the Angry Birds-style gameplay: launch birds, hit structures, pop pigs, earn points, and clear levels.

The frontend handles drawing, menus, buttons, overlays, keyboard controls, mouse input, gameplay HUD, and builder mode UI.

### 🧱 Builder Mode

Builder Mode lets you create, edit, save, load, and playtest custom levels.

You can:

- Add birds to the launch queue
- Place pigs and structures
- Clear birds separately from structures
- Playtest custom layouts
- Save levels with custom names
- Load saved builder levels
- Replace edited saves
- Delete saved levels
- Page through saved levels when the list grows

### 💾 JSON Level Save/Load

Custom levels are saved as JSON files.

The game can turn an in-memory level into reusable JSON, save that level, load it later, and rebuild the same layout. This supports built-in levels, builder levels, named save slots, replace-save workflows, and delete-save workflows.

### 🏆 Local High Scores

High scores are saved locally with SQLite.

When you beat a built-in level, the game checks whether your score is a new best score. If it is, the score is saved and shown in the level menu and gameplay HUD.

### 🐦 Multiple Bird Types

The engine supports different bird behaviors:

- **Red Bird:** standard impact bird
- **Yellow Bird:** speed burst
- **Blue Bird:** splits into three smaller birds
- **Mighty Eagle:** redirects downward into a vertical slam

### 🌐 FastAPI Backend

The project includes a local FastAPI backend for level sharing and leaderboard-style score storage.

Available endpoints:

```text
GET /health
POST /levels
GET /levels
GET /levels/{level_id}
POST /scores
GET /leaderboard/{level_id}
```

FastAPI docs are available at:

```text
http://127.0.0.1:8000/docs
```

### ✅ Tests

The project includes pytest coverage for important behavior, including:

- Level JSON round trips
- Saving and loading level files
- Numbered builder save slots
- Built-in level loading
- Blue Bird split behavior
- Mighty Eagle slam behavior
- Builder save/load
- Builder replace-save
- Local high score persistence
- API health route
- API level creation and retrieval
- API leaderboard sorting

## 🎮 How to Play

- Choose a built-in level from the main menu.
- Drag a bird backward from the slingshot to aim.
- Release the mouse to launch.
- Use each bird’s ability while it is in flight.
- Pop all pigs before running out of birds.
- Earn stars based on your score.
- If you beat your best score on a built-in level, the new high score is saved locally.

### Builder Mode

In Builder Mode, you can place pigs, blocks, and birds, then playtest the layout.

You can also save custom levels as named JSON slots, load them later, edit them, replace the saved version, or delete old saves.

## 🚦 How to Run the Game

### Windows shortcut

From the project root:

```powershell
play_game.bat
```

### Manual Windows setup

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd game
..\.venv\Scripts\python.exe pygame_main.py
```

### Manual macOS/Linux setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd game
python pygame_main.py
```

## 🌐 How to Run the API

The API runs locally with FastAPI.

### Windows

```powershell
cd game
..\.venv\Scripts\python.exe -m uvicorn api.app:create_app --factory --host 127.0.0.1 --port 8000
```

### macOS/Linux

```bash
cd game
python -m uvicorn api.app:create_app --factory --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 🧪 How to Run Tests

Install dependencies first:

```bash
python -m pip install -r requirements.txt
```

Then run tests from the `game/` folder.

### Windows

```powershell
cd game
..\.venv\Scripts\python.exe -m pytest tests
```

### macOS/Linux

```bash
cd game
python -m pytest tests
```

## 🐳 Docker

Docker is used for the FastAPI backend, not the Pygame game window.

You do not need Docker to play the game. Docker is included so the backend can be packaged and run in a reproducible local environment.

Build the backend image from the project root:

```bash
docker build -t physics-game-api .
```

Run the API container:

```bash
docker run -p 8000:8000 physics-game-api
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## 🧠 Architecture

The upgraded project is split into layers so the game logic, UI, persistence, API, and tests each have clear responsibilities.

```text
angry-birds-physics-engine/
├── README.md
├── LICENSE
├── requirements.txt
├── Dockerfile
├── play_game.bat
├── .gitignore
├── .dockerignore
└── game/
    ├── pygame_main.py
    ├── pytest.ini
    │
    ├── angrybirds/
    │   ├── constants.py
    │   ├── engine.py
    │   ├── levels.py
    │   ├── models.py
    │   ├── pygame_client.py
    │   └── scores.py
    │
    ├── api/
    │   ├── app.py
    │   ├── database.py
    │   ├── models.py
    │   ├── schemas.py
    │   └── routes/
    │       ├── levels.py
    │       └── scores.py
    │
    ├── images/
    ├── levels/
    ├── data/
    ├── saved_levels/
    └── tests/
        ├── conftest.py
        ├── test_api.py
        ├── test_engine.py
        ├── test_levels.py
        └── test_scores.py
```

### Main layers

```text
game/angrybirds/engine.py
```

Owns the core game logic: physics ticks, collisions, scoring, bird abilities, win/loss rules, builder state, save/load behavior, and game state transitions.

```text
game/angrybirds/models.py
```

Defines the main game objects: birds, pigs, world bodies, levels, and runtime game state.

```text
game/angrybirds/pygame_client.py
```

Handles drawing, menus, buttons, overlays, mouse input, keyboard input, builder UI, and playtest UI.

```text
game/angrybirds/levels.py
```

Handles built-in level loading, level-to-JSON conversion, JSON-to-level rebuilding, custom level saves, and numbered save slot discovery.

```text
game/angrybirds/scores.py
```

Handles local SQLite high scores used by the Pygame game.

```text
game/api/
```

Provides REST endpoints for saved levels and leaderboard scores.

```text
game/tests/
```

Contains automated tests for engine behavior, serialization, persistence, high scores, and API routes.

## 📡 Example API Payloads

### Create a level

```json
{
  "name": "Starter Level",
  "author": "Danny",
  "level_json": {
    "id": "starter_level",
    "name": "Starter Level",
    "birds": ["red", "yellow"],
    "pigs": [{ "x": 940, "y": 455 }],
    "objects": [
      { "kind": "box", "x": 900, "y": 618, "angle": 0, "material": "wood" }
    ],
    "stars": {
      "one": 500,
      "two": 900,
      "three": 1300
    }
  }
}
```

### Submit a score

```json
{
  "level_id": 1,
  "player": "Danny",
  "score": 2200
}
```

## 💾 Runtime Data

The project is local-first, so it does not require paid hosting or a cloud database.

By default, runtime data is stored under:

```text
%TEMP%\physics_game_engine\
```

This includes:

```text
%TEMP%\physics_game_engine\data\physics_game.db
%TEMP%\physics_game_engine\saved_levels\builder_level_01.json
```

You can override the runtime location by setting:

```text
PHYSICS_GAME_HOME
```

The tracked `game/data/` and `game/saved_levels/` folders only contain placeholders. Actual runtime databases and custom saved levels are ignored by Git.

## 👩‍🍳 Design Decisions

### Why migrate to Pygame?

Pygame is a more recognizable standalone Python game framework than CMU Graphics. Migrating made the project easier to present as an independent software engineering project while keeping the original gameplay idea.

### Why local-first?

The goal was to demonstrate software engineering skills without paid hosting or long-term maintenance. SQLite stores data locally, FastAPI runs on localhost, and Docker packages the backend for reproducible local execution.

### Why separate the API from the game?

The Pygame game can run on its own, while the FastAPI backend demonstrates REST API and database-backed persistence. Keeping them separate avoids overcomplicating the game loop.

### Why keep the code in a `game/` folder?

The repository root stays clean for GitHub visitors, while the actual game code, assets, levels, API, and tests live together in one organized project folder.

## 📚 What I Learned

- How to separate game logic from rendering and input
- How to organize a Python project into testable modules
- How to serialize and deserialize game state with JSON
- How to use SQLite for local persistence
- How to build a local REST API with FastAPI
- How to write pytest coverage for engine and API behavior
- How to package a backend service with Docker
- How to turn an older project into a stronger software engineering portfolio project

## 💭 Future Improvements

- Add updated screenshots and a short gameplay GIF
- Add a builder mode screenshot
- Add a FastAPI docs screenshot
- Connect the Pygame builder UI directly to the local API for one-click publish/load
- Add an in-game API status panel
- Add more regression tests for edge-case physics interactions
- Add level metadata such as description, difficulty, and tags

## 🎨 Asset Credits

This project was built for learning and portfolio purposes. The artwork is not original, and this project is not affiliated with Rovio or the official Angry Birds franchise.

- Angry Birds logo image from the Angry Birds Wiki
- Bird, pig, block, background, star, and UI sprites adapted from GitHub user `estevaofon`'s Angry Birds Python resources
