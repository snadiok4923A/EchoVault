"""Game engine and maze generation for EchoVault."""
from __future__ import annotations
import random
from collections import deque

WALL, FLOOR = "#", " "
PLAYER, SHARD, EXIT, UNKNOWN = "@", "*", "O", "?"

def generate_maze(width=21, height=13, seed=None):
    """Generate a connected maze using randomized depth-first carving."""
    width = max(9, width if width % 2 else width - 1)
    height = max(7, height if height % 2 else height - 1)
    rng = random.Random(seed)
    grid = [[WALL for _ in range(width)] for _ in range(height)]
    start = (1, 1)
    grid[1][1] = FLOOR
    stack = [start]
    while stack:
        x, y = stack[-1]
        choices = []
        for dx, dy in ((0, -2), (2, 0), (0, 2), (-2, 0)):
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and grid[ny][nx] == WALL:
                choices.append((nx, ny, dx, dy))
        if not choices:
            stack.pop()
            continue
        nx, ny, dx, dy = rng.choice(choices)
        grid[y + dy // 2][x + dx // 2] = FLOOR
        grid[ny][nx] = FLOOR
        stack.append((nx, ny))
    return grid

def reachable(grid, start):
    h, w = len(grid), len(grid[0])
    seen = {start}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nxt = (x+dx,y+dy)
            nx, ny = nxt
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] != WALL and nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return seen

class EchoVault:
    def __init__(self, width=21, height=13, seed=None, memory=45, shard_count=5):
        self.width = max(9, width if width % 2 else width - 1)
        self.height = max(7, height if height % 2 else height - 1)
        self.seed = seed
        self.rng = random.Random(seed)
        self.grid = generate_maze(self.width, self.height, seed)
        self.player = (1, 1)
        cells = list(reachable(self.grid, self.player))
        cells.remove(self.player)
        self.rng.shuffle(cells)
        self.exit = max(cells, key=lambda p: abs(p[0]-1)+abs(p[1]-1))
        self.shards = set(cells[:min(shard_count, max(0, len(cells)-1))])
        self.shards.discard(self.exit)
        self.memory = memory
        self.max_memory = memory
        self.moves = 0
        self.seen = {self.player}
        self.status = "playing"
        self._reveal_nearby()

    def _reveal_nearby(self):
        x, y = self.player
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                p = (x+dx, y+dy)
                if 0 <= p[0] < self.width and 0 <= p[1] < self.height:
                    self.seen.add(p)

    def move(self, direction):
        if self.status != "playing":
            return "finished"
        directions = {"up":(0,-1), "down":(0,1), "left":(-1,0), "right":(1,0)}
        if direction not in directions:
            return "invalid"
        dx, dy = directions[direction]
        nx, ny = self.player[0]+dx, self.player[1]+dy
        if not (0 <= nx < self.width and 0 <= ny < self.height) or self.grid[ny][nx] == WALL:
            return "wall"
        self.player = (nx, ny)
        self.moves += 1
        self.memory -= 1
        self._reveal_nearby()
        message = "moved"
        if self.player in self.shards:
            self.shards.remove(self.player)
            self.memory = min(self.max_memory, self.memory + 9)
            message = "shard"
        if self.player == self.exit:
            self.status = "won"
            message = "won"
        elif self.memory <= 0:
            self.status = "lost"
            message = "lost"
        return message

    def render(self):
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                p = (x, y)
                if p == self.player:
                    char = PLAYER
                elif p not in self.seen:
                    char = UNKNOWN
                elif p == self.exit:
                    char = EXIT
                elif p in self.shards:
                    char = SHARD
                else:
                    char = self.grid[y][x]
                row.append(char)
            rows.append("".join(row))
        return "\n".join(rows)
