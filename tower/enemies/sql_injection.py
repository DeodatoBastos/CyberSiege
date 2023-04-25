import os
import pygame
from .enemies import Enemy
from tower.constants import IMAGE_SPRITES

class Sql_Injection(Enemy):
    def __init__(self, wave_level):
        super().__init__()
        self.name = "SQL Injection"
        self.money = 10 * int((1 + 0.1) ** wave_level)
        self.max_health = 100 * int((1 + 0.9) ** wave_level)
        self.health = self.max_health
        self.speed_increase *= (wave_level / 2 + 1)
        self.img = pygame.transform.scale(IMAGE_SPRITES[(False, False, "sql_injection")]
                                          , (64, 64))