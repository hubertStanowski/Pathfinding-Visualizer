FONT = None

# Base delays based on animation_speed and graph_size
DELAYS = {
    "S": {25: 30, 45: 15, 75: 8},
    "N": {25: 20, 45: 10, 75: 5},
    "F": {25: 10, 45: 5, 75: 3}
}


# possible neighbor directions
DIRECTIONS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0)
]


# label colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (127, 255, 148)


# assign colors to node types
BARRIER_COLOR = BLACK
FREE_COLOR = WHITE
START_COLOR = GREEN
END_COLOR = RED
PATH_COLOR = (186, 85, 211)
VISITED_COLOR = BLUE
LINE_COLOR = GRAY
