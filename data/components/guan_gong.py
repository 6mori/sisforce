from . import warrior
from .. import constants as c


class Guan_gong(warrior.Warrior):
    def __init__(self):
        super().__init__()

        self.name = c.GUAN_GONG
        self.sword_damage = 100
        self.skill_damage = 100
        self.max_HP = c.MAX_HP[self.name]
        self.HP = self.max_HP

    def skill(self, action_group):
        super().skill(c.GUAN_GONG, 10, 'gif')
        self.vincible=False
        # 冲刺
        if self.facing_right:
            self.rect.x += 6
        else:
            self.rect.x -= 6
            if self.skill_counter == 10 * c.SKILL_SPEED[c.GUAN_GONG] - 1:
                self.vincible=True


    def action(self, action_group):
        super().action(action_group, c.GUAN_GONG, 6, 'gif', (192 // 3, 133 // 3),c.CHARACTER_SIZE[c.GUAN_GONG])

    def setup_character_image_initial(self, character_name, postfix):
        super().setup_character_image_initial(c.GUAN_GONG, 'gif')

    def setup_character_image_stand(self, character_name, frame_number, postfix):
        super().setup_character_image_stand(c.GUAN_GONG, 7, 'gif')

    def setup_character_image_walk(self, character_name, frame_number, postfix):
        super().setup_character_image_walk(c.GUAN_GONG, 6, 'gif')
