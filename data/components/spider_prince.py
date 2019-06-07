from . import shooter
from .. import constants as c
from . import skill_attack


class Spider_prince(shooter.Shooter):
    def __init__(self):
        super().__init__()

        self.bullet_damage = 20
        self.MP = 3
        self.name = c.SPIDER_PRINCE
        self.max_HP = c.MAX_HP[self.name]
        self.HP = self.max_HP

    def skill(self, action_group):
        super().skill('Spider_prince', 8, 'gif')
        # 发射地波
        if self.skill_counter == 1 or self.skill_counter == 2 * c.SKILL_SPEED[
            c.SPIDER_PRINCE] or self.skill_counter == 4 * c.SKILL_SPEED[c.SPIDER_PRINCE] or self.skill_counter == 6 * \
                c.SKILL_SPEED[c.SPIDER_PRINCE]:
            attack = skill_attack.Skill_attack(self.player_num, 100, c.RIGHT, 'skull',
                                               c.SPIDER_PRINCE)
            attack.x_vel = c.BULLET_VEL // 2
            attack.rect.left = self.rect.right
            attack.rect.bottom = self.rect.bottom
            action_group.add(attack)

            attack2 = skill_attack.Skill_attack(self.player_num, 100, c.LEFT, 'skull',
                                                c.SPIDER_PRINCE)
            attack2.x_vel = -c.BULLET_VEL // 2
            attack2.rect.right = self.rect.left
            attack2.rect.bottom = self.rect.bottom
            action_group.add(attack2)

    def action(self, action_group):
        super().action(c.SPIDER_PRINCE, 5, 'gif')
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
        super().setup_character_image_initial(c.SPIDER_PRINCE, 'gif')

    def setup_character_image_stand(self, character_name, max_frame_number, postfix):
        super().setup_character_image_stand(c.SPIDER_PRINCE, 9, 'gif')

    def setup_character_image_walk(self, character_name, max_frame_number, postfix):
        super().setup_character_image_walk(c.SPIDER_PRINCE, 4, 'gif')
