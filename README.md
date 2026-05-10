# 🐦 Angry Birds Physics Engine

A small Angry Birds-inspired physics game built in Python with CMU Graphics.

I built this as a learning project to practice object-oriented programming, projectile motion, collision physics, and event-driven game logic. The game has premade levels, a slingshot launch system, destructible objects, bird abilities, scoring, and a builder mode where you can create your own level.

## 🍿 Demo

[![Angry Birds Physics Engine Demo](https://img.youtube.com/vi/O0r57TcT31w/maxresdefault.jpg)](https://www.youtube.com/watch?v=O0r57TcT31w)

Alternative link: https://youtu.be/O0r57TcT31w

## 🚦 How to Run

This project uses Python and CMU Graphics.

### 1. Clone the repo

```bash
git clone https://github.com/Danny625/angry-birds-physics-engine.git
cd angry-birds-physics-engine
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Go into the game folder

```bash
cd "Angry Birds"
```

### 4. Run the game

```bash
python main.py
```

The image assets need to stay inside `Angry Birds/images/` because the code loads sprites from that folder.

## 📦 Technologies

- Python
- CMU Graphics
- Object-oriented programming
- Basic physics simulation

## 🦄 Features

### 🎮 Classic Mode

Play through premade levels and try to pop all the pigs by launching birds at different structures.

Each level has its own birds, pigs, objects, and score thresholds. You can earn one, two, or three stars depending on how much destruction you cause and how many birds you use.

### 🧱 Builder Mode

Create your own level by placing birds, pigs, boxes, wheels, and columns onto the map.

Once the level is built, you can press play and test it directly in the game.

### 🎯 Slingshot + Trajectory Preview

Click and drag a bird from the slingshot to aim. The farther you pull back, the stronger the launch.

Before releasing, the game shows a trajectory preview so you can see where the bird is expected to fly.

### 💥 Collision Physics

The game has custom collision logic between birds, pigs, boxes, columns, and wheels.

Objects can fall, slide, rotate, roll, disappear, or damage other objects depending on what hits them and what material they are made of.

### ⚡ Bird Ability

The yellow bird has a speed-up ability that can be activated mid-flight by pressing `Space`.

## 🎯 Controls

- Click a level button to start a premade level
- Click Builder Mode to create a custom level
- Drag a bird from the slingshot to aim
- Release the mouse to launch
- Press `Space` to activate the yellow bird ability
- Click the home button to return to the main menu

## 🧠 Project Structure

The main game files are inside the `Angry Birds/` folder:

```text
angry-birds-physics-engine/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
└── Angry Birds/
    ├── main.py          # Screens, levels, drawing, input handling, and game loop
    ├── objects.py       # Bird/Object classes, gravity, collisions, movement, and rotation
    └── images/          # Sprites and UI assets
```

## 🧩 How It Works

At a high level, the game works like this:

1. The player chooses a premade level or opens Builder Mode.
2. The game loads birds, pigs, and objects into the current level.
3. The player drags a bird back from the slingshot.
4. The game calculates and previews the bird's trajectory.
5. When released, the bird follows that path frame by frame.
6. Collisions update object health, velocity, rotation, score, and win/loss state.
7. The level ends when all pigs are gone or the player runs out of birds.

### `main.py`

This file controls the overall game flow:

- App setup
- Home screen and level selection
- Premade level loading
- Builder Mode state
- Mouse and keyboard input
- Drawing the screen
- Updating the game each step
- Score, stars, and win/loss logic

### `objects.py`

This file defines the main game entities:

- `Bird` handles bird position, trajectory, flight, and abilities
- `Object` handles pigs, boxes, wheels, and columns
- Gravity, movement, friction, collisions, rotation, and rolling behavior live here

## 👩‍🍳 The Process

I started with the core Angry Birds mechanic: dragging a bird back from a slingshot and launching it across the screen.

Once the launch worked, I added a trajectory preview so aiming felt more playable. After that, I built the object system for birds, pigs, boxes, wheels, and columns. Each object needed to track its own position, velocity, material, health, and movement behavior.

The hardest part was collision handling. A bird hitting a pig is pretty simple, but a box falling onto another box, a wheel rolling after impact, or a column rotating after being hit all needed different rules. I ended up writing custom collision logic based on object type, material, position, and velocity.

After Classic Mode worked, I added Builder Mode so players could place their own objects and test custom levels. That made the project feel more like a small physics engine instead of just a fixed set of levels.

## 📚 What I Learned

- How to structure an interactive Python game around an event loop
- How to use classes to organize game entities and state
- How to model projectile motion and trajectory previews
- How messy collision logic can get when objects have different shapes, materials, and movement rules
- How to manage game state across menus, levels, scoring, win/loss screens, and Builder Mode

## 💭 How It Can Be Improved

If I were rebuilding this now, I would probably:

- Refactor the collision logic into smaller helper functions
- Store level layouts in JSON or config files instead of hardcoding them
- Add save/load support for Builder Mode levels
- Add more bird types and abilities
- Improve physics edge cases
- Add more levels and object materials
- Clean up the folder structure
- Add tests for smaller physics/helper functions

## 🎨 Asset Credits

This project was built for learning purposes. The artwork is not original.

- Angry Birds logo image from the Angry Birds Wiki
- Bird, pig, block, background, star, and UI sprites adapted from GitHub user `estevaofon`'s Angry Birds Python resources
