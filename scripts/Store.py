import pygame 
from pygame.locals import *

class Store(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        pygame.sprite.Sprite.__init__(self, groups)
        #* load images
        self.sprite = pygame.image.load("data/sprites/scenary/Store/store_2.png")
        self.image = self.sprite

        #* set rect
        self.pos = pos
        
        
        self.size = size
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topright = pos)
