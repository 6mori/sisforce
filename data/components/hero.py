import pygame as pg
from pygame.sprite import Sprite

from .. import constants as c


class Hero(Sprite):

    def __init__(self):
        super().__init__()
        self.heart = c.PLAYER_HEART
        # 大招次数  默认为3
        self.MP = 3

        # 默认贴图为Darling
        self.setup_character_image_initial(c.DARLING, 'png')
        self.player_num = 0

        self.state = c.STANDING

        self.commands = {
            c.ACTION: False,
            c.SKILL: False,
            c.JUMP: False,
            c.GO_LEFT: False,
            c.GO_RIGHT: False,
            c.GO_DOWN: False
        }

        self.setup_forces()
        self.setup_state_booleans()

        self.HP = 0
        self.max_HP = 0

        self.stand_counter = 0
        self.walk_counter = 0
        self.skill_counter = 0
        self.action_counter = 0

        self.vincible = True

        # for props
        self.acctime = 0
        self.invtime = 0

        self.freeze_time = 0.0

    def setup_character_image_initial(self, character_name='Darling', postfix='png'):
        self.image = pg.transform.scale(pg.image.load('images/%s/stand/0.%s' % (character_name, postfix)).convert(),
                                        c.CHARACTER_SIZE[character_name])
        self.image_right = self.image
        self.image_left = pg.transform.flip(self.image_right, True, False)
        self.rect = self.image.get_rect()
        self.show_xy = (self.rect.topleft)

    def setup_character_image_stand(self, character_name='Darling', max_frame_number='2', postfix='png'):
        if self.stand_counter // c.STAND_ANIMATION_SPEED[character_name] != (self.stand_counter - 1) // \
                c.STAND_ANIMATION_SPEED[character_name]:
            self.image_address_stand = 'images/' + character_name + '/stand/%d.%s' % (
            self.stand_counter // c.STAND_ANIMATION_SPEED[character_name], postfix)
        self.stand_counter += 1
        self.stand_counter %= max_frame_number * c.STAND_ANIMATION_SPEED[character_name]
        self.image_right = pg.transform.scale(pg.image.load(self.image_address_stand).convert(), c.CHARACTER_SIZE[character_name])
        self.image_left = pg.transform.flip(self.image_right, True, False)

    def setup_character_image_walk(self, character_name='Darling', max_frame_number='4', postfix='png'):
        if self.walk_counter // c.CHARACTER_MOVING_SPEED[character_name] != (self.walk_counter - 1) // \
                c.CHARACTER_MOVING_SPEED[character_name]:
            self.image_address_walk = 'images/' + character_name + '/walk/%d.%s' % (
            (self.walk_counter // c.CHARACTER_MOVING_SPEED[character_name]), postfix)
        self.walk_counter += 1
        self.walk_counter %= max_frame_number * c.CHARACTER_MOVING_SPEED[character_name]
        self.image_right = pg.transform.scale(pg.image.load(self.image_address_walk).convert(), c.CHARACTER_SIZE[character_name])
        self.image_left = pg.transform.flip(self.image_right, True, False)

    def setup_state_booleans(self):
        self.facing_right = True
        self.allow_jump = True
        self.allow_action = True
        self.allow_skill = True
        self.dead = False

    def setup_forces(self):
        self.x_vel = 0
        self.y_vel = 0
        self.max_x_vel = c.MAX_X_VEL
        self.max_y_vel = c.MAX_Y_VEL
        self.jump_vel = c.JUMP_VEL
        self.gravity = c.GRAVITY

    def update(self, keys, keybinding, game_info, action_group):
        self.show_xy = (self.rect.topleft)
        self.bind_keys(keys, keybinding)
        self.current_time = game_info[c.CURRENT_TIME]
        self.check_props_effect()
        self.handle_state(action_group)
        self.character_direction()

    def check_props_effect(self):
        if self.acctime:
            self.acctime -= 1
            if self.acctime <= 0:
                self.max_x_vel = c.MAX_X_VEL

        if self.invtime:
            pass

    def character_direction(self):
        if self.facing_right:
            self.image = self.image_right
        else:
            self.image = self.image_left

    def bind_keys(self, keys, keybinding):
        for command in self.commands.keys():
            if keys[keybinding[command]]:
                self.commands[command] = True
            else:
                self.commands[command] = False

    def handle_state(self, action_group):
        if self.state == c.STANDING:
            self.stand(action_group)
        if self.state == c.WALKING:
            self.walk(action_group)
        if self.state == c.JUMPING:
            self.jump(action_group)
        if self.state == c.FALLING:
            self.fall(action_group)
        if self.state == c.SKILLING:
            self.skill(action_group)
        if self.state == c.ACTIONING:
            self.action(action_group)
        if self.state == c.FREEZING:
            self.freeze()

    def stand(self, action_group):
        self.check_to_allow_jump()
        self.check_to_allow_action()
        self.check_to_allow_skill()

        self.setup_character_image_stand(c.DARLING, 2, 'png')

        self.x_vel = 0
        self.y_vel = 0

        if self.commands[c.ACTION]:
            if self.allow_action:
                self.state = c.ACTIONING
                return

        if self.commands[c.SKILL]:
            if self.allow_skill:
                self.state = c.SKILLING
                return

        if self.commands[c.GO_LEFT]:
            self.facing_right = False
            self.state = c.WALKING
            self.x_vel = -self.max_x_vel
        elif self.commands[c.GO_RIGHT]:
            self.facing_right = True
            self.state = c.WALKING
            self.x_vel = self.max_x_vel
        elif self.commands[c.JUMP]:
            if self.allow_jump:
                self.state = c.JUMPING
                self.y_vel = self.jump_vel
        else:
            self.state = c.STANDING

    def walk(self, action_group):
        self.check_to_allow_jump()
        self.check_to_allow_action()
        self.check_to_allow_skill()

        # 加载贴图
        self.setup_character_image_walk(c.DARLING, 2, 'png')

        if self.commands[c.ACTION]:
            if self.allow_action:
                self.state = c.ACTIONING

        if self.commands[c.SKILL]:
            if self.allow_skill:
                self.state = c.SKILLING

        if self.commands[c.JUMP]:
            if self.allow_jump:
                self.state = c.JUMPING
                self.y_vel = self.jump_vel

        if self.commands[c.GO_LEFT]:

            self.facing_right = False
            if self.x_vel >= 0:
                self.x_vel = -self.max_x_vel
            else:
                self.x_vel = 0

        elif self.commands[c.GO_RIGHT]:

            self.facing_right = True
            if self.x_vel <= 0:
                self.x_vel = self.max_x_vel
            else:
                self.x_vel = 0

        else:
            if self.y_vel == 0:
                self.state = c.STANDING
            self.x_vel = 0

    def jump(self, action_group):
        self.check_to_allow_action()
        self.check_to_allow_skill()

        self.allow_jump = False
        self.gravity = c.JUMP_GRAVITY
        self.y_vel += self.gravity

        if 0 <= self.y_vel < self.max_y_vel:
            self.gravity = c.GRAVITY
            self.state = c.FALLING

        if self.commands[c.ACTION]:
            if self.allow_action:
                self.state = c.ACTIONING
                return

        if self.commands[c.SKILL]:
            if self.allow_skill:
                self.state = c.SKILLING
                return

        if self.commands[c.GO_LEFT]:
            self.facing_right = False
            self.x_vel = -self.max_x_vel
        elif self.commands[c.GO_RIGHT]:
            self.facing_right = True
            self.x_vel = self.max_x_vel

        if not self.commands[c.JUMP]:
            self.gravity = c.GRAVITY
            self.state = c.FALLING

    def fall(self, action_group):
        self.check_to_allow_action()
        self.check_to_allow_skill()

        if self.y_vel < c.MAX_Y_VEL:
            self.y_vel += self.gravity

        if self.commands[c.ACTION]:
            if self.allow_action:
                self.state = c.ACTIONING
                return

        if self.commands[c.SKILL]:
            if self.allow_skill:
                self.state = c.SKILLING
                return

        if self.commands[c.GO_LEFT]:
            self.facing_right = False
            self.x_vel = -self.max_x_vel
        elif self.commands[c.GO_RIGHT]:
            self.facing_right = True
            self.x_vel = self.max_x_vel

    def action(self, character_name=None, max_frame_number=None, postfix=None, size=None):
        self.allow_action = False

        #self.y_vel = 0

        if size and self.action_counter == 0:
            self.origin_rect_action = self.rect
        if self.action_counter // c.ACTION_SPEED[character_name] != (self.action_counter - 1) // c.ACTION_SPEED[
            character_name]:
            self.action_image_address = 'images/%s/action/%d.%s' % (
                character_name, self.action_counter // c.ACTION_SPEED[character_name], postfix)

        self.action_counter += 1

        if size:
            self.image_right = pg.transform.scale(pg.image.load(self.action_image_address).convert(), size)
        else:
            self.image_right = pg.transform.scale(pg.image.load(self.action_image_address).convert(),
                                                  c.CHARACTER_SIZE[character_name])
        self.image_left = pg.transform.flip(self.image_right, True, False)
        image_rect = self.image_right.get_rect()
        if size:
            if self.name == c.GUAN_GONG:
                self.show_xy = (self.rect.centerx - (image_rect.right - image_rect.left) // 2, self.rect.y + 7)
            elif self.name == c.K:
                self.show_xy = (self.rect.centerx - (image_rect.right - image_rect.left) // 2, self.rect.y + 7)
            else:
                self.show_xy = (
                self.rect.centerx - (image_rect.right - image_rect.left) // 2, self.rect.y + size[1] // 2)
        else:
            self.show_xy = (self.rect.centerx - (image_rect.right - image_rect.left) // 2, self.rect.y)

        if self.action_counter == max_frame_number * c.ACTION_SPEED[character_name] - 1:
            self.action_counter = 0
            self.state = c.FALLING

    def skill(self, character_name=None, max_frame_number=None, postfix=None, size=None):
        if self.allow_skill:
            self.MP -= 1
        self.allow_skill = False

        self.x_vel = 0
        self.y_vel = 0

        self.action_image_address = 'images/%s/skill/%d.%s' % (
            character_name, self.skill_counter // c.SKILL_SPEED[character_name], postfix)

        self.skill_counter += 1
        self.skill_counter %= max_frame_number * c.SKILL_SPEED[character_name]
        if size:
            self.image_right = pg.transform.scale(pg.image.load(self.action_image_address).convert(), size)
        else:
            self.image_right = pg.transform.scale(pg.image.load(self.action_image_address).convert(),
                                                  c.CHARACTER_SIZE[character_name])
        self.image_left = pg.transform.flip(self.image_right, True, False)
        image_rect = self.image_right.get_rect()
        if self.name == c.K:
            self.show_xy = (self.rect.centerx - (image_rect.right - image_rect.left) // 2, self.rect.y -50)
        else:
            self.show_xy = (self.rect.centerx - (image_rect.right - image_rect.left) // 2, self.rect.y)

        if self.skill_counter == max_frame_number * c.SKILL_SPEED[character_name] - 1:
            self.state = c.FALLING
            #self.MP -= 1

    def freeze(self):
        self.x_vel = 0
        self.y_vel = 0
        self.allow_skill = False
        self.allow_action = False
        self.allow_jump = False

        if self.current_time - self.freeze_time >= c.RELIVE_TIME:
            print(self.current_time, self.freeze_time)
            self.state = c.FALLING
            self.reset_character_state()

    def check_to_allow_jump(self):
        if not self.commands[c.JUMP]:
            self.allow_jump = True

    def check_to_allow_action(self):
        if not self.commands[c.ACTION]:
            self.allow_action = True

    def check_to_allow_skill(self):
        if (not self.commands[c.SKILL]) and (self.MP > 0):
            self.allow_skill = True

    def reset_character_state(self):
        self.HP = self.max_HP
        self.MP = 3
        #self.heart -= 1
