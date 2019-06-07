import pygame as pg

from .. import tools, setup
from .. import constants as c


class GameOver(tools._State):
    def __init__(self):
        super(GameOver, self).__init__()

    def startup(self, current_time, persist):
        self.game_info = persist
        self.persist = self.game_info
        self.next = c.CHOOSING

        self.state = c.PLAY

        print(self.game_info)

        self.setup_background()
        #self.setup_cursor()
        self.setup_UI()
        self.setup_poster()

        # For test
        #self.quit = True


    def setup_UI(self):
        self.UI = {c.PLAY: [{'image': pg.transform.scale(pg.image.load('images/UI/once_more.png'), (150, 50))},
                            {'image': pg.transform.scale(pg.image.load('images/UI/once_more.png'), (180, 60))}],
                   c.QUIT: [{'image': pg.transform.scale(pg.image.load('images/UI/exit_game.png'), (150, 50))},
                            {'image': pg.transform.scale(pg.image.load('images/UI/exit_game.png'), (180, 60))}]}
        for state, k in zip(self.UI.keys(), range(0, 2)):
            for i in range(0, 2):
                rect = self.UI[state][i]['image'].get_rect()
                rect.centerx = c.SCREEN_WIDTH // 2
                rect.centery = 430 + 60 * k
                self.UI[state][i]['rect'] = rect
        self.Victory = pg.image.load('images/Victory.png')
        self.Defeated = pg.image.load('images/Defeated.png')


    def setup_background(self):
        self.background = pg.transform.scale(pg.image.load('images/%s' % c.RESULT_SCREEN), c.SCREEN_SIZE)
        self.background_rect = self.background.get_rect()


    def setup_poster(self):
        self.chara_poster = {}
        for character_name in c.CHARACTERS:
            self.chara_poster[character_name] = [
                pg.transform.scale(pg.image.load('images/posters/%s.png' % (character_name)), c.HALF_SCREEN_SIZE),
                pg.transform.flip(pg.transform.scale(pg.image.load('images/posters/%s.png' % (character_name)), c.HALF_SCREEN_SIZE), True, False),
                ]


    def setup_cursor(self):
        pass
        # self.cursor = pg.sprite.Sprite()
        # self.cursor.image = pg.Surface([c.TITLE_CURSOR_WIDTH, c.TITLE_CURSOR_HEIGHT])
        # # self.cursor.image.set_colorkey(c.BLACK)
        # self.cursor.rect = self.cursor.image.get_rect()
        # self.cursor.rect.x = 350
        # self.cursor.rect.y = 400
        # self.cursor.state = c.PLAY


    def update(self, surface, keys, current_time):
        self.current_time = current_time
        self.game_info[c.CURRENT_TIME] = self.current_time
        self.update_cursor(keys)
        self.blit_everything(surface)


    def update_cursor(self, keys):
        if self.state == c.PLAY:
            if keys[pg.K_DOWN]:
                self.state = c.QUIT
            if keys[pg.K_RETURN]:
                self.done = True
        elif self.state == c.QUIT:
            if keys[pg.K_UP]:
                self.state = c.PLAY
            if keys[pg.K_RETURN]:
                self.quit = True


    def blit_everything(self, surface):
        surface.blit(self.background, self.background_rect)
        surface.blit(self.chara_poster[self.game_info[c.P1_CHARACTER]][0], pg.Rect((0, 0), c.HALF_SCREEN_SIZE))
        surface.blit(self.chara_poster[self.game_info[c.P2_CHARACTER]][1],
                     pg.Rect((c.SCREEN_WIDTH / 2, 0), c.HALF_SCREEN_SIZE))
        #surface.blit(self.cursor.image, self.cursor.rect)
        for state in self.UI.keys():
            if state == self.state:
                surface.blit(self.UI[state][1]['image'], self.UI[state][1]['rect'])
            else:
                surface.blit(self.UI[state][0]['image'], self.UI[state][0]['rect'])
        if self.game_info[c.P1_HEART] == 0:
            surface.blit(self.Victory, (600, 40))
            surface.blit(self.Defeated, (0, 40))
        else:
            surface.blit(self.Victory, (0, 40))
            surface.blit(self.Defeated, (600, 40))