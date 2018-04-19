from . import tools, setup
from .states import gaming, menu
from . import constants as c

def main():
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {
        #c.MENU: menu.Menu(),
        c.GAMING: gaming.Gaming()
    }

    run_it.setup_states(state_dict, c.GAMING)
    run_it.main()