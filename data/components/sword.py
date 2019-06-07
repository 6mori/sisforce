import pygame as pg
from pygame.sprite import Sprite

from .. import constants as c


class Sword(Sprite):
    def __init__(self, owner, damage,size=(50,20)):
        super().__init__()

        self.type = c.SWORD
        self.owner = owner
        self.damage = damage
        self.creat_time = 0.0
        self.is_finished = False

        self.image = pg.transform.scale(pg.image.load('images/sword.png'), size)
        self.rect = self.image.get_rect()
        # For test
        self.color = c.BLUE

    def update(self):
        self.kill()
