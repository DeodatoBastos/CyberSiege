import os
import pygame
from .enemies import Enemy
from tower.constants import IMAGE_SPRITES
from math import sqrt

class DDOS(Enemy):
    def __init__(self, wave_level):
        super().__init__()
        self.name = "DDOS"
        self.money = int(10 + 5 * sqrt(wave_level))
        self.max_health = 40 + 10 * wave_level
        self.health = self.max_health
        self.speed_increase = 1 + wave_level*1.5
        self.img = pygame.transform.scale(IMAGE_SPRITES[(False, False, "ddos")], 
                                          (64, 64))