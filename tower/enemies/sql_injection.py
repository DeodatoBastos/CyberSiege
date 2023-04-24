import os
import pygame
from .enemies import Enemy

class Sql_Injection(Enemy):
    def __init__(self, wave_level):
        super().__init__()
        self.name = "SQL Injection"
        self.money = 10 * int((1 + 0.1) ** wave_level)
        self.max_health = 100 * int((1 + 0.9) ** wave_level)
        self.health = self.max_health
        self.speed_increase *= (wave_level / 2 + 1)
        self.img = pygame.transform.scale(
        pygame.image.load(os.path.join("tower", "assets", "sprites", "sql_injection.png")),
        (64, 64))