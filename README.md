# EchoVault — The Memory Maze

A unique little Python puzzle game: explore a shifting maze, collect echo shards, and escape before your memory runs out. Each move costs one memory point, and collecting shards restores it. The maze is generated from a seeded map so runs can be replayed.

## Features
- Procedurally generated maze with guaranteed connected paths
- Collect echo shards to restore memory
- Reach the portal to win before memory reaches zero
- Fog-of-war exploration and simple terminal visuals
- WASD or arrow-key controls
- Restart with a new maze seed
- Pure Python; no external packages required

## Requirements
Python 3.10+

## Run
```bash
python game.py
```

## Controls
- `W A S D` or arrow keys: move
- `R`: restart with a new maze
- `Q`: quit

## Game rules
- `@` is you, `*` is an echo shard, `O` is the exit, `#` is a wall.
- `?` is an unexplored tile; previously explored tiles remain visible.
- Every move consumes 1 memory point.
- Pick up shards to regain 8 memory points.
- Find the portal before memory reaches zero.

## Tests
```bash
python -m unittest discover -s tests -v
```

## License
MIT
