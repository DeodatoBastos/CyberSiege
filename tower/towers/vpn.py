import os
import pygame
from tower.towers.towers import Towers

class vpn(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "vpn.png")),
    (64, 64))
    
    def __init__(self):
        super().__init__()
        self.damage = 40
        self.recharge_time = 270
        self.cost = 100
        self.range = 200
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

        self.damage += 20 * factor
        self.recharge_time -= 45 * factor
        self.upgrade_cost += 25 * factor
        self.range += 10 * factor

