import pygame as pg
import random

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
        self.setup_position()
        self.setup_icon()
        self.setup_poster()
        #self.setup_BGM()


    def setup_background(self):
        self.background = pg.transform.scale(pg.image.load('images/%s' % c.CHOOSING_SCREEN), c.SCREEN_SIZE)
        self.background_rect = self.background.get_rect()


    def setup_cursor(self):
        #self.cursor_1 = self.creat_cursor(c.P1_CHOOSE_BASE, 50, 50)
        self.p1_offset = (0, 0)
        self.p1_confirm = False

        #self.cursor_2 = self.creat_cursor(c.P2_CHOOSE_BASE, 50, 50)
        self.p2_offset = (0, 0)
        self.p2_confirm = False


    def setup_position(self):
        self.pos2Chara = {}
        x = y = 0
        for character_name in c.CHARACTERS:
            self.pos2Chara[(x, y)] = character_name
            x += 50
            if x > 100:
                x = 0
                y += 50


    def setup_icon(self):
        self.chara_icon = {}
        for character_name in c.CHARACTERS:
            self.chara_icon[character_name] = [
                pg.transform.scale(pg.image.load('images/icons/%s.png' % (character_name)), (50, 50)),
                pg.transform.scale(pg.image.load('images/icons/%s_unselect.png' % (character_name)), (50, 50))]


    def setup_poster(self):
        self.chara_poster = {}
        for character_name in c.CHARACTERS:
            self.chara_poster[character_name] = [
                pg.transform.scale(pg.image.load('images/posters/%s.png' % (character_name)), c.HALF_SCREEN_SIZE),
                pg.transform.flip(pg.transform.scale(pg.image.load('images/posters/%s.png' % (character_name)), c.HALF_SCREEN_SIZE), True, False),
                ]


    '''def creat_cursor(self, pos, height, width):
        cursor = pg.sprite.Sprite()
        cursor.image = pg.Surface([height, width])
        # self.cursor.image.set_colorkey(c.BLACK)
        cursor.rect = cursor.image.get_rect()
        cursor.rect.x = pos[0]
        cursor.rect.y = pos[1]
        return cursor'''


    def update(self, surface, keys, current_time):
        self.current_time = current_time
        self.game_info[c.CURRENT_TIME] = self.current_time
        #self.update_cursor()
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
            if not self.p1_confirm:
                if event.key in P1_input_list.keys():
                    command = P1_input_list[event.key]
                    if command == c.CONFIRM:
                        self.p1_confirm = True
                    else:
                        next_pos = tuple(
                            [cur + off for cur, off in zip(self.p1_offset, tools.direct2pos[command])])
                        if next_pos in self.pos2Chara.keys():
                            self.p1_offset = next_pos

            if not self.p2_confirm:
                if event.key in P2_input_list.keys():
                    command = P2_input_list[event.key]
                    if command == c.CONFIRM:
                        self.p2_confirm = True
                    else:
                        next_pos = tuple(
                            [cur + off for cur, off in zip(self.p2_offset, tools.direct2pos[command])])
                        if next_pos in self.pos2Chara.keys():
                            self.p2_offset = next_pos

        if self.p1_confirm and self.pos2Chara[self.p1_offset] == c.RANDOM:
            times = random.randint(0, len(c.CHARACTERS)-1)
            for pos in self.pos2Chara.keys():
                if times == 0:
                    self.p1_offset = pos
                times -= 1

        if self.p2_confirm and self.pos2Chara[self.p2_offset] == c.RANDOM:
            times = random.randint(0, len(c.CHARACTERS)-1)
            for pos in self.pos2Chara.keys():
                if times == 0:
                    self.p2_offset = pos
                times -= 1


    '''def update_cursor(self):
        self.cursor_1.rect.x, self.cursor_1.rect.y = [base + off for base, off in
                                                      zip(c.P1_CHOOSE_BASE, self.cursor_1.offset)]
        self.cursor_2.rect.x, self.cursor_2.rect.y = [base + off for base, off in
                                                      zip(c.P2_CHOOSE_BASE, self.cursor_2.offset)]'''


    def blit_everything(self, surface):
        surface.blit(self.background, self.background_rect)
        surface.blit(self.chara_poster[self.pos2Chara[self.p1_offset]][0], pg.Rect((0, 0), c.HALF_SCREEN_SIZE))
        surface.blit(self.chara_poster[self.pos2Chara[self.p2_offset]][1],
                     pg.Rect((c.SCREEN_WIDTH / 2, 0), c.HALF_SCREEN_SIZE))

        for pos, chara in self.pos2Chara.items():
            surface.blit(self.chara_icon[chara][1], (c.P1_CHOOSE_BASE[0] + pos[0], c.P1_CHOOSE_BASE[1] + pos[1]))
            surface.blit(self.chara_icon[chara][1], (c.P2_CHOOSE_BASE[0] + pos[0], c.P2_CHOOSE_BASE[1] + pos[1]))

        surface.blit(self.chara_icon[self.pos2Chara[self.p1_offset]][0],
                     [base + off for base, off in zip(c.P1_CHOOSE_BASE, self.p1_offset)])
        surface.blit(self.chara_icon[self.pos2Chara[self.p2_offset]][0],
                     [base + off for base, off in zip(c.P2_CHOOSE_BASE, self.p2_offset)])


    def check_if_all_confirmed(self):
        if self.p1_confirm and self.p2_confirm:
            self.game_info[c.P1_CHARACTER] = self.pos2Chara[self.p1_offset]
            self.game_info[c.P2_CHARACTER] = self.pos2Chara[self.p2_offset]
            self.done = True

    def setup_BGM(self):
        pg.mixer.music.load('music/{}'.format(c.CHOOSING_BGM))
        pg.mixer.music.play()
