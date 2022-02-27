import pygame
from collections import deque
from math import floor, inf, sqrt
from heapq import heappop, heappush
from queue import PriorityQueue
from random import randrange, choice, shuffle


WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000
GRAPH_WIDTH, GRAPH_HEIGHT = 900, 900
GRAPH_SIZE = 45  # Best change to divisors of GRAPH_WIDTH and GRAPH_HEIGHT

NODE_SIZE = GRAPH_WIDTH // GRAPH_SIZE  # Width and height of each node
SIDE_SIZE = (WINDOW_WIDTH - GRAPH_WIDTH) // 2  # Side tab size
TB_SIZE = (WINDOW_HEIGHT - GRAPH_HEIGHT) // 2  # Top and bottom tab size
BUTTON_WIDTH, BUTTON_HEIGHT = (SIDE_SIZE - 100) + 5, 70


GRID = False
ANIMATION_SPEED = "F"
FONT = None

# Base delays based on ANIMATION_SPEED and GRAPH_SIZE
DELAYS = {
    "S": {25: 30, 45: 15, 75: 8},
    "N": {25: 20, 45: 10, 75: 5},
    "F": {25: 10, 45: 5, 75: 3}
}

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

BARRIER_COLOR = BLACK
FREE_COLOR = WHITE
START_COLOR = GREEN
END_COLOR = RED
PATH_COLOR = (186, 85, 211)
VISITED_COLOR = BLUE
LINE_COLOR = GRAY

pygame.init()
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pathfinding Algorithms Visualizer")


# *************************
# *** General functions ***
# *************************

def main():
    global GRAPH_SIZE, NODE_SIZE, GRID, ANIMATION_SPEED

    graph = create_graph()
    start, end = None, None
    pathfinding_done = False
    selected_algorithm = None
    clock = pygame.time.Clock()

    # Initialize buttons for pathfinding algorithms
    diff = 115
    algo_buttons = [Button("BFS", 50, TB_SIZE + 10, algorithm=BFS),
                    Button("DFS", 50, TB_SIZE + 10 + diff, algorithm=DFS),
                    Button("Dijkstra's", 50,
                           TB_SIZE + 10 + diff*2, text_offset=-51, algorithm=dijkstras),
                    Button("A*", 50, TB_SIZE + 10 + diff*3, text_offset=20, algorithm=astar)]

    # Initialize buttons for maze-generating algorithms
    diff = 115
    maze_buttons = [Button("Prim's", 50, TB_SIZE + 10 + diff*4,
                           text_offset=-20, color=(127, 255, 148), algorithm=prims),
                    Button("Division", 50,
                           TB_SIZE + 10 + diff*5, text_offset=-43, color=(127, 255, 148), algorithm=divide),
                    Button("Backtrack", 50, TB_SIZE + 10 + diff*6,
                           text_offset=-60, color=(127, 255, 148), algorithm=backtrack),
                    Button("Random", 50, TB_SIZE + 10 +
                           diff*7, text_offset=-43, color=(127, 255, 148), algorithm=random_maze)]

    # Initialize buttons for graph management and view
    diff = 115
    other_buttons = [Button("GRID OFF", WINDOW_WIDTH -
                            (BUTTON_WIDTH + 50), TB_SIZE + 360, text_offset=-59, height_offset=20, color=FREE_COLOR),
                     Button("GRID ON", WINDOW_WIDTH -
                            (BUTTON_WIDTH + 50), TB_SIZE + 360, text_offset=-49, height_offset=20, color=BLUE),
                     Button("RUN", WINDOW_WIDTH -
                            (BUTTON_WIDTH + 50), TB_SIZE + 10 + diff*5, text_offset=-2, color=START_COLOR),
                     Button("CLEAR", WINDOW_WIDTH -
                            (BUTTON_WIDTH + 50), TB_SIZE + 10 + diff*6, text_offset=-31, color=YELLOW),
                     Button("RESET", WINDOW_WIDTH -
                            (BUTTON_WIDTH + 50), TB_SIZE + 10 + diff*7, text_offset=-24, color=END_COLOR)]

    if GRID:
        other_buttons[0].visible = False
        other_buttons[1].visible = True
    else:
        other_buttons[0].visible = True
        other_buttons[1].visible = False

    # Initialize buttons for changing graph size
    diff = 60
    size_buttons = [SmallButton("S", SIDE_SIZE + GRAPH_WIDTH + 70, TB_SIZE + 445, offset=-1),
                    SmallButton("M", SIDE_SIZE + GRAPH_WIDTH + 70 + diff,
                                TB_SIZE + 445, offset=-4),
                    SmallButton("L", SIDE_SIZE + GRAPH_WIDTH + 70 + diff*2, TB_SIZE + 445)]

    if GRAPH_SIZE == 25:
        size_buttons[0].color = PATH_COLOR
    elif GRAPH_SIZE == 45:
        size_buttons[1].color = PATH_COLOR
    elif GRAPH_SIZE == 75:
        size_buttons[2].color = PATH_COLOR

    # Initialize buttons for changing animation speed
    animation_buttons = [SmallButton("S", SIDE_SIZE + GRAPH_WIDTH + 70, TB_SIZE + 523, offset=-1, ),
                         SmallButton("N", SIDE_SIZE + GRAPH_WIDTH + 70 + diff,
                                     TB_SIZE + 523, offset=-2),
                         SmallButton("F", SIDE_SIZE + GRAPH_WIDTH + 70 + diff*2, TB_SIZE + 523)]

    if ANIMATION_SPEED == "S":
        animation_buttons[0].color = PATH_COLOR
    elif ANIMATION_SPEED == "N":
        animation_buttons[1].color = PATH_COLOR
    elif ANIMATION_SPEED == "F":
        animation_buttons[2].color = PATH_COLOR

    # Main program loop
    while True:
        # Update the window
        draw(graph, algo_buttons + other_buttons +
             maze_buttons + size_buttons + animation_buttons)
        clock.tick(60)

        # For preventing multiple clicks
        wait = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_graph_pos(pos)

                if row < GRAPH_SIZE and row >= 0 and col < GRAPH_SIZE and col >= 0:
                    # Select nodes on the graph
                    node = graph[row][col]
                    if start is None:
                        node.set_start()
                        node.draw(update=True)
                        start = node
                    elif end is None and not node.is_start():
                        node.set_end()
                        node.draw(update=True)
                        end = node
                    else:
                        node.set_barrier()
                        node.draw(update=True)
                else:
                    # Select a pathfinding algorithm
                    for button in algo_buttons:
                        if button.rect.collidepoint(pos):
                            button.color = PATH_COLOR
                            selected_algorithm = button.algorithm

                            for other in algo_buttons:
                                if other is not button:
                                    other.color = FREE_COLOR
                                    other.draw()

                    # Select and generate a maze
                    for button in maze_buttons:
                        if button.rect.collidepoint(pos) and not wait:
                            clear_graph(graph, save_barriers=False)
                            pathfinding_done = False
                            wait = True

                            if button.text == "Random":
                                draw_graph(graph)
                                button.algorithm(graph)

                            elif button.text == "Division":
                                draw_graph(graph)
                                button.algorithm(
                                    graph, 1, GRAPH_SIZE - 2, 1, GRAPH_SIZE-2)
                                add_border(graph)

                            elif button.text == "Backtrack":
                                fill_graph(graph)
                                draw_graph(graph)
                                button.algorithm(graph, 1, 1)

                            elif button.text == "Prim's":
                                fill_graph(graph)
                                draw_graph(graph)
                                button.algorithm(graph)

                    # Select and change size of the graph
                    for button in size_buttons:
                        if button.rect.collidepoint(pos):
                            for other in size_buttons:
                                if other is not button:
                                    other.color = FREE_COLOR
                                    other.draw()
                            button.color = PATH_COLOR

                            if button.text == "S":
                                GRAPH_SIZE = 25
                            elif button.text == "M":
                                GRAPH_SIZE = 45
                            elif button.text == "L":
                                GRAPH_SIZE = 75

                            NODE_SIZE = GRAPH_WIDTH // GRAPH_SIZE

                            graph = create_graph()
                            start, end = None, None
                            pathfinding_done = False
                            draw_graph(graph)

                    for button in animation_buttons:
                        if button.rect.collidepoint(pos):
                            for other in animation_buttons:
                                if other is not button:
                                    other.color = FREE_COLOR
                                    other.draw()

                            button.color = PATH_COLOR

                            ANIMATION_SPEED = button.text

                    for button in other_buttons:
                        if button.rect.collidepoint(pos):
                            if button.text == "RUN":
                                if start and end and not pathfinding_done and selected_algorithm:
                                    # Run the selected algorithm
                                    for row in range(GRAPH_SIZE):
                                        for col in range(GRAPH_SIZE):
                                            current = graph[row][col]
                                            current.get_neighbors(graph)

                                    path = selected_algorithm(start, end)

                                    pathfinding_done = True
                                    if not path:
                                        # Inform that no path has been found
                                        font = pygame.font.SysFont(FONT, 120)
                                        label = font.render(
                                            "PATH NOT FOUND!", True, RED)
                                        text_rect = label.get_rect(
                                            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                                        WINDOW.blit(label, text_rect)
                                        pygame.display.update()
                                        pygame.time.delay(500)
                                        pathfinding_done = False
                                        print("PATH NOT FOUND")
                                    else:
                                        draw_path(path)

                            elif button.text == "CLEAR":
                                # Clear the graph (keep the barriers)
                                clear_graph(graph)
                                pathfinding_done = False

                            elif button.text == "RESET":
                                # Reset the graph (create a completely new one)
                                graph = create_graph()
                                start, end = None, None
                                pathfinding_done = False

                            elif button in [other_buttons[0], other_buttons[1]] and button.visible and not wait:
                                # Toggle the grid
                                other_buttons[0].visible = not other_buttons[0].visible
                                other_buttons[1].visible = not other_buttons[1].visible
                                wait = True

                                GRID = not GRID

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_graph_pos(pos)
                if row < GRAPH_SIZE and row >= 0 and col < GRAPH_SIZE and col >= 0:
                    # Unselect a node
                    node = graph[row][col]
                    if node.is_start():
                        start = None
                    elif node.is_end():
                        end = None
                    node.set_free()
                    node.draw(update=True)


# Helper function for handling events within algorithms
def run_checks():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise Exception(
                "Exiting the program while executing an algorithm! (current settings will not be saved)")


# **************************
# *** Settings functions ***
# **************************

def save_settings():
    with open("settings.txt", "w") as file:
        file.write(f"{int(GRID)} ")
        file.write(f"{GRAPH_SIZE} ")
        file.write(f"{ANIMATION_SPEED}")


def load_settings():
    global GRID, GRAPH_SIZE, ANIMATION_SPEED, NODE_SIZE
    try:
        with open("settings.txt", "r") as file:
            GRID, GRAPH_SIZE, ANIMATION_SPEED = file.readline().split(" ")
            GRID = bool(int(GRID))
            GRAPH_SIZE = int(GRAPH_SIZE)
            ANIMATION_SPEED = ANIMATION_SPEED
            NODE_SIZE = GRAPH_WIDTH // GRAPH_SIZE
    except FileNotFoundError:
        GRID = False
        GRAPH_SIZE = 45
        ANIMATION_SPEED = "F"
        NODE_SIZE = GRAPH_WIDTH // GRAPH_SIZE


# **********************
# *** Draw functions ***
# **********************

# Draw the full window
def draw(graph, buttons=[]):
    WINDOW.fill(BARRIER_COLOR)
    for button in (buttons):
        button.draw()
    draw_legend()
    draw_graph(graph)

    pygame.display.update()


# Draw the path between start and end
def draw_path(path):
    length = len(path)
    prev = path[0]
    for node in path[1:]:
        run_checks()
        if not prev.is_start():
            prev.color = PATH_COLOR
            prev.draw(update=True)
        if not node.is_start() and not node.is_end():
            node.color = YELLOW
            node.draw(update=True)
            prev = node
        # Delay based on length relative to GRAPH_SIZE and base delay
        pygame.time.delay(round(4 * GRAPH_SIZE / length * 6 *
                          DELAYS[ANIMATION_SPEED][GRAPH_SIZE]))


# Draw the graph and grid if toggled
def draw_graph(graph):
    for row in graph:
        for node in row:
            node.draw()

    pygame.display.update()


# Draw the information legend
def draw_legend():
    draw_legend_node("Start node", START_COLOR,  height_offset=0)
    draw_legend_node("End node", END_COLOR,  height_offset=50)
    draw_legend_node("Free node", FREE_COLOR,  height_offset=100)
    draw_legend_node("Barrier node", BARRIER_COLOR, height_offset=150)
    draw_legend_node("Visited node", VISITED_COLOR,  height_offset=200)
    draw_legend_node("Path node", PATH_COLOR,  height_offset=250)
    draw_legend_node("Select a node",  height_offset=290, action="LMB")
    draw_legend_node("Unselect a node",  height_offset=320, action="RMB")
    draw_legend_node("Graph size", height_offset=410, text_offset=33)
    draw_legend_node("Animation speed", height_offset=488)


# Helper function for draw_legend()
def draw_legend_node(text, color=None, height_offset=0, text_offset=0, action=""):

    height_offset += 3
    x, y = SIDE_SIZE + GRAPH_WIDTH + 30, TB_SIZE + height_offset

    font = pygame.font.SysFont(FONT, 32)
    if action != "" or color is not None:
        label = font.render(action + " - " + text, True, WHITE)
    else:
        label = font.render(text, True, WHITE)
    text_rect = pygame.Rect(x + 30 + text_offset, y + 5, 100, 50)
    if action != "":
        text_rect = pygame.Rect(x + text_offset, y + 5, 100, 50)

    if color:
        pygame.draw.rect(WINDOW, color, (x, y, 30, 30))
        pygame.draw.rect(WINDOW, LINE_COLOR, (x, y, 30, 30), 1)

    WINDOW.blit(label, text_rect)


# ***********************
# *** Graph functions ***
# ***********************

# Get position in the graph (row, col)
def get_graph_pos(pos):
    x, y = pos
    col = (y - TB_SIZE) // NODE_SIZE
    row = (x - SIDE_SIZE) // NODE_SIZE

    return row, col


# Create a new graph
def create_graph():
    graph = [[GraphNode(row, col) for col in range(GRAPH_SIZE)]
             for row in range(GRAPH_SIZE)]

    return graph


# Fill the graph with barriers
def fill_graph(graph):
    for row in graph:
        for node in row:
            node.set_barrier()


# Adds a border for each side of the graph
def add_border(graph, depth=0):
    for i in range(GRAPH_SIZE):
        graph[depth][i].set_barrier()
        graph[depth][i].draw(update=True)

        graph[GRAPH_SIZE-1-depth][i].set_barrier()
        graph[GRAPH_SIZE-1-depth][i].draw(update=True)

        graph[i][depth].set_barrier()
        graph[i][depth].draw(update=True)

        graph[i][GRAPH_SIZE-1-depth].set_barrier()
        graph[i][GRAPH_SIZE-1-depth].draw(update=True)

        pygame.time.delay(2 * DELAYS[ANIMATION_SPEED][GRAPH_SIZE])


# Clear the graph (keep start and end, also choose whether to keep barriers)
def clear_graph(graph, save_barriers=True):
    for row in range(GRAPH_SIZE):
        for col in range(GRAPH_SIZE):
            node = graph[row][col]
            if (node.is_barrier() and save_barriers) or node.is_start() or node.is_end():
                graph[row][col].reset(keep_color=True)
            else:
                graph[row][col].reset(keep_color=False)


# *****************************
# *** Pathfinding algorithms***
# *****************************


# Breadth-first search algorithm (end parameter left for universal alias selected_algorithm())
def BFS(start, end):
    path = [start]
    bfs_queue = deque([[start, path]])

    while bfs_queue:
        run_checks()

        current, path = bfs_queue.popleft()
        for neighbor in current.neighbors:
            if not neighbor.been_visited():
                if neighbor.is_end():
                    return path + [neighbor]
                else:
                    neighbor.set_visited()
                    neighbor.draw(update=True)
                    pygame.time.delay(DELAYS[ANIMATION_SPEED][GRAPH_SIZE])
                    bfs_queue.append([neighbor, path + [neighbor]])


# Depth-first search algorithm (end parameter left for universal alias selected_algorithm())
def DFS(current, end):
    call_stack = [current]

    # List for recreating the path
    visited = []

    while len(call_stack) > 0:
        current = call_stack.pop()
        run_checks()

        current.set_visited()
        current.draw(update=True)
        pygame.time.delay(DELAYS[ANIMATION_SPEED][GRAPH_SIZE])
        visited.append(current)

        if current.is_end():
            return visited

        for neighbor in current.neighbors:
            if not neighbor.been_visited():
                call_stack.append(neighbor)


# Dijkstra's algorithm
def dijkstras(start, end):
    start.source_dist = 0
    to_visit = [start]

    while to_visit:
        run_checks()

        current = heappop(to_visit)
        current.set_visited()
        current.draw(update=True)
        pygame.time.delay(DELAYS[ANIMATION_SPEED][GRAPH_SIZE])

        for neighbor in current.neighbors:
            new_dist = current.source_dist + 1
            new_path = current.path + [current]
            if new_dist < neighbor.source_dist:
                neighbor.source_dist = new_dist
                neighbor.path = new_path
                heappush(to_visit, neighbor)
            if current.is_end():
                return end.path + [end]


# A* algorithm
def astar(start, end):
    open_pqueue = PriorityQueue()
    open_pqueue.put(start)
    parents = {}
    start.source_dist = 0
    start.source_dist = h(start.pos(), end.pos())
    open_set = set([start])

    while not open_pqueue.empty():
        run_checks()

        current = open_pqueue.get()
        current.set_visited()
        current.draw(update=True)
        pygame.time.delay(DELAYS[ANIMATION_SPEED][GRAPH_SIZE])
        open_set.remove(current)

        # Generate and return the path when end reached
        if current.is_end():
            path = [end]
            temp = end
            while not temp.is_start():
                temp = parents[temp]
                path.append(temp)

            path.reverse()

            return path

        for neighbor in current.neighbors:
            new_g_score = current.source_dist + 1
            if new_g_score < neighbor.source_dist:
                parents[neighbor] = current
                neighbor.source_dist = new_g_score
                neighbor.target_dist = new_g_score + \
                    h(neighbor.pos(), end.pos())
                if neighbor not in open_set:
                    open_pqueue.put(neighbor)
                    open_set.add(neighbor)
                    neighbor.set_visited()
                    neighbor.draw(update=True)
                    pygame.time.delay(DELAYS[ANIMATION_SPEED][GRAPH_SIZE])


# Heuristic function for A* (Manhattan distance)
def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    h = abs(x1 - x2) + abs(y1 - y2)

    return h


# Heuristic function for A* (Euclidean distance)
def h_euclidean(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    h = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return h


# *********************************
# *** Maze-generating algorithms***
# *********************************

# Random maze generator (1/3 chance for barrier)
def random_maze(graph):
    for row in range(GRAPH_SIZE):
        for col in range(GRAPH_SIZE):
            run_checks()

            node = graph[row][col]
            if choice([True, False, False]):
                node.set_barrier()
                node.draw(update=True)
                pygame.time.delay(DELAYS[ANIMATION_SPEED][GRAPH_SIZE] // 2)

    return graph


# Recursive division maze generator
def divide(graph, min_x, max_x, min_y,  max_y):
    run_checks()

    width, height = max_x - min_x, max_y - min_y
    horizontal = choose_orientation(width, height)

    if horizontal:
        if width < 2:
            return

        # Randomly generate a wall
        y = floor(randrange(min_y, max_y) / 2) * 2

        # Randomly generate a hole
        hole = floor(randrange(min_x, max_x) / 2) * 2 + 1

        # Draw the wall with the hole
        for x in range(min_x, max_x+1):
            node = graph[y][x]
            if x == hole and not node.is_start() and not node.is_end():
                node.set_free()
            else:
                node.set_barrier()

            node.draw(update=True)
            pygame.time.delay(DELAYS[ANIMATION_SPEED][GRAPH_SIZE])

        # Recursive calls
        divide(graph, min_x, max_x, min_y, y-1)
        divide(graph, min_x, max_x, y+1, max_y)
    else:
        if height < 2:
            return

        # Randomly generate a wall
        x = floor(randrange(min_x, max_x) / 2) * 2

        # Randomly generate a hole
        hole = floor(randrange(min_y, max_y) / 2) * 2 + 1

        # Draw the wall with the hole
        for y in range(min_y, max_y+1):
            node = graph[y][x]
            if y == hole and not node.is_start() and not node.is_end():
                node.set_free()
            else:
                node.set_barrier()

            node.draw(update=True)
            pygame.time.delay(DELAYS[ANIMATION_SPEED][GRAPH_SIZE])

        # Recursive calls
        divide(graph, min_x, x-1, min_y, max_y)
        divide(graph, x+1, max_x, min_y, max_y)


# Recurisve backtracker maze generator
def backtrack(graph, row, col):
    node = graph[row][col]
    if node.is_barrier():
        node.set_free()
        node.draw(update=True)
        pygame.time.delay(DELAYS[ANIMATION_SPEED][GRAPH_SIZE])

    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    shuffle(directions)

    while len(directions) > 0:
        run_checks()

        # Pick a random neighboring node of "node"
        direction = directions.pop()
        r, c = row + direction[0] * 2, col + direction[1] * 2
        if in_graph(r, c, offset=1):
            current = graph[r][c]

            if not current.is_free():
                r, c = row + direction[0], col + direction[1]
                if in_graph(r, c, offset=1):
                    # Turn the node between previous "current" and current "current" into a passage
                    link = graph[r][c]
                    if link.is_barrier():
                        link.set_free()
                        link.draw(update=True)
                        pygame.time.delay(
                            DELAYS[ANIMATION_SPEED][GRAPH_SIZE])

                # Recursive call
                backtrack(graph, current.row, current.col)


# Prim's maze generator
def prims(graph):
    # Randomly select a starting node
    x, y = randrange(GRAPH_SIZE), randrange(GRAPH_SIZE)

    # [0] = row of middle node between current frontier and previous frontier
    # [1] = col of middle node between current frontier and previous frontier
    # [2] = row of current frontier
    # [3] = col of current frontier
    frontiers = [[x, y, x, y]]

    while len(frontiers) > 0:
        run_checks()

        frontier = choice(frontiers)
        frontiers.remove(frontier)
        x, y = frontier[2], frontier[3]
        current = graph[x][y]

        if current.is_barrier():
            mid = graph[frontier[0]][frontier[1]]
            # Create a passage
            current.set_free()
            current.draw(update=True)
            if mid.is_barrier():
                mid.set_free()
                mid.draw(update=True)
            pygame.time.delay(DELAYS[ANIMATION_SPEED][GRAPH_SIZE])

            # If in the graph, add fontiers of the current frontier (with nodes in between them) to the list of frontiers
            if (x >= 2 and graph[x-2][y].is_barrier()):
                frontiers.append([x-1, y, x-2, y])
            if (y >= 2 and graph[x][y-2].is_barrier()):
                frontiers.append([x, y-1, x, y-2])
            if (x < GRAPH_SIZE-2 and graph[x+2][y].is_barrier()):
                frontiers.append([x+1, y, x+2, y])
            if (y < GRAPH_SIZE-2 and graph[x][y+2].is_barrier()):
                frontiers.append([x, y+1, x, y+2])


# Helper function for backtrack()
def in_graph(row, col, offset=0):
    return row in range(offset, GRAPH_SIZE-offset) and col in range(offset, GRAPH_SIZE-offset)


# Helper function for divide()
def choose_orientation(width, height):
    # True for horizontal, False for vertical
    if width < height:
        return True
    elif width > height:
        return False
    else:
        return choice([True, False])


# *********************
# *** Graph Classes ***
# *********************
class GraphNode:
    def __init__(self, row, col):
        self.x = SIDE_SIZE + row * NODE_SIZE
        self.y = TB_SIZE + col * NODE_SIZE
        self.row = row
        self.col = col
        self.color = FREE_COLOR
        self.neighbors = []
        self.visited = False
        self.source_dist = inf  # g score in a*
        self.target_dist = inf  # f score in a*
        self.path = []

    def draw(self, update=False):
        pygame.draw.rect(WINDOW, self.color,
                         (self.x, self.y, NODE_SIZE, NODE_SIZE))

        if GRID:
            pygame.draw.line(WINDOW, LINE_COLOR, (self.x, self.y),
                             (self.x + NODE_SIZE, self.y))

            pygame.draw.line(WINDOW, LINE_COLOR, (self.x, self.y),
                             (self.x, self.y + NODE_SIZE))

            pygame.draw.line(WINDOW, LINE_COLOR, (self.x + NODE_SIZE, self.y),
                             (self.x + NODE_SIZE, self.y + NODE_SIZE))

            pygame.draw.line(WINDOW, LINE_COLOR, (self.x, self.y + NODE_SIZE),
                             (self.x + NODE_SIZE, self.y + NODE_SIZE))

        if update:
            pygame.display.update()

    def pos(self):
        return self.row, self.col

    def set_start(self):
        self.color = START_COLOR

    def set_free(self):
        self.color = FREE_COLOR

    def set_end(self):
        self.color = END_COLOR

    def set_barrier(self):
        if self.is_free():
            self.color = BARRIER_COLOR

    def set_visited(self):
        self.visited = True
        if not self.is_start() and not self.is_end():
            self.color = VISITED_COLOR

    def is_start(self):
        return self.color == START_COLOR

    def is_end(self):
        return self.color == END_COLOR

    def is_free(self):
        return self.color == FREE_COLOR

    def is_barrier(self):
        return self.color == BARRIER_COLOR

    def been_visited(self):
        return self.color == VISITED_COLOR

    def reset(self, keep_color=True):
        if not keep_color:
            self.color = FREE_COLOR
        self.neighbors = []
        self.visited = False
        self.source_dist = inf  # g score in a*
        self.target_dist = inf  # f score in a*
        self.path = []

    def get_neighbors(self, graph):
        self.neighbors = []

        # DOWN
        if self.col + 1 < GRAPH_SIZE:
            if not graph[self.row][self.col+1].is_barrier():
                self.neighbors.append(graph[self.row][self.col+1])

        # RIGHT
        if self.row + 1 < GRAPH_SIZE:
            if not graph[self.row+1][self.col].is_barrier():
                self.neighbors.append(graph[self.row+1][self.col])

        # UP
        if self.col > 0:
            if not graph[self.row][self.col-1].is_barrier():
                self.neighbors.append(graph[self.row][self.col-1])

        # LEFT
        if self.row > 0:
            if not graph[self.row-1][self.col].is_barrier():
                self.neighbors.append(graph[self.row-1][self.col])

        return self.neighbors

    def __lt__(self, other):
        if self.target_dist is not inf:
            return self.target_dist < other.target_dist

        return self.source_dist < other.source_dist


# **********************
# *** Button Classes ***
# **********************

class Button:
    def __init__(self, text, x, y, color=WHITE, text_offset=0, height_offset=0, algorithm=None, visible=True):
        self.algorithm = algorithm
        self.text = text
        self.x = x
        self.y = y
        self.text_offset = text_offset
        self.height_offset = height_offset
        self.rect = pygame.Rect(
            x, y, BUTTON_WIDTH, BUTTON_HEIGHT-height_offset)
        self.color = color
        self.visible = visible

    def draw(self):
        if not self.visible:
            return

        pygame.draw.rect(WINDOW, self.color, self.rect)
        font = pygame.font.SysFont(FONT, 60)
        label = font.render(self.text, True, BLACK)
        text_rect = pygame.Rect(
            self.x + 60 + self.text_offset, self.y + 16 - self.height_offset // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        WINDOW.blit(label, text_rect)


class SmallButton:
    def __init__(self, text, x, y, offset=0, color=WHITE):
        self.text = text
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.offset = offset

    def draw(self):
        pygame.draw.rect(WINDOW, self.color, self.rect)
        font = pygame.font.SysFont(FONT, 45)
        label = font.render(self.text, True, BLACK)
        text_rect = pygame.Rect(
            self.x + 11 + self.offset, self.y + 7, 40, 40)
        WINDOW.blit(label, text_rect)


if __name__ == "__main__":
    load_settings()
    main()
    save_settings()
