import pygame
from tower.resources import import_image

DESIRED_FPS = 90
# Replace width and height with the desired size of the game window.
SCREENRECT = pygame.Rect(0, 0, 960, 640)
MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT = 1, 2, 3

SPRITES = {
    "antivirus": "antivirus.png",
    "firewall": "firewall.png",
    "2FA": "2FA.png",
    "vpn": "vpn.png",
    "ddos": "ddos.png",
    "sql_injection": "sql_injection.png",
    "malware": "malware.png",
    "trojan": "trojan.png",
    "map01": "map01.png",
    "menu": "menu.png",
    "play": "Play.png",
    "pause": "Pause.png",
    "red": "red_button.png",
    "green": "green_button.png",
    "heart": "heart.png",
    "coin": "GoldCoin.png",
}

IMAGE_SPRITES = {}

channels = {
    "footsteps": None,
    "turrets": None,
    "score": None,
}