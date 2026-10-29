import unittest
from echovault.engine import EchoVault, generate_maze, reachable, WALL

class EchoVaultTests(unittest.TestCase):
    def test_maze_has_connected_path(self):
        grid = generate_maze(21, 13, seed=42)
        cells = sum(ch != WALL for row in grid for ch in row)
        self.assertGreater(cells, 20)
        self.assertEqual(len(reachable(grid, (1, 1))), cells)

    def test_wall_does_not_consume_memory(self):
        game = EchoVault(seed=12)
        game.player = (1, 1)
        game.grid[1][0] = WALL
        before = game.memory
        self.assertEqual(game.move("left"), "wall")
        self.assertEqual(game.memory, before)

    def test_move_consumes_memory(self):
        game = EchoVault(seed=7, memory=45)
        options = [d for d in ("up", "down", "left", "right")
                   if game.move(d) != "wall"]
        # Use a fresh game for a deterministic legal first move.
        game = EchoVault(seed=7, memory=45)
        direction = next(d for d in ("right", "down", "left", "up")
                         if game.grid[1 + {"up":-1,"down":1,"left":0,"right":0}[d]][1 + {"left":-1,"right":1,"up":0,"down":0}[d]] != WALL)
        before = game.memory
        game.move(direction)
        self.assertEqual(game.memory, before - 1)

    def test_shard_restores_memory(self):
        game = EchoVault(seed=2, memory=20, shard_count=1)
        target = next(iter(game.shards))
        # Place a shard on a reachable adjacent floor to isolate pickup behavior.
        game.player = (1, 1)
        game.shards = {(2, 1)}
        game.grid[1][2] = " "
        game.memory = 10
        self.assertEqual(game.move("right"), "shard")
        self.assertEqual(game.memory, 18)
        self.assertNotIn(target, game.shards)

    def test_exit_wins(self):
        game = EchoVault(seed=5)
        game.player = (game.exit[0]-1, game.exit[1])
        game.grid[game.exit[1]][game.exit[0]-1] = " "
        result = game.move("right")
        if result != "won":
            game.player = (game.exit[0], game.exit[1]-1)
            game.grid[game.exit[1]-1][game.exit[0]] = " "
            result = game.move("down")
        self.assertEqual(game.status, "won")

if __name__ == "__main__":
    unittest.main()
