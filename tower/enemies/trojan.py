import os
import pygame
from .enemies import Enemy
from tower.constants import IMAGE_SPRITES
import math

class Trojan(Enemy):
    def __init__(self, wave_level):
        super().__init__()
        self.name = "Trojan"
        self.money = int(30 + 10 * math.sqrt(wave_level))
        self.max_health = 80 + 40 *math.log2(wave_level+1)* wave_level**1.5
        self.health = self.max_health
        self.speed_increase = 1 + wave_level/2.0
        self.img = pygame.transform.scale(IMAGE_SPRITES[(False, False, "trojan")],
                                          (64, 64))
