import pygame as pg
from pygame.sprite import Sprite

from .. import constants as c


class Bullet(Sprite):
    def __init__(self, owner, damage, direction, bullet_style):
        super().__init__()

        self.type = c.BULLET
        # 加载子弹图片并设置子弹大小
        self.image = pg.transform.scale(pg.image.load('images/bullet/' + bullet_style + '/0.gif'), c.BULLET_SIZE)
        self.direction = direction
        self.handle_bullet_direction()

        self.owner = owner
        self.damage = damage
        self.x_vel = 0
        self.y_vel = 0

        self.HP = 1
        self.counter = 0

        self.rect = self.image.get_rect()
        self.penetration_mode = 1

    def update(self):
        self.rect.x += round(self.x_vel)
        self.rect.y += round(self.y_vel)

    def handle_bullet_direction(self):
        if self.direction == c.LEFT:
            self.image = pg.transform.rotate(self.image, 180)
        elif self.direction == c.UP:
            self.image = pg.transform.rotate(self.image, 90)
        elif self.direction == c.DOWN:
            self.image = pg.transform.rotate(self.image, 270)
        elif self.direction == c.RIGHT_UP:
            self.image = pg.transform.rotate(self.image, 45)
        elif self.direction == c.LEFT_UP:
            self.image = pg.transform.rotate(self.image, 135)
        elif self.direction == c.RIGHT_DOWN:
            self.image = pg.transform.rotate(self.image, 315)
        elif self.direction == c.LEFT_DOWN:
            self.image = pg.transform.rotate(self.image, 225)
