import pygame as pg
from pygame.sprite import Sprite

from .. import tools as t
from .. import constants as c

class Prop(Sprite):
    def __init__(self, x, y, kind, width=1, height=1):
        super().__init__()
        self.kind = kind
        self.image = pg.transform.scale(pg.image.load(t.kindOfProps[kind]['name']),
                                        (c.BRICK_WIDTH*width, c.BRICK_HEIGHT*height))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

        self.y_vel = 0
        self.state = c.FALLING


    def ActOnCharacters(self, character):
        if self.kind == 'Prop_HP_potion':
            character.HP = character.HP+1
        elif self.kind == 'Prop_HP_Apple.png':
            character.HP = character.HP + 1
        elif self.kind == 'Prop_HP_Ginseng.png':
            character.HP = character.HP + 2
        elif self.kind == 'Prop_MP_potion':
            character.MP = character.MP+1


    def update(self):
        if self.state == c.FALLING:
            if self.y_vel < c.PROP_MAX_Y_VEL:
                self.y_vel += c.GRAVITY

            self.rect.y += round(self.y_vel)