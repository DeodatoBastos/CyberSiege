import os
import pygame
from tower.towers.towers import Towers

class antivirus(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "antivirus.png")),
    (64, 64))
    
    def __init__(self):
        super().__init__()
        self.damage = 30
        self.recharge_time = 60
        self.cost = 20
        self.range = 100
        self.time = 0