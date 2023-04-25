import os
import pygame
from tower.towers.towers import Towers

class vpn(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "vpn.png")),
    (64, 64))
    
    def __init__(self):
        super().__init__()
        self.damage = 5
        self.recharge_time = 20
        self.cost = 50
        self.range = 500
        self.time = 0
        self.upgrade_cost = int(self.cost * 1.60)
        self.last_bullet = None
        self.bullet_color = (255,255,255) #WHITE
