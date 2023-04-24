import math
import pygame

class Enemy:

    def __init__ (self):
        self.width = 64
        self.height = 64
        self.path = [(1, 63),(352, 64),(351, 94),(542, 95),(544, 63),(831, 63),(830, 222),(576, 224),(574, 351),(448, 352),(448, 223),(65, 224),(62, 384),(192, 382),(320, 510),(319, 574),(833, 576),(831, 375)]
        self.path_pos = 0
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.speed_increase = 2

        self.name = None
        self.img = None
        self.max_health = self.health = 100

    def draw(self, screen: pygame.Surface):
        """
        Draws the enemy with the given images
        :param win: surface
        :return: None
        """
        screen.blit(self.img, (self.x - self.img.get_width()/2,
                               self.y - self.img.get_height()*3/4))
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen: pygame.Surface):
        """
        draw health bar above enemy
        :param screen: surface
        :return: None
        """
        length = 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)

        pygame.draw.rect(screen, (255,0,0), (self.x-30, self.y-45, length, 10), 0)
        pygame.draw.rect(screen, (0, 255, 0), (self.x-30, self.y - 45, health_bar, 10), 0)

    def collide(self, X, Y):
        """
        Returns if position has hit enemy
        :param x: int
        :param y: int
        :return: Bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def aux_update(self, x2, y2):
        self.x = x2
        self.y = y2
        self.path_pos += 1

    def move(self):
        """
        Move enemy
        :return: None
        """

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (-10, 355)
        else:
            x2, y2 = self.path[self.path_pos+1]

        dirn = ((x2-x1)*2, (y2-y1)*2)
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length * self.speed_increase, dirn[1]/length * self.speed_increase)


        # if dirn[0] < 0 and not(self.flipped):
        #     self.flipped = True
        #     self.img = pygame.transform.flip(self.img, True, False)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))

        self.x = move_x
        self.y = move_y

        # Go to next point
        if dirn[0] >= 0: # moving right
            if dirn[1] >= 0: # moving down
                if self.x >= x2 and self.y >= y2:
                    self.aux_update(x2, y2)
            else:
                if self.x >= x2 and self.y <= y2:
                    self.aux_update(x2, y2)
        else: # moving left
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 and self.y >= y2:
                    self.aux_update(x2, y2)
            else:
                if self.x <= x2 and self.y <= y2:
                    self.aux_update(x2, y2)
    
    def hit(self, damage):
        """
        Returns if an enemy has died and removes one health
        each call
        :return: Bool
        """
        self.health -= damage
        if self.health <= 0:
            return True
        return False
