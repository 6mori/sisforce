import pygame as pg
from pygame.sprite import Sprite

from .. import tools as t
from .. import constants as c


class Prop(Sprite):
    def __init__(self, x, y, kind, width=1, height=1):
        super().__init__()
        self.kind = kind
        self.image = pg.transform.scale(pg.image.load(t.kindOfProps[kind]['name']),
                                        (c.BRICK_WIDTH * width, c.BRICK_HEIGHT * height))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

        self.HP = 1000000000

        self.y_vel = 0
        self.state = c.FALLING

    def ActOnCharacters(self, character):
        if character.state != c.FREEZING:
            if self.kind == 'Prop_HP_potion':
                character.HP += 80
                if character.HP >= character.max_HP:
                    character.HP = character.max_HP
            elif self.kind == 'Prop_MP_potion':
                if character.MP < 6:
                    character.MP = character.MP + 1
            elif self.kind == 'Prop_Shoe':
                character.acctime = 120
                character.max_x_vel *= 2
            elif self.kind == 'Prop_Corselet':
                character.invtime = 120

    def update(self):
        if self.state == c.FALLING:
            if self.y_vel < c.PROP_MAX_Y_VEL:
                self.y_vel += c.GRAVITY

            self.rect.y += round(self.y_vel)


class Spline(Sprite):
    def __init__(self, x, y, HP, width=1, height=1):
        super().__init__()
        self.x = x
        self.y = y
        self.HP = HP
        self.height = height
        self.width = width
        self.origin_image = pg.transform.scale(pg.image.load('images/spline.png'),
                                        (c.BRICK_WIDTH * width, c.BRICK_HEIGHT * height // 2))
        self.image = self.origin_image
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def scale_change(self, current_HP):
        rate = current_HP / self.HP
        self.image = pg.transform.scale(self.image, ((int)(c.BRICK_WIDTH * self.width * rate), c.BRICK_HEIGHT // 2))
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

    def reset(self):
        self.image = self.origin_image
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y


class Spline_Space(Sprite):
    def __init__(self, x, y, width=1, height=1):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('images/spline_space.png'),
                                        (c.BRICK_WIDTH * width, c.BRICK_HEIGHT * height // 2))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y


class MPsphere(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('images/MPsphere.png'), (c.BRICK_WIDTH, c.BRICK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y


class Icon(Sprite):
    def __init__(self, x, y, charactor):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load("images/icons/%s.png"%(charactor)), (c.BRICK_WIDTH*2, c.BRICK_HEIGHT*2))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y