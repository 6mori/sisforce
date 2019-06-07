from . import shooter
from .. import constants as c
from . import skill_attack
import pygame as pg


class Iccy(shooter.Shooter):
    def __init__(self):
        super().__init__()

        self.bullet_damage = 30
        self.MP = 5
        self.name = c.ICCY
        self.max_HP = c.MAX_HP[self.name]
        self.HP = self.max_HP

    def skill(self, action_group):
        super().skill(c.ICCY, 11, 'gif')
        if self.skill_counter == 1:
            if self.facing_right:
                attack = skill_attack.Skill_attack(self.player_num, 100, c.RIGHT, 'ice_flame',
                                                   c.ICCY)
                attack.rect.left = self.rect.right - 20
            else:
                attack = skill_attack.Skill_attack(self.player_num, 100, c.LEFT, 'ice_flame',
                                                   c.ICCY)
                attack.rect.right = self.rect.left - 180
            attack.rect.bottom = self.rect.top
            attack.penetration_mode = 4
            attack.damage = 2
            action_group.add(attack)

    def action(self, action_group):
        super().action(c.ICCY, 9, 'gif')
        if self.action_counter == 1:
            # 子弹类型
            if self.facing_right:
                firing_bullet = self.get_bullet_type(c.SPIDER_PRINCE, c.RIGHT)
            else:
                firing_bullet = self.get_bullet_type(c.SPIDER_PRINCE, c.LEFT)
            # 子弹方向
            self.handle_bullet_direction(firing_bullet)
            # 子弹发射位置
            firing_bullet.rect.centery = self.rect.centery
            # 子弹组
            action_group.add(firing_bullet)

    def setup_character_image_initial(self, character_name, postfix):
        super().setup_character_image_initial(c.ICCY, 'gif')

    def setup_character_image_stand(self, character_name, max_frame_number, postfix):
        super().setup_character_image_stand(c.ICCY, 8, 'gif')

    def setup_character_image_walk(self, character_name, max_frame_number, postfix):
        super().setup_character_image_walk(c.ICCY, 8, 'gif')

