from . import shooter
from .. import constants as c
import time
from . import skill_attack
import pygame as pg


class Ghost(shooter.Shooter):
    def __init__(self):
        super().__init__()

        self.bullet_damage = 30
        self.MP = 3
        self.invincible_time_counter = time.time()
        self.name = c.GHOST
        self.max_HP = c.MAX_HP[self.name]
        self.HP = self.max_HP

    def skill(self, action_group):
        super().skill(c.GHOST, 6, 'gif')
        if self.skill_counter == 6 * c.SKILL_SPEED[c.GHOST] - 1:
            self.vincible = False
            self.invincible_time_counter = time.time()
        if self.skill_counter == 1:
            if self.facing_right:
                attack = skill_attack.Skill_attack(self.player_num, 0, c.RIGHT, 'servent',
                                                   c.GHOST)
                attack.rect.right = self.rect.left
            else:
                attack = skill_attack.Skill_attack(self.player_num, 0, c.LEFT, 'servent',
                                                   c.GHOST)
                attack.rect.left = self.rect.right
            attack.rect.centery = self.rect.top
            action_group.add(attack)

    def action(self, action_group):
        super().action(c.GHOST, 6, 'gif')
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
        super().setup_character_image_initial(c.GHOST, 'gif')

    def setup_character_image_stand(self, character_name, max_frame_number, postfix):
        super().setup_character_image_stand(c.GHOST, 3, 'gif')

    def setup_character_image_walk(self, character_name, max_frame_number, postfix):
        super().setup_character_image_walk(c.GHOST, 4, 'gif')

    def update(self, keys, keybinding, game_info, action_group):
        super().update(keys, keybinding, game_info, action_group)
        if not self.vincible:
            if self.facing_right:
                attack = skill_attack.Skill_attack(self.player_num, 0, c.RIGHT, 'servent',
                                                   c.GHOST)
                attack.counter = attack.frame_numbers * attack.animation_speed - 2
                attack.rect.right = self.rect.left
            else:
                attack = skill_attack.Skill_attack(self.player_num, 0, c.LEFT, 'servent',
                                                   c.GHOST)
                attack.counter = attack.frame_numbers * attack.animation_speed - 2
                attack.rect.left = self.rect.right
            attack.rect.centery = self.rect.top
            action_group.add(attack)
        if time.time() - self.invincible_time_counter >= 5 and self.vincible == False:
            self.vincible = True
