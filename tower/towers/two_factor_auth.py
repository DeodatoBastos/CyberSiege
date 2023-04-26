import os
import pygame
from tower.towers.towers import Towers

class twoFactorAuth(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "2FA.png")),
    (64, 64))

    def __init__(self):
        super().__init__()
        self.damage = 35
        self.recharge_time = 225
        self.cost = 60
        self.range = 150
        self.time = 0
        self.upgrade_cost = 150
        self.last_bullet = None
        self.bullet_color = (0,255,0) #GREEN

    def upgrade(self):
        self.level += 1

        if self.level == len(self.level_colors):
            factor = 2
        else:
            factor = 1

        self.damage += 15 * factor
        self.recharge_time -= 36 * factor
        self.upgrade_cost += 30 * factor
        self.range += 10 * factor
