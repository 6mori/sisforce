import os
import pygame as pg

from . import constants as c

direct2pos = {
    c.RIGHT: (50, 0),
    c.LEFT: (-50, 0),
    c.UP: (0, -50),
    c.DOWN: (0, 50),
}

keybinding = [
    {
        c.ACTION: pg.K_j,
        c.SKILL: pg.K_l,
        c.JUMP: pg.K_w,
        c.GO_LEFT: pg.K_a,
        c.GO_RIGHT: pg.K_d,
        c.GO_DOWN: pg.K_s
    },
    {
        c.ACTION: pg.K_KP1,
        c.SKILL: pg.K_KP3,
        c.JUMP: pg.K_UP,
        c.GO_LEFT: pg.K_LEFT,
        c.GO_RIGHT: pg.K_RIGHT,
        c.GO_DOWN: pg.K_DOWN
    }
]

# 砖块种类
kindOfBrick = {
    'grass_left': {'name': 'images/bricks/grass_left', 'dur': 25,'movable':0},
    'grass_middle': {'name': 'images/bricks/grass_middle', 'dur': 25,'movable':0},
    'grass_right': {'name': 'images/bricks/grass_right', 'dur': 25,'movable':0},
    'grass_inside': {'name': 'images/bricks/grass_inside', 'dur': 25,'movable':0},
    'long_wood':{'name':'images/bricks/long_wood', 'dur': 50,'movable':0},
    'long_stone':{'name':'images/bricks/long_stone', 'dur': 10000,'movable':0},
    'cool_grass_left':{'name':'images/bricks/cool_grass_left','dur':25,'movable':0},
    'cool_grass_mid':{'name':'images/bricks/cool_grass_mid','dur':25,'movable':0},
    'cool_grass_right':{'name':'images/bricks/cool_grass_right','dur':25,'movable':0},
    'cool_grass_inside_left':{'name':'images/bricks/cool_grass_inside_left','dur':25,'movable':0},
    'cool_grass_inside_mid':{'name':'images/bricks/cool_grass_inside_mid','dur':25,'movable':0},
    'cool_grass_inside_right':{'name':'images/bricks/cool_grass_inside_right','dur':25,'movable':0},
    'left_grass': {'name':'images/bricks/left_grass','dur':25,'movable':0},
    'right_grass':{'name':'images/bricks/right_grass','dur':25,'movable':0},
    'water':{'name':'images/bricks/water','dur':10000,'movable':1,'frame':2},
    'fire':{'name':'images/bricks/fire','dur':50,'movable':0},
    'iron_up_left':{'name':'images/bricks/iron_up_left','dur':300,'movable':0},
    'iron_down_left':{'name':'images/bricks/iron_down_left','dur':300,'movable':0},
    'iron_up_right':{'name':'images/bricks/iron_up_right','dur':300,'movable':0},
    'iron_down_right': {'name': 'images/bricks/iron_down_right', 'dur': 300,'movable':0},
    'iron':{'name':'images/bricks/iron','dur':300,'movable':0},
    'ice':{'name':'images/bricks/ice','dur':50,'movable':0},
    'glass':{'name':'images/bricks/glass','dur':100,'movable':0},
    'broken_glass':{'name':'images/bricks/glass0','dur':50,'movable':0}
}

#背景种类
kindOfGround={
    'grass_surface':['grass_left', 'grass_middle', 'grass_right'],
    'grass_soil':['grass_inside', 'grass_inside', 'grass_inside'],
    'long_wood':['long_wood', 'long_wood', 'long_wood'],
    'long_stone':['long_stone', 'long_stone', 'long_stone'],
    'cool_grass_surface':['cool_grass_left','cool_grass_mid','cool_grass_right'],
    'cool_grass_soil':['cool_grass_inside_left','cool_grass_inside_mid','cool_grass_inside_right'],
    'air_grass':['left_grass','cool_grass_inside_mid','right_grass'],
    'water':['water','water','water'],
    'fire':['fire','fire','fire'],
    'iron':['iron_up_right','iron','iron_up_left'],
    'long_iron':['iron','iron','iron'],
    'ice':['ice','ice','ice'],
    'glass':['glass','glass','glass'],
 }

# 道具种类
kindOfProps = {
    'Prop_HP_potion': {'name': 'images/Prop_HP_potion.png', 'dur': 25},
    'Prop_MP_potion': {'name': 'images/Prop_MP_potion.png', 'dur': 25},
    'Prop_HP_Apple': {'name': 'images/Prop_HP_Apple.png', 'dur': 25},
    'Prop_HP_Ginseng': {'name': 'images/Prop_HP_Ginseng.png', 'dur': 25},
    'Prop_Shoe': {'name': 'images/shoe.png', 'dur': 25},
    'Prop_Corselet': {'name': 'images/Prop_Corselet.png', 'dur': 25},
}


class Control(object):
    ''' Control object for entire project '''

    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        self.caption = caption
        self.state_dict = {}
        self.state_name = None
        self.state = None

        self.font = pg.font.SysFont("arial", 24)



    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

        # For test
        persist = self.state.cleanup()
        self.state.startup(self.current_time, persist)


    def update(self):
        self.current_time = pg.time.get_ticks()
        #print(self.current_time)
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)



    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)
        self.state.previous = previous


    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.state.get_event(event)


    def show_fps(self):
        text_surface = self.font.render(str(int(self.clock.get_fps())), False, c.WHITE)
        self.screen.blit(text_surface, (c.SCREEN_WIDTH-24, c.SCREEN_HEIGHT-24))


    def main(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.show_fps()
            pg.display.update()
            self.clock.tick(c.FPS)
            #print(self.clock.get_fps())


class _State(object):
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.current_screen_bottom=c.SCREEN_HEIGHT
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def get_event(self, event):
        pass

    def startup(self, current_time, persistant):
        self.persist = persistant
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.persist

    def update(self, surface, keys, current_time):
        pass


def load_all_music(directory, accept=('.wav', '.mp3', '.ogg', '.mdi', '.flac')):
    songs = {}
    for song in os.listdir(directory):
        name, ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    #print(songs.values())
    return songs
