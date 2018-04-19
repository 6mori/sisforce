import pygame as pg
from pygame.sprite import Sprite

from .. import constants as c

class Sword(Sprite):
    def __init__(self, owner, damage):
        super().__init__()

        self.rect = pg.Rect((0, 0), (c.BULLET_WIDTH, c.BULLET_HEIGHT))
        self.owner = owner
        self.damage = damage
        self.creat_time = 0.0
        self.is_finished = False

        # For test
        self.color = c.BLUE

    def update(self):
        pass

