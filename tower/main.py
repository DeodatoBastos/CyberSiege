# Local imports
from tower.TowerGame import TowerGame

# External imports
import pygame


if __name__ == "__main__":

    game = TowerGame.create()
    game.start_game()
