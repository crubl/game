# main.py
import subprocess
import sys
from game import Game

if __name__ == "__main__":
    # subprocess.run([sys.executable, "game.py"])
    game = Game()
    game.run()