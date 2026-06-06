# 🐦 Physics Game Engine + Level Sharing API

A local-first 2D physics game upgraded from an Angry Birds-inspired CMU Graphics project into a modular Python software engineering project.

The active version uses **Pygame** for the playable frontend, a separated game engine for physics and game state, **JSON serialization** for custom levels, **SQLite** for local persistence, **FastAPI** for level and leaderboard endpoints, **pytest** for automated tests, and **Docker** for reproducible backend execution.

## 🍿 Demo

[![Angry Birds Physics Engine Demo](https://img.youtube.com/vi/O0r57TcT31w/maxresdefault.jpg)](https://www.youtube.com/watch?v=O0r57TcT31w)

Alternative link: https://youtu.be/O0r57TcT31w

> Note: this video shows the original gameplay demo. The upgraded version now includes the modern Pygame frontend, builder save/load, local high scores, API backend, tests, and Docker setup.

## 🧠 What This Project Shows

This started as a playable game, but I upgraded it to show broader software engineering skills:

- modular Python architecture
- separation of game logic from rendering/input
- JSON serialization and deserialization for levels
- local SQLite persistence for high scores
- FastAPI backend for levels and leaderboard scores
- pytest coverage for engine, persistence, serialization, and API behavior
- Dockerized backend setup for reproducible local execution
- preserved legacy version plus active modern version

## 📦 Technologies

- Python
- Pygame
- FastAPI
- SQLite
- pytest
- Docker
- JSON
- CMU Graphics, preserved in the legacy version

## ✨ Features

### 🎮 Modern Pygame Game

The active version runs in Pygame and keeps the original Angry Birds-style gameplay: launch birds, hit structures, pop pigs, earn points, and clear levels.

The game now has a cleaner frontend layer for rendering, menus, buttons, overlays, keyboard controls, mouse input, and gameplay HUD.

### 🧱 Builder Mode

Builder Mode lets you create and test custom levels.

You can:

- add birds to the launch queue
- place pigs and structures
- clear birds separately from structures
- playtest custom layouts
- save levels with custom names
- load saved builder levels
- replace edited saves
- delete saved levels
- page through saved levels when the list grows

### 💾 JSON Level Save/Load

Custom levels are saved as JSON files.

That means the game can turn an in-memory level into a reusable file, then load that file later and rebuild the same level. This supports built-in levels, builder levels, named save slots, and replace-save workflows.

### 🏆 Local High Scores

High scores are saved locally with SQLite.

When you beat a built-in level, the game checks whether your score is a new best score. If it is, the score is saved and shown in the level menu and gameplay HUD.

### 🐦 Multiple Bird Types

The engine supports different bird behaviors:

- Red Bird: standard impact bird
- Yellow Bird: speed burst
- Blue Bird: splits into three smaller birds
- Mighty Eagle: redirects downward into a vertical slam

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

- level JSON round trips
- saving and loading level files
- numbered builder save slots
- built-in level loading
- Blue Bird split behavior
- Mighty Eagle slam behavior
- builder save/load
- builder replace-save
- local high score persistence
- API health route
- API level creation and retrieval
- API leaderboard sorting

## 🚦 How to Run the Game

### 1. Clone the repo

```bash
git clone https://github.com/Danny625/angry-birds-physics-engine.git
cd angry-birds-physics-engine
```

### 2. Go into the modern version

```bash
cd "Angry Birds/modern_pygame"
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the game

```bash
python pygame_main.py
```

On Windows, you can also use:

```powershell
run_pygame.bat
```

## 🌐 How to Run the API

From the modern project folder:

```bash
cd "Angry Birds/modern_pygame"
```

Run:

```bash
python -m uvicorn api.app:create_app --factory --host 127.0.0.1 --port 8000
```

Or on Windows:

```powershell
run_api.bat
```

Then open:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## 🧪 How to Run Tests

From the modern project folder:

```bash
cd "Angry Birds/modern_pygame"
pytest
```

Or on Windows:

```powershell
run_tests.bat
```

## 🐳 Docker

Docker is used for the FastAPI backend, not the Pygame window.

Build the backend image from the project root:

```bash
cd "Angry Birds"
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
├── .gitignore
└── Angry Birds/
    ├── legacy_cmu/
    │   ├── main.py
    │   ├── objects.py
    │   ├── images/
    │   └── HOW_TO_RUN.txt
    │
    ├── modern_pygame/
    │   ├── angrybirds/
    │   │   ├── constants.py
    │   │   ├── engine.py
    │   │   ├── levels.py
    │   │   ├── models.py
    │   │   ├── pygame_client.py
    │   │   └── scores.py
    │   │
    │   ├── api/
    │   │   ├── app.py
    │   │   ├── database.py
    │   │   ├── models.py
    │   │   ├── schemas.py
    │   │   └── routes/
    │   │       ├── levels.py
    │   │       └── scores.py
    │   │
    │   ├── images/
    │   ├── levels/
    │   ├── saved_levels/
    │   ├── tests/
    │   ├── pygame_main.py
    │   ├── requirements.txt
    │   ├── run_api.bat
    │   ├── run_pygame.bat
    │   └── run_tests.bat
    │
    ├── Dockerfile
    └── PROJECT_UPGRADE_SUMMARY.md
```

### Game Engine

```text
modern_pygame/angrybirds/engine.py
```

Owns the core game logic:

- physics ticks
- collisions
- scoring
- bird abilities
- win/loss rules
- builder state
- game state transitions
- builder save/load behavior

### Data Models

```text
modern_pygame/angrybirds/models.py
```

Defines the main game objects:

- birds
- pigs
- world bodies
- levels
- runtime game state

### Rendering and Input

```text
modern_pygame/angrybirds/pygame_client.py
```

Handles the playable interface:

- drawing
- menus
- buttons
- overlays
- mouse input
- keyboard input
- builder UI
- playtest UI

### Level Serialization

```text
modern_pygame/angrybirds/levels.py
```

Handles:

- loading built-in levels
- converting levels to JSON
- rebuilding levels from JSON
- saving custom builder levels
- discovering numbered save slots

### Local Score Persistence

```text
modern_pygame/angrybirds/scores.py
```

Handles local SQLite high scores used by the Pygame game.

### Backend API

```text
modern_pygame/api/
```

Provides REST endpoints for saved levels and leaderboard scores.

### Tests

```text
modern_pygame/tests/
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

## 👩‍🍳 Design Decisions

### Why keep the original CMU Graphics version?

The original version is preserved in `legacy_cmu/` to show the starting point and avoid rewriting history.

### Why migrate to Pygame?

Pygame is a more recognizable standalone Python game framework. Migrating made the project easier to present as an independent software engineering project while keeping the original class version available.

### Why local-first?

The goal was to demonstrate software engineering skills without paid hosting or maintenance. SQLite stores data locally, FastAPI runs on localhost, and Docker packages the backend for reproducible local execution.

### Why separate the API from the game?

The Pygame game can run on its own, while the FastAPI backend demonstrates REST API and database-backed persistence. Keeping them separate avoids overcomplicating the game loop.

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

This project was built for learning purposes. The artwork is not original.

- Angry Birds logo image from the Angry Birds Wiki
- Bird, pig, block, background, star, and UI sprites adapted from GitHub user `estevaofon`'s Angry Birds Python resources
