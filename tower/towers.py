import pygame
import os

class Towers:
    damage : int
    recharge_time : int
    cost : int
    range : int
    #Tem que ter um script pro ataque tbm


class antivirus(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "antivirus.png")),
    (64, 64))
    
    def __init__(self):
        super().__init__()
        self.damage = 30
        self.recharge_time = 1
        self.cost = 20
        self.range = 100

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

class twoFactorAuth(Towers):
    img = pygame.transform.scale(
    pygame.image.load(os.path.join("tower", "assets", "sprites", "2FA.png")),
    (64, 64))

    def __init__(self):
        super().__init__()
        self.damage = 5
        self.recharge_time = 2
        self.cost = 20
        self.range = 300
