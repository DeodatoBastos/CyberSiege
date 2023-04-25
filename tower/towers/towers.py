import math
import pygame
from constants import DESIRED_FPS

class Towers:
    damage: int
    recharge_time: int
    time: int
    cost: int
    upgrade_cost: int
    range: int
    level: int
    level_colors: "list[str]"

    def __init__(self):
        self.level = 1
        self.level_colors = ['#CCCCCCA6', '#00CED1A6', '#FF1493A6', '#FFD700A6']
    cost : int
    range : int
    last_bullet : "list[pygame.Surface,pygame.Rect]" 
    bullet_color : "tuple(int,int,int)"

    WIDTH = 4 #LARGURA DO LASER

    def distance(self, pos, en_x, en_y):
        return math.sqrt((pos[0] - en_x)**2 + (pos[1] - en_y)**2)

    def hit_enemies(self,screen, pos, enemies: list):
        if self.time > 0:
            self.time -= 1
            if (self.last_bullet != None):
                self.decrease_transparency(10)
                screen.blit(self.last_bullet[0],self.last_bullet[1])
                
            return enemies, 0
        self.last_bullet = None
        money = 0
        for enemy in enemies:
            distance = self.distance(pos, enemy.x-32, enemy.y-32)
            if self.range >= distance:
                self.time = self.recharge_time
                self.draw_bullet(pos,enemy.x-32,enemy.y-32)
                if enemy.hit(self.damage):
                    money = enemy.money
                    enemies.remove(enemy)
                break
        return enemies, money

    def sell_value(self):
        return int(0.9 * self.cost * ((1.6 ** self.level) - 1) / 0.6)

    def level_color(self):
        return self.level_colors[self.level - 1]

    def upgrade(self):
        self.level += 1
        self.damage *= int((1.50) ** self.level)
        self.recharge_time = int( self.recharge_time * (0.95) ** self.level)
        self.range *= int((1.15) ** self.level)
        self.upgrade_cost *= int((1.60) ** self.level)

    def is_upgradable(self, balance):
        return (balance >= self.upgrade_cost) and (self.level < len(self.level_colors))
    
    def draw_bullet(self, pos, en_x, en_y):
        d = self.distance(pos,en_x,en_y)
        img0 = pygame.Surface((d, self.WIDTH)).convert_alpha()
        img0.fill(self.bullet_color)
        img0.set_colorkey((0,0,0))
        rect0 = img0.get_rect()
        if en_x == pos[0]:
            angle = 90
        else:
            angle = -math.degrees(math.atan((en_y - pos[1])/(en_x - pos[0])))
        rect0.center = ((pos[0] + en_x)/2, (pos[1] + en_y)/2) 
        img1 = pygame.transform.rotate(img0, angle)
        rect1 = img1.get_rect()
        rect1.center = rect0.center
        self.last_bullet = [img1,rect1]
        print(angle)
        print(pos)
        print((en_x,en_y))
    
    def decrease_transparency(self, speed):
        if (self.last_bullet == None):
            return
        if self.last_bullet[0].get_alpha() >= speed:
            self.last_bullet[0].set_alpha(self.last_bullet[0].get_alpha() - speed)
        else:
            self.last_bullet[0].set_alpha(0)
            
    
    
    
