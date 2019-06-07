import pygame as pg
from pygame.sprite import Sprite
from .. import tools as t
from .. import constants as c


class Brick(Sprite):

    def __init__(self, x, y, kind, width=1, height=1):  # width和height为砖块长宽
        super().__init__()
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.kind=kind
        self.HP = t.kindOfBrick[kind]['dur']
        self.rect = pg.Rect((0, 0), c.BRICK_SIZE)
        self.rect.left = self.x
        self.rect.top = self.y
        self.vincible = True


    # for test
    def ActOnCharacter(self,character):
        if self.kind=='fire' and character.HP > 0:
            character.HP -= c.FIRE_BRICK_DAMAGE
        if self.kind=='glass' or  self.kind=='broken_glass':
            self.HP-=1
            if self.HP==50:
                self.kind = 'broken_glass'
            if self.HP<=0:
                self.kill()