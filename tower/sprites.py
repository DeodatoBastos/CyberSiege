import pygame

class TileSprite(pygame.sprite.Sprite):
    def __init__(self):
        #Image, rect are attributes
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color(0,255,0,255))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 200)