# 🐦 Angry Birds Physics Engine

A small Angry Birds-inspired physics game built in Python with CMU Graphics.

I built this as a learning project to practice object-oriented programming, projectile motion, collision physics, and event-driven game logic. The game includes premade levels, a slingshot launch system, destructible objects, bird abilities, scoring, and a builder mode where you can create your own level.

## 🍿 Demo

[![Angry Birds Physics Engine Demo](https://img.youtube.com/vi/O0r57TcT31w/maxresdefault.jpg)](https://www.youtube.com/watch?v=O0r57TcT31w)

Alternative link: https://youtu.be/O0r57TcT31w

## 📦 Technologies

- Python
- CMU Graphics
- Object-oriented programming
- Basic physics simulation

## 🦄 Features

Here’s what you can do in the game:

### 🎮 Play Classic Mode

Choose from premade levels and try to pop all the pigs by launching birds at different structures.

Each level has its own pigs, birds, objects, and score thresholds. You can earn one, two, or three stars depending on how much destruction you cause and how many birds you use.

### 🧱 Build Your Own Level

Builder Mode lets you create your own setup by placing birds, pigs, boxes, wheels, and columns onto the map.

Once the level is built, you can press play and test it directly in the game.

### 🎯 Launch Birds With a Slingshot

Click and drag a bird from the slingshot to aim. The farther you pull back, the stronger the launch.

Before releasing, the game shows a trajectory preview so you can see where the bird is expected to fly.

### 💥 Break Structures

The game has custom collision logic between birds, pigs, boxes, columns, and wheels.

Objects can fall, slide, rotate, roll, disappear, or damage other objects depending on what hits them and what material they are made of.

### ⚡ Use Bird Abilities

The yellow bird has a speed-up ability that can be activated mid-flight by pressing `Space`.

## 🎯 Controls

- Click a level button to start a premade level
- Click Builder Mode to create a custom level
- Drag a bird from the slingshot to aim
- Release the mouse to launch
- Press `Space` to activate the yellow bird ability
- Click the home button to return to the main menu

## 🧠 How the Code Is Organized

The project is mainly split into two files:

```text
angry-birds-physics-engine/
├── main.py          # Screens, level setup, drawing, input handling, and game loop
├── objects.py       # Bird/Object classes, gravity, collisions, movement, and rotation
├── images/          # Sprites and UI assets
├── requirements.txt # Python dependency list
└── README.md
