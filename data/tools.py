
import pygame as pg

keybinding = [
    {
        'action': pg.K_j,
        'skill' : pg.K_l,
        'jump': pg.K_w,
        'left': pg.K_a,
        'right':pg.K_d,
        'down': pg.K_s
    },
    {
        'action': pg.K_KP1,
        'skill' : pg.K_KP3,
        'jump': pg.K_UP,
        'left': pg.K_LEFT,
        'right':pg.K_RIGHT,
        'down': pg.K_DOWN
    }
]

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

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

        # For test
        persist = self.state.cleanup()
        self.state.startup(self.current_time, persist, self.screen)

    def update(self):
        self.current_time = pg.time.get_ticks()
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

    def main(self):
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()


class _State(object):
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
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
