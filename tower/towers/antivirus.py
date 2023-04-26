import os
import pygame
from tower.towers.towers import Towers

class antivirus(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "antivirus.png")),
    (64, 64))
    
    def __init__(self):
        super().__init__()
        self.damage = 20
        self.recharge_time = 120
        self.cost = 30
        self.range = 128
        self.time = 0
        self.upgrade_cost = 60
        self.last_bullet = None
        self.bullet_color = (0,0,255) #BLUE

    def upgrade(self):
        self.level += 1

        if self.level == len(self.level_colors):
            factor = 2
        else:
            factor = 1

        self.damage += 15 * factor
        self.recharge_time -= 18 * factor
        self.upgrade_cost += 50 * factor
        self.range += 15 * factor
