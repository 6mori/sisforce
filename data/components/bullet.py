import pygame as pg
from pygame.sprite import Sprite

from .. import constants as c

class Bullet(Sprite):
    def __init__(self, owner, damage, facing_right, bullet_style):
        super().__init__()

        #加载子弹图片并设置子弹大小
        self.image=pg.transform.scale(pg.image.load('images/bullet/'+bullet_style+'/0.png'),c.BULLET_SIZE)
        if not facing_right:
            self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

        self.HP = 1

        self.owner = owner
        self.damage = damage
        self.x_vel = 0
        self.y_vel = 0
        self.x = 0
        self.y = 0


    def set_x(self):
        self.x = float(self.rect.x)


    def update(self):
        self.rect.x += round(self.x_vel)
        self.rect.y += round(self.y_vel)

    def blitme(self,screen):
        screen.blit(self.image, self.rect)
