FONT = None

# Base delays based on animation_speed and graph_size
DELAYS = {
    "S": {25: 30, 45: 15, 75: 8},
    "N": {25: 20, 45: 10, 75: 5},
    "F": {25: 10, 45: 5, 75: 3}
}

MAZE_DELAY_MULTIPLIER = 2

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
