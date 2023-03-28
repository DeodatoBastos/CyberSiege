import pygame
from tower.resources import import_image

DESIRED_FPS = 60
# Replace width and height with the desired size of the game window.
SCREENRECT = pygame.Rect(0, 0, 960, 640)
MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT = 1, 2, 3

SPRITES = {
    # "game_logo": "game_logo.png",
    # "land": "land.png",
    # "road": "road.png",
    "background": "map01.png",
    "antivirus": "antivirus.png"
}

IMAGE_SPRITES = {}

channels = {
    "footsteps": None,
    "turrets": None,
    "score": None,
}