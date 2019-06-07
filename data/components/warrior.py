import pygame as pg

from .. import constants as c
from . import hero
from . import sword


class Warrior(hero.Hero):
    def __init__(self):
        super(Warrior, self).__init__()

        self.sword_damage = c.SWORD_DAMAGE
        self.max_HP = 500
        self.HP = self.max_HP

    def action(self, action_group, character_name, frame_nums, postfix, size=None,attack_size=None):
        super().action(character_name, frame_nums, postfix, size)
        if self.action_counter == 1:
            if attack_size:
                cutting_sword = sword.Sword(self.player_num, self.sword_damage,attack_size)
            else:
                cutting_sword = sword.Sword(self.player_num, self.sword_damage)
            if self.facing_right:
                cutting_sword.rect.left = self.rect.right + c.MAX_X_VEL
            else:
                cutting_sword.rect.right = self.rect.left - c.MAX_X_VEL

            cutting_sword.rect.centery = self.rect.centery
            action_group.add(cutting_sword)
