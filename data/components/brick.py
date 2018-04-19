import pygame as pg
from pygame.sprite import Sprite

from .. import constants as c

class Brick(Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.rect = pg.Rect((x, y), (c.BRICK_WIDTH, c.BRICK_HEIGHT))

        #self.image = pygame.image.load('images/')
        #self.rect = self.image.get_rect()

        self.HP = c.BRICK_DUR

        # for test
        self.color = c.ORANGE

    #def update(self):
    def blitme(self):
        self.screen.blit( self.image, self.rect )

    # for test