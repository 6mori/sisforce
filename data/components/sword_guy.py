import pygame as pg

from .. import constants as c
from . import character
from . import sword


class Sword_guy(character.Character):
    def __init__(self, player_num):
        super(Sword_guy, self).__init__()

        self.sword_damage = c.P1_DAMAGE
        self.player_num = player_num
        self.HP = 10


    def action(self, action_group):
        self.allow_action = False
        '''
        if self.player_num == 1:
            firing_bullet = bullet.Bullet(self.name, self.bullet_damage, self.facing_right, 'flamebow')
        else:
            firing_bullet = bullet.Bullet(self.name, self.bullet_damage, self.facing_right, 'freezebow')
        '''
        cutting_sword = sword.Sword(self.name, self.sword_damage)
        if self.facing_right:
            cutting_sword.rect.left = self.rect.right
        else:
            cutting_sword.rect.right = self.rect.left

        cutting_sword.rect.centery = self.rect.centery-23

        action_group.add(cutting_sword)