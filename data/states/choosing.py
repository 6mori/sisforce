import pygame as pg

from .. import tools, setup
from .. import constants as c

class Choosing(tools._State):
    def __init__(self):
        super(Choosing, self).__init__()


    def startup(self, current_time, persist):
        self.game_info = persist
        self.persist = self.game_info

        self.next = c.GAMING

        self.setup_background()
        self.setup_cursor()


    def setup_background(self):
        self.background = pg.transform.scale(pg.image.load('images/%s.png' % c.CHOOSING_SCREEN), c.SCREEN_SIZE)
        self.background_rect = self.background.get_rect()


    def setup_cursor(self):
        self.cursor_1 = self.creat_cursor(c.P1_CHOOSE_BASE, 50, 50)
        self.cursor_1.offset = (0, 0)
        self.cursor_1.confirm = False

        self.cursor_2 = self.creat_cursor(c.P2_CHOOSE_BASE, 50, 50)
        self.cursor_2.offset = (0, 0)
        self.cursor_2.confirm = False


    def creat_cursor(self, pos, height, width):
        cursor = pg.sprite.Sprite()
        cursor.image = pg.Surface([height, width])
        # self.cursor.image.set_colorkey(c.BLACK)
        cursor.rect = cursor.image.get_rect()
        cursor.rect.x = pos[0]
        cursor.rect.y = pos[1]
        return cursor


    def update(self, surface, keys, current_time):
        self.current_time = current_time
        self.game_info[c.CURRENT_TIME] = self.current_time
        self.update_cursor()
        self.blit_everything(surface)
        self.check_if_all_confirmed()


    def get_event(self, event):
        P1_input_list = {
            pg.K_w: c.UP,
            pg.K_s: c.DOWN,
            pg.K_a: c.LEFT,
            pg.K_d: c.RIGHT,
            pg.K_RETURN: c.CONFIRM
        }
        P2_input_list = {
            pg.K_UP: c.UP,
            pg.K_DOWN: c.DOWN,
            pg.K_LEFT: c.LEFT,
            pg.K_RIGHT: c.RIGHT,
            pg.K_KP_ENTER: c.CONFIRM
        }

        if event.type == pg.KEYDOWN:
            if self.cursor_1.confirm == False:
                if event.key in P1_input_list.keys():
                    command = P1_input_list[event.key]
                    if command == c.CONFIRM:
                        self.cursor_1.confirm = True
                    else:
                        next_pos = tuple(
                            [cur + off for cur, off in zip(self.cursor_1.offset, tools.direct2pos[command])])
                        if next_pos in tools.pos2Chara.keys():
                            self.cursor_1.offset = next_pos

            if self.cursor_2.confirm == False:
                if event.key in P2_input_list.keys():
                    command = P2_input_list[event.key]
                    if command == c.CONFIRM:
                        self.cursor_2.confirm = True
                    else:
                        next_pos = tuple(
                            [cur + off for cur, off in zip(self.cursor_2.offset, tools.direct2pos[command])])
                        if next_pos in tools.pos2Chara.keys():
                            self.cursor_2.offset = next_pos


    def update_cursor(self):
        self.cursor_1.rect.x, self.cursor_1.rect.y = [base + off for base, off in
                                                      zip(c.P1_CHOOSE_BASE, self.cursor_1.offset)]
        self.cursor_2.rect.x, self.cursor_2.rect.y = [base + off for base, off in
                                                      zip(c.P2_CHOOSE_BASE, self.cursor_2.offset)]


    def blit_everything(self, surface):
        surface.blit(self.background, self.background_rect)
        surface.blit(self.cursor_1.image, self.cursor_1.rect)
        surface.blit(self.cursor_2.image, self.cursor_2.rect)


    def check_if_all_confirmed(self):
        if self.cursor_1.confirm and self.cursor_2.confirm:
            self.game_info[c.P1_CHARACTER] = tools.pos2Chara[self.cursor_1.offset]
            self.game_info[c.P2_CHARACTER] = tools.pos2Chara[self.cursor_2.offset]
            self.done = True