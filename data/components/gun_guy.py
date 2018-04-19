import pygame as pg

from .. import constants as c
from . import character
from . import bullet

class Gun_guy(character.Character):
    def __init__(self, player_num):
        super(Gun_guy, self).__init__()
        self.player_num = player_num
        self.bullet_damage = c.P1_DAMAGE
        self.HP = 10


    def action(self, action_group):
        self.allow_action = False
        if self.player_num == 1:
            firing_bullet = bullet.Bullet(self.name, self.bullet_damage,self.facing_right,'flamebow')
        else:
            firing_bullet = bullet.Bullet(self.name, self.bullet_damage, self.facing_right, 'freezebow')
        if self.facing_right:
            firing_bullet.x_vel = c.BULLET_VEL
            firing_bullet.rect.left = self.rect.right
        else:
            firing_bullet.x_vel = -c.BULLET_VEL
            firing_bullet.rect.right = self.rect.left

        firing_bullet.rect.centery = self.rect.centery-23

        action_group.add(firing_bullet)


    def skill(self):
        self.allow_skill = False

        action_image_address = 'images/m_shoter/skill/action/dnf_r_%d.png' % (self.skill_counter // c.CHARACTER_SKILL_SPEED)

        self.skill_counter += 1
        self.skill_counter %= 16 * c.CHARACTER_SKILL_SPEED
        self.image_right = pg.transform.scale(pg.image.load(action_image_address), c.CHARACTER_SIZE)
        self.image_left = pg.transform.flip(self.image_right, True, False)

        if self.skill_counter == 16 * c.CHARACTER_SKILL_SPEED-1:
            self.state = c.FALL





