import pygame
from tower.constants import *

class button:
    def __init__(self, tower, x,y,width,height,resize, text=''):
        self.tower = tower
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = tower.imageStr
        self.resize = resize

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        #pygame.draw.rect(win, (255,0,0), (self.x,self.y,self.width,self.height),0)           ONLY USED TO DEBUG THE BUTTON HITBOX
    
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
            
        win.blit(pygame.transform.scale(IMAGE_SPRITES[(False, False, self.image)], (self.resize,self.resize)), (self.x,self.y))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False