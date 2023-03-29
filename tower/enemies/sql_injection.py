import os
import pygame
from .enemies import Enemy

class Sql_Injection(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "SQL Injection"
        self.money = 1
        self.max_health = 100
        self.health = self.max_health
        self.img = pygame.transform.scale(
        pygame.image.load(os.path.join("tower", "assets", "sprites", "sql_injection.png")),
        (64, 64))