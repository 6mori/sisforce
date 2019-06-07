from . import tools, setup
from . import constants as c

from .states import main_menu
from .states import gaming
from .states import choosing
from .states import game_over

def main():
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {
        c.MAIN_MENU: main_menu.MainMenu(),
        c.CHOOSING: choosing.Choosing(),
        c.GAMING: gaming.Gaming(),
        c.GAME_OVER: game_over.GameOver()
    }
    run_it.setup_states(state_dict, c.MAIN_MENU)
    run_it.main()
