import os
import pygame
from .enemies import Enemy

class DDOS(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "DDOS"
        self.money = 15
        self.max_health = 100
        self.health = self.max_health
        self.img = pygame.transform.scale(
        pygame.image.load(os.path.join("tower", "assets", "sprites", "ddos.png")),
        (64, 64))