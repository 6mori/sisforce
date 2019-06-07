from .. import constants as c
from . import hero
from . import bullet
import pygame as pg


class Shooter(hero.Hero):
    def __init__(self):
        super().__init__()

        self.bullet_damage = c.BULLET_DAMAGE
        self.max_HP = 500
        self.HP = self.max_HP

    def get_bullet_type(self, character_name, direction):
        # 默认为Darling
        if character_name == c.DARLING:
            if self.player_num == 0:
                return bullet.Bullet(self.player_num, self.bullet_damage, direction, 'flamebow')
            else:
                return bullet.Bullet(self.player_num, self.bullet_damage, direction, 'freezebow')
        elif character_name == c.SPIDER_PRINCE:
            if self.player_num == 0:
                return bullet.Bullet(self.player_num, self.bullet_damage, direction, 'flamebow')
            else:
                return bullet.Bullet(self.player_num, self.bullet_damage, direction, 'freezebow')
        elif character_name == c.ARCHER:
            return bullet.Bullet(self.player_num, self.bullet_damage, direction, 'zidan')
        else:  # 默认为Darling
            if self.player_num == 0:
                return bullet.Bullet(self.player_num, self.bullet_damage, direction, 'flamebow')
            else:
                return bullet.Bullet(self.player_num, self.bullet_damage, direction, 'freezebow')

    def handle_bullet_direction(self, Mybullet):
        if self.facing_right:
            Mybullet.x_vel = c.BULLET_VEL
            Mybullet.rect.left = self.rect.right
        else:
            Mybullet.x_vel = -c.BULLET_VEL
            Mybullet.rect.right = self.rect.left
