import subprocess
import sys
from game import Game
sys.dont_write_bytecode = True

if __name__ == "__main__":
    game = Game()
    game.run()