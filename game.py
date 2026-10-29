#!/usr/bin/env python3
"""EchoVault terminal game."""
import os
import random
import sys
import time
from echovault.engine import EchoVault

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def read_key():
    """Read one key without requiring Enter, using standard-library terminal support."""
    if os.name == "nt":
        import msvcrt
        key = msvcrt.getch()
        if key in (b"\x00", b"\xe0"):
            code = msvcrt.getch()
            return {b"H":"up", b"P":"down", b"K":"left", b"M":"right"}.get(code, "")
        return key.decode("utf-8", errors="ignore").lower()
    import tty, termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            seq = sys.stdin.read(2)
            return {"[A":"up", "[B":"down", "[D":"left", "[C":"right"}.get(seq, "")
        return ch.lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def main():
    seed = random.randrange(1, 1_000_000)
    game = EchoVault(seed=seed)
    message = "Find the portal. Shards restore memory."
    while True:
        clear()
        print("╔══════════════════════════════════════╗")
        print("║          E C H O V A U L T           ║")
        print("║            THE MEMORY MAZE           ║")
        print("╚══════════════════════════════════════╝")
        print(f"Memory: {game.memory:02d}/{game.max_memory}   Moves: {game.moves}   Shards left: {len(game.shards)}")
        print(f"Seed: {seed}  (R makes a new maze)")
        print()
        print(game.render())
        print()
        print("WASD / Arrow keys: move   R: restart   Q: quit")
        print(message)
        if game.status == "won":
            print(f"\nYOU ESCAPED! You made it in {game.moves} moves.")
            print("Press R for another maze or Q to quit.")
        elif game.status == "lost":
            print("\nYOUR MEMORY FADED. The maze swallowed your trail.")
            print("Press R to try again or Q to quit.")
        key = read_key()
        if key in ("q", "\x03"):
            break
        if key == "r":
            seed = random.randrange(1, 1_000_000)
            game = EchoVault(seed=seed)
            message = "New maze generated. Follow the echoes."
            continue
        if game.status != "playing":
            continue
        direction = {"w":"up", "s":"down", "a":"left", "d":"right"}.get(key, key)
        result = game.move(direction)
        message = {
            "wall":"A cold wall blocks your way.",
            "moved":"You hear the maze shift around you...",
            "shard":"Echo shard collected! +8 memory (capped at maximum).",
            "won":"The portal opens. You escaped!",
            "lost":"Your memory reached zero.",
            "invalid":"Use WASD or the arrow keys."
        }.get(result, message)
    print("Thanks for playing EchoVault!")

if __name__ == "__main__":
    main()
