SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)

ORIGINAL_CAPTION = "Gayforce"

## COLORS ##

#            R    G    B
GRAY         = (100, 100, 100)
NAVYBLUE     = ( 60,  60, 100)
WHITE        = (255, 255, 255)
RED          = (255,   0,   0)
GREEN        = (  0, 255,   0)
FOREST_GREEN = ( 31, 162,  35)
BLUE         = (  0,   0, 255)
SKY_BLUE     = ( 39, 145, 251)
YELLOW       = (255, 255,   0)
ORANGE       = (255, 128,   0)
PURPLE       = (255,   0, 255)
CYAN         = (  0, 255, 255)
BLACK        = (  0,   0,   0)
NEAR_BLACK   = ( 19,  15,  48)
COMBLUE      = (233, 232, 255)
GOLD         = (255, 215,   0)

BGCOLOR = WHITE

# Game states

MENU      = 'menu'
LOADING   = 'loading'
GAMING    = 'gaming'
GAME_OVER = 'game over'

# Character states

STAND = 'stand'
WALK  = 'walk'
JUMP  = 'jump'
FALL  = 'fall'
CLIMB = 'climb'
SKILL = 'skill'

# Character property

MAX_X_VEL    = 3
MAX_Y_VEL    = 11
JUMP_VEL     = -2.1
GRAVITY      = 0.05
JUMP_GRAVITY = 0.02

# Player1 property

P1_DAMAGE = 2

# Game info

CURRENT_TIME = 'current time'
KEYBINDING  = 'keybinding'

# Brick property

BRICK_WIDTH  = 20
BRICK_HEIGHT = 15
BRICK_DUR    = 5

# Bullet property

BULLET_VEL    = 2
BULLET_WIDTH  = 50
BULLET_HEIGHT = 10
BULLET_SIZE = (50,10)

# Sword property

SWORD_DAMAGE    = 2
SWORD_WIDTH     = 25
SWORD_HEIGHT    = 20
SWORD_LAST_TIME = 0.5

# For test
BG_COLOR = GRAY

#Character speeds(higher = slower)
CHARACTER_MOVING_SPEED = 20
CHARACTER_SKILL_SPEED = 15

#Character size
CHARACTER_SIZE=(103//2,133//2)