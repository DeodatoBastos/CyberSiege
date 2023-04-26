import os
import pygame
from .enemies import Enemy
from tower.constants import IMAGE_SPRITES

class Trojan(Enemy):
    def __init__(self, wave_level):
        super().__init__()
        self.name = "Trojan"
        self.money = 20 + 5 * wave_level
        self.max_health = 80 + 40 * wave_level
        self.health = self.max_health
        self.speed_increase = wave_level
        self.img = pygame.transform.scale(IMAGE_SPRITES[(False, False, "trojan")],
                                          (64, 64))
