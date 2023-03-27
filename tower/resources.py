import pygame
import importlib.resources


class TileSprite(pygame.sprite.Sprite):
    def __init__(self):
        # Image, rect are attributes
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color(0, 255, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 200)


def load(module_path: str, name: str):
    return importlib.resources.path(module_path, name)


def import_image(asset_name: str):
    with load("tower.assets.sprites", asset_name) as resource:
        return pygame.image.load(resource).convert_alpha()


def import_sound(asset_name: str):
    """
    Imports, as a sound effect, `asset_name`.
    """
    with load("tower.assets.audio", asset_name) as resource:
        return pygame.mixer.Sound(resource)
