from . import warrior
from .. import constants as c
from . import sword


class K(warrior.Warrior):
    def __init__(self):
        super().__init__()

        self.sword_damage = 50
        self.name = c.K
        self.max_HP = c.MAX_HP[self.name]
        self.HP = self.max_HP

    def skill(self, action_group):
        super().skill(c.K, 21, 'gif', (60, 90))
        # 冲刺
        if self.facing_right:
            self.rect.x += 1
        else:
            self.rect.x -= 1
        self.rect.y -= 1
        cutting_sword = sword.Sword(self.player_num, self.sword_damage)
        if self.facing_right:
            cutting_sword.rect.left = self.rect.right + c.MAX_X_VEL
        else:
            cutting_sword.rect.right = self.rect.left - c.MAX_X_VEL

        cutting_sword.rect.centery = self.rect.centery
        action_group.add(cutting_sword)

    def action(self, action_group):
        super().action(action_group, c.K, 7, 'gif', (89 // 3, 103 // 3))

    def setup_character_image_initial(self, character_name, postfix):
        super().setup_character_image_initial(c.K, 'gif')

    def setup_character_image_stand(self, character_name, frame_number, postfix):
        super().setup_character_image_stand(c.K, 40, 'gif')

    def setup_character_image_walk(self, character_name, frame_number, postfix):
        super().setup_character_image_walk(c.K, 8, 'gif')
