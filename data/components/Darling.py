from . import shooter
from .. import constants as c
import pygame as pg


class Darling(shooter.Shooter):
    def __init__(self):
        super().__init__()

        self.name = c.DARLING
        self.bullet_damage = 20
        self.max_HP = c.MAX_HP[self.name]
        self.HP = self.max_HP


    def skill(self, action_group):
        super().skill('Darling', 16, 'gif')
        self.wild_shot_bullets(action_group)

    def action(self, action_group):
        self.allow_action = False
        # 子弹类型
        if self.facing_right:
            firing_bullet = self.get_bullet_type('Darling', c.RIGHT)
        else:
            firing_bullet = self.get_bullet_type('Darling', c.LEFT)
        # 子弹方向
        self.handle_bullet_direction(firing_bullet)
        # 子弹发射位置
        firing_bullet.rect.centery = self.rect.centery - 11
        # 子弹组
        action_group.add(firing_bullet)
        self.state = c.FALLING

    def setup_character_image_initial(self, character_name, postfix):
        super().setup_character_image_initial(c.DARLING, 'gif')

    def setup_character_image_stand(self, character_name, max_frame_number, postfix):
        super().setup_character_image_stand(c.DARLING, 2, 'gif')

    def setup_character_image_walk(self, character_name, max_frame_number, postfix):
        super().setup_character_image_walk(c.DARLING, 4, 'gif')

    def wild_shot_bullets(self, action_group):
        if not self.skill_counter % (c.SKILL_SPEED['Darling']):
            bullets = [self.get_bullet_type(c.DARLING, c.LEFT), self.get_bullet_type(c.DARLING, c.RIGHT),
                       self.get_bullet_type(c.DARLING, c.UP), self.get_bullet_type(c.DARLING, c.RIGHT_UP),
                       self.get_bullet_type(c.DARLING, c.LEFT_UP)]
            bullets[0].x_vel = -c.BULLET_VEL
            bullets[4].x_vel = -c.BULLET_VEL
            bullets[1].x_vel = c.BULLET_VEL
            bullets[3].x_vel = c.BULLET_VEL
            bullets[2].y_vel = -c.BULLET_VEL
            bullets[3].y_vel = -c.BULLET_VEL
            bullets[4].y_vel = -c.BULLET_VEL

            bullets[1].rect.left = self.rect.right
            bullets[3].rect.left = self.rect.right
            bullets[2].rect.centerx = self.rect.centerx
            bullets[0].rect.right = self.rect.left
            bullets[4].rect.right = self.rect.left
            for i in range(len(bullets)):
                bullets[i].rect.centery = self.rect.centery - 23
                if i >= 2:
                    bullets[i].rect.bottom = self.rect.top
                action_group.add(bullets[i])
