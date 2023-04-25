import os
import pygame
from .enemies import Enemy
from tower.constants import IMAGE_SPRITES

class DDOS(Enemy):
    def __init__(self, wave_level):
        super().__init__()
        self.name = "DDOS"
        self.money = 15 * int((1 + 0.1) ** wave_level)
        self.max_health = 100 * int((1 + 0.9) ** wave_level)
        self.health = self.max_health
        self.speed_increase *= (wave_level / 2 + 1)
        self.img = pygame.transform.scale(IMAGE_SPRITES[(False, False, "ddos")], 
                                          (64, 64))