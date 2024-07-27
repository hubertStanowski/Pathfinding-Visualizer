SMALL, MEDIUM, LARGE = 25, 45, 75

# TODO make grid_size dynamic to best fit change delays dict to only assign multipliers to s n f
# Base delays based on animation_speed and graph_size
DELAYS = {
    "S": {SMALL: 30, MEDIUM: 20, LARGE: 10},
    "N": {SMALL: 20, MEDIUM: 10, LARGE: 5},
    "F": {SMALL: 10, MEDIUM: 5, LARGE: 3}
}


MAZE_DELAY_MULTIPLIER = 2

FONT = None

DEFAULT_BUTTON_COOLDOWN = 200

DIRECTIONS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0)
]

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (127, 255, 148)
MAGENTA = (186, 85, 211)


BARRIER_COLOR = BLACK
FREE_COLOR = WHITE
START_COLOR = GREEN
END_COLOR = RED
PATH_COLOR = MAGENTA
VISITED_COLOR = BLUE
LINE_COLOR = GRAY
MAZE_BUTTON_COLOR = LIGHT_GREEN
BUTTON_FONT_COLOR = BLACK
LEGEND_FONT_COLOR = WHITE
