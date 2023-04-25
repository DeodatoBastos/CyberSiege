import os
import pygame
from tower.towers.towers import Towers

class twoFactorAuth(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "2FA.png")),
    (64, 64))

    def __init__(self):
        super().__init__()
        self.damage = 40
        self.recharge_time = 60
        self.cost = 20
        self.range = 300
        self.time = 0
        self.upgrade_cost = int(self.cost * 1.60)
