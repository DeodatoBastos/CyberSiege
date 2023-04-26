import os
import pygame
from tower.towers.towers import Towers

class firewall(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "firewall.png")),
    (64, 64))
    
    def __init__(self):
        super().__init__()
        self.damage = 25
        self.recharge_time = 180
        self.cost = 75
        self.range = 60
        self.time = 0
        self.upgrade_cost = 125
        self.last_bullet = None
        self.bullet_color = (255,0,0) #RED

    def upgrade(self):
        self.level += 1

        if self.level == len(self.level_colors):
            factor = 2
        else:
            factor = 2

        self.damage += 20 * factor
        self.recharge_time -= 27 * factor
        self.upgrade_cost += 20 * factor
        self.range += 10 * factor

