import os
import pygame
from tower.towers.towers import Towers

class firewall(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "firewall.png")),
    (64, 64))
    
    def __init__(self):
        super().__init__()
        self.damage = 10
        self.recharge_time = 1
        self.cost = 25
        self.range = 30