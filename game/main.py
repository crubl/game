import sys
sys.dont_write_bytecode = True

from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()