import os
import pygame
from tower.towers.towers import Towers

class firewall(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "firewall.png")),
    (64, 64))
    
    def __init__(self):
        super().__init__()
        self.damage = 60
        self.recharge_time = 120
        self.cost = 50
        self.range = 96
        self.time = 0
        self.upgrade_cost = 100
        self.last_bullet = None
        self.bullet_color = (255,0,0) #RED

    def upgrade(self):
        self.level += 1

        if self.level == len(self.level_colors):
            factor = 2
        else:
            factor = 1

        self.damage += 20 * factor
        self.recharge_time -= 25 * factor
        self.upgrade_cost += 120 * factor
        self.range += 10 * factor

