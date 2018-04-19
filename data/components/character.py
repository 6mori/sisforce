import pygame as pg
from pygame.sprite import Sprite

from .. import tools
from .. import constants as c

class Character(Sprite):

    def __init__(self):
        super().__init__()

        self.image = pg.transform.scale(pg.image.load('images/m_shoter/stand/dnf_s.png'),c.CHARACTER_SIZE)
        self.image_right = self.image
        self.image_left = pg.transform.flip(self.image_right, True, False)
        self.rect = self.image.get_rect()

        self.state = c.STAND

        self.commands = {
            'action': False,
            'skill': False,
            'jump' : False,
            'left' : False,
            'right': False,
            'down' : False
        }

        self.setup_forces()
        self.setup_state_booleans()

        self.HP = 0

        self.walk_counter=0
        self.skill_counter=0


    def setup_state_booleans(self):
        self.facing_right = True
        self.allow_jump = True
        self.allow_action = True
        self.allow_skill = True
        self.dead = False
        #self.skill_done = False


    def setup_forces(self):
        self.x_vel = 0
        self.y_vel = 0
        self.max_x_vel = c.MAX_X_VEL
        self.max_y_vel = c.MAX_Y_VEL
        self.jump_vel = c.JUMP_VEL
        self.gravity = c.GRAVITY


    def update(self, keys, keybinding, game_info, action_group):
        self.bind_keys(keys, keybinding)
        self.current_time = game_info[c.CURRENT_TIME]
        # self.character_direction()
        self.handle_state(action_group)
        self.character_direction()
        # self.character_direction()
        #self.check_for_special_statle()
        #self.animation()

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
        if self.state == c.STAND:
            self.stand(action_group)
        elif self.state == c.WALK:
            self.walk(action_group)
        elif self.state == c.JUMP:
            self.jump(action_group)
        elif self.state == c.FALL:
            self.fall(action_group)
        elif self.state == c.SKILL:
            self.skill()



    def stand(self, action_group):
        self.check_to_allow_jump()
        self.check_to_allow_action()
        self.check_to_allow_skill()

        self.image_right = pg.transform.scale(pg.image.load('images\m_shoter\stand\dnf_s.png'), c.CHARACTER_SIZE)
        self.image_left = pg.transform.flip(self.image_right, True, False)

        self.x_vel = 0
        self.y_vel = 0

        if self.commands['action']:
            if self.allow_action:
                self.action(action_group)

        if self.commands['skill']:
            if self.allow_skill:
                self.state = c.SKILL
                return

        if self.commands['left']:
            self.facing_right = False
            self.state = c.WALK
            self.x_vel = -self.max_x_vel
        elif self.commands['right']:
            self.facing_right = True
            self.state = c.WALK
            self.x_vel = self.max_x_vel
        elif self.commands['jump']:
            if self.allow_jump:
                self.state = c.JUMP
                self.y_vel = self.jump_vel
        else:
            self.state = c.STAND


    def walk(self, action_group):
        self.check_to_allow_jump()
        self.check_to_allow_action()
        self.check_to_allow_skill()

        #加载贴图
        image_address='images\m_shoter\walk\dnf_w_%d.png'%(self.walk_counter//c.CHARACTER_MOVING_SPEED)
        self.walk_counter+=1
        self.walk_counter%=4*c.CHARACTER_MOVING_SPEED
        self.image_right= pg.transform.scale(pg.image.load(image_address),c.CHARACTER_SIZE)
        self.image_left = pg.transform.flip(self.image_right, True, False)

        if self.commands['action']:
            if self.allow_action:
                self.action(action_group)

        if self.commands['skill']:
            if self.allow_skill:
                self.state = c.SKILL

        if self.commands['jump']:
            if self.allow_jump:
                self.state = c.JUMP
                self.y_vel = self.jump_vel

        if self.commands['left']:

            self.facing_right = False
            if self.x_vel >= 0:
                self.x_vel = -self.max_x_vel
            else:
                self.x_vel = 0

        elif self.commands['right']:

            self.facing_right = True
            if self.x_vel <= 0:
                self.x_vel = self.max_x_vel
            else:
                self.x_vel = 0

        else:
            if self.y_vel == 0:
                self.state = c.STAND
            self.x_vel = 0

    def jump(self, action_group):
        self.check_to_allow_action()
        self.check_to_allow_skill()

        self.allow_jump = False
        self.gravity = c.JUMP_GRAVITY
        self.y_vel += self.gravity

        if self.y_vel >= 0 and self.y_vel < self.max_y_vel:
            self.gravity = c.GRAVITY
            self.state = c.FALL

        if self.commands['action']:
            if self.allow_action:
                self.action(action_group)

        if self.commands['skill']:
            if self.allow_skill:
                self.state = c.SKILL
                return

        if self.commands['left']:
            self.facing_right = False
            self.x_vel = -self.max_x_vel
        elif self.commands['right']:
            self.facing_right = True
            self.x_vel = self.max_x_vel

        if not self.commands['jump']:
            self.gravity = c.GRAVITY
            self.state = c.FALL


    def fall(self, action_group):
        self.check_to_allow_action()
        self.check_to_allow_skill()

        if self.y_vel < c.MAX_Y_VEL:
            self.y_vel += self.gravity

        if self.commands['action']:
            if self.allow_action:
                self.action(action_group)

        if self.commands['skill']:
            if self.allow_skill:
                self.state = c.SKILL

        if self.commands['left']:
            self.facing_right = False
            self.x_vel = -self.max_x_vel
        elif self.commands['right']:
            self.facing_right = True
            self.x_vel = self.max_x_vel


    def action(self, action_group):
        pass

    def skill(self):
        pass


    def check_to_allow_jump(self):
        if not self.commands['jump']:
            self.allow_jump = True


    def check_to_allow_action(self):
        if not self.commands['action']:
            self.allow_action = True

    def check_to_allow_skill(self):
        if not self.commands['skill']:
            self.allow_skill = True


    def blitme(self):
    #    self.screen.blit( self.image, self.rect )
        pass

    # for test
