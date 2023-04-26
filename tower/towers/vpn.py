import os
import pygame
from tower.towers.towers import Towers

class vpn(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "vpn.png")),
    (64, 64))
    
    def __init__(self):
        super().__init__()
        self.damage = 10
        self.recharge_time = 50
        self.cost = 100
        self.range = 144
        self.time = 0
        self.upgrade_cost = 125
        self.last_bullet = None
        self.bullet_color = (255,255,255) #WHITE

    def upgrade(self):
        self.level += 1

        if self.level == len(self.level_colors):
            factor = 2
        else:
            factor = 1

        self.damage += 10 * factor
        self.recharge_time /= 2
        self.upgrade_cost += 100 * factor
        self.range += 10 * factor

