import os
import pygame
from .enemies import Enemy
from tower.constants import IMAGE_SPRITES

class DDOS(Enemy):
    def __init__(self, wave_level):
        super().__init__()
        self.name = "DDOS"
        self.money = 10 + 5 * wave_level
        self.max_health = 40 + 10 * wave_level
        self.health = self.max_health
        self.speed_increase = 1 + wave_level
        self.img = pygame.transform.scale(IMAGE_SPRITES[(False, False, "ddos")], 
                                          (64, 64))