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
    "background": "map01.png"
}

for sprite_index, sprite_name in SPRITES.items():
    img = import_image(sprite_name)
    for flipped_x in (True, False):
        for flipped_y in (True, False):
            new_img = pygame.transform.flip(img, flip_x=flipped_x, flip_y=flipped_y)
            IMAGE_SPRITES[(flipped_x, flipped_y, sprite_index)] = new_img

channels = {
    "footsteps": None,
    "turrets": None,
    "score": None,
}

for channel_id, channel_name in enumerate(channels):
    channels[channel_name] = pygame.mixer.Channel(channel_id)
    # Configure the volume here.
    channels[channel_name].set_volume(1.0)