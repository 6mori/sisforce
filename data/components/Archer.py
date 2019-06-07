from . import shooter
from .. import constants as c
from . import skill_attack


class Archer(shooter.Shooter):
    def __init__(self):
        super().__init__()

        self.bullet_damage = 5
        self.MP = 3
        self.name = c.ARCHER
        self.max_HP = c.MAX_HP[self.name]
        self.HP = self.max_HP

    # 大招
    def skill(self, action_group):
        super().skill(c.ARCHER, 7, 'gif')
        if self.skill_counter == 1:
            if self.facing_right:
                attack = skill_attack.Skill_attack(self.player_num, 100, c.RIGHT, 'dodge',
                                                   c.ARCHER)
                attack.rect.left = self.rect.right
                attack.x_vel = c.BULLET_VEL // 2
            else:
                attack = skill_attack.Skill_attack(self.player_num, 100, c.LEFT, 'dodge',
                                                   c.ARCHER)
                attack.rect.right = self.rect.left
                attack.x_vel = -c.BULLET_VEL // 2
            attack.rect.centery = self.rect.top
            attack.penetration_mode = 3  # 全穿透
            action_group.add(attack)

    # 发射弓箭
    def action(self, action_group):
        super().action(c.ARCHER, 5, 'gif')
        if self.action_counter == 1:
            # 子弹类型
            if self.facing_right:
                firing_bullet = self.get_bullet_type(c.ARCHER, c.RIGHT)
            else:
                firing_bullet = self.get_bullet_type(c.ARCHER, c.LEFT)
            # 子弹方向
            self.handle_bullet_direction(firing_bullet)
            # 子弹发射位置
            firing_bullet.rect.centery = self.rect.centery
            # 子弹组
            action_group.add(firing_bullet)

    def setup_character_image_initial(self, character_name, postfix):
        super().setup_character_image_initial(c.ARCHER, 'gif')

    def setup_character_image_stand(self, character_name, max_frame_number, postfix):
        super().setup_character_image_stand(c.ARCHER, 1, 'gif')

    def setup_character_image_walk(self, character_name, max_frame_number, postfix):
        super().setup_character_image_walk(c.ARCHER, 8, 'gif')
