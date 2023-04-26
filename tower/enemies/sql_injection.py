import os
import pygame
from .enemies import Enemy
from tower.constants import IMAGE_SPRITES
from math import sqrt
class Sql_Injection(Enemy):
    def __init__(self, wave_level):
        super().__init__()
        self.name = "SQL Injection"
        self.money = int(10 + 15 * sqrt(wave_level))
        self.max_health = 70 + 30 * wave_level
        self.health = self.max_health
        self.speed_increase = 1 + wave_level * 2
        self.img = pygame.transform.scale(IMAGE_SPRITES[(False, False, "sql_injection")]
                                          , (64, 64))