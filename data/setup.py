import os
import pygame as pg
from . import tools
from . import constants as c

ORIGINAL_CAPTION = c.ORIGINAL_CAPTION

pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(c.ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

MUSIC = tools.load_all_music(os.path.join("music"))
