import pygame
from collections import deque
from math import floor, inf, sqrt
from heapq import heappop, heappush
from queue import PriorityQueue
from random import randrange, choice, shuffle
from time import sleep


# TODO refactoring
# TODO add drawing single node
# TODO add saving previous settings

WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000
GRID_WIDTH, GRID_HEIGHT = 900, 900
GRID_SIZE = 45  # Best change to divisors of 900 if LINES

SQUARE_SIZE = GRID_WIDTH // GRID_SIZE  # Width and height of each node
SIDE_SIZE = (WINDOW_WIDTH - GRID_WIDTH) // 2  # Side tab size
TB_SIZE = (WINDOW_HEIGHT - GRID_HEIGHT) // 2  # Top and bottom tab size
BUTTON_WIDTH, BUTTON_HEIGHT = (SIDE_SIZE - 100) + 5, 70

LINES = False
FONT = None

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


class GraphNode:
    def __init__(self, row, col):
        self.x = SIDE_SIZE + row * SQUARE_SIZE
        self.y = TB_SIZE + col * SQUARE_SIZE
        self.row = row
        self.col = col
        self.color = FREE_COLOR
        self.neighbors = []
        self.visited = False
        self.source_dist = inf  # g score in a*
        self.target_dist = inf  # f score in a*
        self.path = []

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

    def not_barrier(self):
        return self.color != BARRIER_COLOR

    def been_visited(self):
        return self.color == VISITED_COLOR

    def copy(self):
        new = GraphNode(self.row, self.col)
        new.color = self.color

        return new

    def get_neighbors(self, grid):
        self.neighbors = []

        # DOWN
        if self.col + 1 < GRID_SIZE:
            if grid[self.row][self.col+1].not_barrier():
                self.neighbors.append(grid[self.row][self.col+1])

        # RIGHT
        if self.row + 1 < GRID_SIZE:
            if grid[self.row+1][self.col].not_barrier():
                self.neighbors.append(grid[self.row+1][self.col])

        # UP
        if self.col > 0:
            if grid[self.row][self.col-1].not_barrier():
                self.neighbors.append(grid[self.row][self.col-1])

        # LEFT
        if self.row > 0:
            if grid[self.row-1][self.col].not_barrier():
                self.neighbors.append(grid[self.row-1][self.col])

        return self.neighbors

    def __lt__(self, other):
        if self.target_dist is not inf:
            return self.target_dist < other.target_dist

        return self.source_dist < other.source_dist


class Button:
    def __init__(self, text, x, y, offset=0, color=WHITE, algorithm=None):
        self.algorithm = algorithm
        self.text = text
        self.x = x
        self.y = y
        self.offset = offset
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.color = color

    def draw(self):
        pygame.draw.rect(WINDOW, self.color, self.rect)
        font = pygame.font.SysFont(FONT, 60)
        label = font.render(self.text, True, BLACK)
        text_rect = pygame.Rect(
            self.x + 60 + self.offset, self.y + 15, BUTTON_WIDTH, BUTTON_HEIGHT)
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


def main():
    global GRID_SIZE, SQUARE_SIZE

    grid = create_grid()
    start, end = None, None
    pathfinding_done, maze_done = False, False
    selected_algorithm = None
    clock = pygame.time.Clock()

    # Initializing buttons for pathfinding algorithms
    diff = 115
    algo_buttons = [Button("BFS", 50, TB_SIZE, algorithm=BFS),
                    Button("DFS", 50, TB_SIZE + diff, algorithm=DFS),
                    Button("Dijkstra's", 50,
                           TB_SIZE + diff*2, offset=-51, algorithm=dijkstras),
                    Button("A*", 50, TB_SIZE + diff*3, offset=20, algorithm=astar)]

    # Initializing buttons for maze-generating algorithms
    diff = 115
    maze_buttons = [Button("Prim's", 50, TB_SIZE + diff*4,
                           offset=-20, color=(127, 255, 148), algorithm=prims),
                    Button("Division", 50,
                           TB_SIZE + diff*5, offset=-43, color=(127, 255, 148), algorithm=divide),
                    Button("Backtrack", 50, TB_SIZE + diff*6,
                           offset=-60, color=(127, 255, 148), algorithm=backtrack),
                    Button("Random", 50, TB_SIZE +
                           diff*7, offset=-43, color=(127, 255, 148), algorithm=random_maze)]

    # Initializing buttons for grid management and view
    diff = 120
    other_buttons = [Button("LINES", WINDOW_WIDTH -
                            (BUTTON_WIDTH + 50), TB_SIZE + 450, offset=-24, color=FREE_COLOR),
                     Button("RUN", WINDOW_WIDTH -
                            (BUTTON_WIDTH + 50), TB_SIZE + 450 + diff, offset=-2, color=START_COLOR),
                     Button("CLEAR", WINDOW_WIDTH -
                            (BUTTON_WIDTH + 50), TB_SIZE + 450 + diff*2, offset=-31, color=YELLOW),
                     Button("RESET", WINDOW_WIDTH -
                            (BUTTON_WIDTH + 50), TB_SIZE + 450 + diff*3, offset=-24, color=END_COLOR)]

    # Initializing buttons for changing grid size
    diff = 60
    size_buttons = [SmallButton("S", SIDE_SIZE + GRID_WIDTH + 70, TB_SIZE + 375, offset=-1),
                    SmallButton("M", SIDE_SIZE + GRID_WIDTH + 70 + diff,
                                TB_SIZE + 375, offset=-4, color=PATH_COLOR),
                    SmallButton("L", SIDE_SIZE + GRID_WIDTH + 70 + diff*2, TB_SIZE + 375)]

    while True:
        # Updating the window
        draw(grid, algo_buttons + other_buttons + maze_buttons + size_buttons)
        clock.tick(60)

        # For preventing multiple clicks causing redrawing the maze several times
        maze_done = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_grid_pos(pos)

                if row < GRID_SIZE and row >= 0 and col < GRID_SIZE and col >= 0:
                    # Selecting nodes on the grid
                    node = grid[row][col]
                    if start is None:
                        node.set_start()
                        start = node
                    elif end is None and not node.is_start():
                        node.set_end()
                        end = node
                    else:
                        node.set_barrier()
                else:
                    # Selecting a pathfinding algorithm
                    for button in algo_buttons:
                        if button.rect.collidepoint(pos):
                            button.color = PATH_COLOR
                            selected_algorithm = button.algorithm

                            for other in algo_buttons:
                                if other is not button:
                                    other.color = FREE_COLOR
                                    other.draw()

                    # Selecting and generating a maze
                    for button in maze_buttons:
                        if button.rect.collidepoint(pos) and not maze_done:
                            grid, start, end = clear_grid(
                                grid, start, end, save_barriers=False)
                            pathfinding_done = False
                            maze_done = True

                            if button.text == "Random":
                                button.algorithm(grid)

                            elif button.text == "Division":
                                button.algorithm(
                                    grid, 1, GRID_SIZE - 2, 1, GRID_SIZE-2)
                                add_border(grid)

                            elif button.text == "Backtrack":
                                fill_grid(grid)
                                button.algorithm(grid, 1, 1)

                            elif button.text == "Prim's":
                                fill_grid(grid)
                                button.algorithm(grid)

                    # Selecting and changing size of the grid
                    for button in size_buttons:
                        if button.rect.collidepoint(pos):
                            for other in size_buttons:
                                if other is not button:
                                    other.color = FREE_COLOR
                                    other.draw()
                            button.color = PATH_COLOR

                            if button.text == "S":
                                GRID_SIZE = 25
                            elif button.text == "M":
                                GRID_SIZE = 45
                            elif button.text == "L":
                                GRID_SIZE = 75

                            SQUARE_SIZE = GRID_WIDTH // GRID_SIZE

                            grid = create_grid()
                            start, end = None, None
                            pathfinding_done = False
                            draw_grid(grid)

                    for button in other_buttons:
                        if button.rect.collidepoint(pos):
                            if button.text == "RUN":
                                if start and end and not pathfinding_done and selected_algorithm:
                                    # Run the selected algorithm
                                    for row in range(GRID_SIZE):
                                        for col in range(GRID_SIZE):
                                            current = grid[row][col]
                                            current.get_neighbors(grid)

                                    path = selected_algorithm(grid, start, end)

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
                                        draw_path(grid, path)

                            elif button.text == "CLEAR":
                                # Clear the grid (keep the barriers)
                                grid, start, end = clear_grid(grid, start, end)
                                pathfinding_done = False

                            elif button.text == "RESET":
                                # Reset the grid (create a completely new one)
                                grid = create_grid()
                                start, end = None, None
                                pathfinding_done = False

                            elif button.text == "LINES":
                                toggle_lines(button)

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_grid_pos(pos)
                if row < GRID_SIZE and row >= 0 and col < GRID_SIZE and col >= 0:
                    # Unselect a node
                    node = grid[row][col]
                    if node.is_start():
                        start = None
                    elif node.is_end():
                        end = None
                    node.set_free()


# **********************
# *** Draw functions ***
# **********************

# Draw the full window
def draw(grid, buttons=[]):
    WINDOW.fill(BARRIER_COLOR)
    for button in (buttons):
        button.draw()
    draw_legend()
    draw_grid(grid)

    pygame.display.update()


# Draw the path between start and end
def draw_path(grid, path):
    length = len(path)
    for node in path:
        if not node.is_start() and not node.is_end():
            node.color = PATH_COLOR
            if length > 500:
                delay = 10
            elif length > 200:
                delay = 30
            else:
                delay = 50

            pygame.time.delay(delay)
            draw_grid(grid)


# Draw the grid with lines if toggled
def draw_grid(grid):
    # Draw nodes
    for row in grid:
        for node in row:
            pygame.draw.rect(WINDOW, node.color,
                             (node.x, node.y, SQUARE_SIZE, SQUARE_SIZE))

    if LINES:
        # Draw lines
        x, y = SIDE_SIZE, TB_SIZE
        width, height = GRID_WIDTH, GRID_HEIGHT

        for i in range(GRID_SIZE + 1):
            pygame.draw.line(WINDOW, LINE_COLOR, (x, y + i *
                                                  SQUARE_SIZE), (x + width, y + i * SQUARE_SIZE))

            for j in range(GRID_SIZE + 1):
                pygame.draw.line(WINDOW, LINE_COLOR, (x + j *
                                                      SQUARE_SIZE, y), (x + j * SQUARE_SIZE, y + height))

    pygame.display.update()


# Draw the information legend
def draw_legend():
    draw_legend_node("Start node", START_COLOR,  offset=0)
    draw_legend_node("End node", END_COLOR,  offset=50)
    draw_legend_node("Free node", FREE_COLOR,  offset=100)
    draw_legend_node("Barrier node", BARRIER_COLOR, offset=150)
    draw_legend_node("Visited node", VISITED_COLOR,  offset=200)
    draw_legend_node("Path node", PATH_COLOR,  offset=250)
    draw_legend_node("Select a node",  offset=290, action="LMB")
    draw_legend_node("Unselect a node",  offset=320, action="RMB")


# Helper function for draw_legend()
def draw_legend_node(text, color=None, offset=0, action=""):
    x, y = SIDE_SIZE + GRID_WIDTH + 30, TB_SIZE + offset

    font = pygame.font.SysFont(FONT, 30)
    label = font.render(action + " - " + text, True, WHITE)
    text_rect = pygame.Rect(x + 30, y + 5, 100, 50)
    if action != "":
        text_rect = pygame.Rect(x, y + 5, 100, 50)

    if color:
        pygame.draw.rect(WINDOW, color, (x, y, 30, 30))
        pygame.draw.rect(WINDOW, LINE_COLOR, (x, y, 30, 30), 1)

    WINDOW.blit(label, text_rect)


# **********************
# *** Grid functions ***
# **********************

# Get position in the grid (row, col)
def get_grid_pos(pos):
    x, y = pos
    col = (y - TB_SIZE) // SQUARE_SIZE
    row = (x - SIDE_SIZE) // SQUARE_SIZE

    return row, col


# Create a new grid
def create_grid():
    grid = [[GraphNode(row, col) for col in range(GRID_SIZE)]
            for row in range(GRID_SIZE)]

    return grid


# Fill the grid with barriers
def fill_grid(grid):
    for row in grid:
        for node in row:
            node.set_barrier()


# Adds a border for each side of the grid
def add_border(grid, depth=0):
    for i in range(GRID_SIZE):
        grid[depth][i].set_barrier()
        grid[GRID_SIZE-1-depth][i].set_barrier()
        grid[i][depth].set_barrier()
        grid[i][GRID_SIZE-1-depth].set_barrier()

        draw_grid(grid)
        sleep(0.01)


# Toggle the lines dividing the grid (on/off)
def toggle_lines(button):
    global LINES
    if LINES == True:
        LINES = False
        button.color = FREE_COLOR
    else:
        LINES = True
        button.color = BLUE


# Clear the grid (keep start, end and choose to keep barriers)
def clear_grid(grid, start=None, end=None, save_barriers=True):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            node = grid[row][col]
            if (node.is_barrier() and save_barriers) or node.is_start() or node.is_end():
                grid[row][col] = node.copy()
            else:
                grid[row][col] = GraphNode(row, col)
    if start:
        start = grid[start.row][start.col]
        start.set_start()
    if end:
        end = grid[end.row][end.col]
        end.set_end()

    return grid, start, end


# *****************************
# *** Pathfinding algorithms***
# *****************************

# Breadth-first search algorithm (end parameter left for universal alias selected_algorithm())
def BFS(grid, start, end):
    path = [start]
    bfs_queue = deque([[start, path]])

    while bfs_queue:
        current, path = bfs_queue.popleft()

        draw_grid(grid)
        for neighbor in current.neighbors:
            if not neighbor.been_visited():
                if neighbor.is_end():
                    return path + [neighbor]
                else:
                    neighbor.set_visited()
                    bfs_queue.append([neighbor, path + [neighbor]])


# Depth-first search algorithm (end parameter left for universal alias selected_algorithm())
def DFS(grid, current, end, visited=None):
    # List for recreating the path
    if visited == None:
        visited = []

    current.set_visited()
    visited.append(current)

    if current.is_end():
        return visited

    draw_grid(grid)
    for neighbor in current.neighbors:
        if not neighbor.been_visited():
            path = DFS(grid, neighbor, end, visited)
            if path:
                return path


# Dijkstra's algorithm
def dijkstras(grid, start, end):
    start.source_dist = 0
    to_visit = [start]

    while to_visit:
        current = heappop(to_visit)
        current.set_visited()

        draw_grid(grid)
        for neighbor in current.neighbors:
            new_dist = current.source_dist + 1
            new_path = current.path + [current]
            if new_dist < neighbor.source_dist:
                neighbor.source_dist = new_dist
                neighbor.path = new_path
                heappush(to_visit, neighbor)
            if current.is_end():
                return end.path


# A* algorithm
def astar(grid, start, end):
    open_pqueue = PriorityQueue()
    open_pqueue.put(start)
    parents = {}
    start.source_dist = 0
    start.source_dist = h(start.pos(), end.pos())
    open_set = set([start])

    while not open_pqueue.empty():
        current = open_pqueue.get()
        current.set_visited()
        open_set.remove(current)  # closing the node

        if current.is_end():
            path = [end]
            temp = end
            while not temp.is_start():
                temp = parents[temp]
                path.append(temp)

            path.reverse()

            return path

        draw_grid(grid)
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
def random_maze(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            node = grid[row][col]
            if choice([True, False, False]):
                node.set_barrier()
                draw_grid(grid)

    return grid


# Recursive division maze generator
def divide(grid, min_x, max_x, min_y,  max_y):
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
            node = grid[y][x]
            if x == hole and not node.is_start() and not node.is_end():
                node.set_free()
            else:
                node.set_barrier()

            draw_grid(grid)

        # Recursive calls
        divide(grid, min_x, max_x, min_y, y-1)
        divide(grid, min_x, max_x, y+1, max_y)
    else:
        if height < 2:
            return

        # Randomly generate a wall
        x = floor(randrange(min_x, max_x) / 2) * 2

        # Randomly generate a hole
        hole = floor(randrange(min_y, max_y) / 2) * 2 + 1

        # Draw the wall with the hole
        for y in range(min_y, max_y+1):
            node = grid[y][x]
            if y == hole and not node.is_start() and not node.is_end():
                node.set_free()
            else:
                node.set_barrier()
            draw_grid(grid)

        # Recursive calls
        divide(grid, min_x, x-1, min_y, max_y)
        divide(grid, x+1, max_x, min_y, max_y)


# Recurisve backtracker maze generator
def backtrack(grid, row, col):
    node = grid[row][col]
    if node.is_barrier():
        node.set_free()

    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    shuffle(directions)

    while len(directions) > 0:
        # Pick a random neighboring node of "node"
        direction = directions.pop()
        r, c = row + direction[0] * 2, col + direction[1] * 2
        if in_grid(r, c, offset=1):
            current = grid[r][c]

            if not current.is_free():
                r, c = row + direction[0], col + direction[1]
                if in_grid(r, c, offset=1):
                    # Turn the node between previous "current" and current "current" into a passage
                    link = grid[r][c]
                    if link.is_barrier():
                        link.set_free()
                        draw_grid(grid)

                # Recursive call
                backtrack(grid, current.row, current.col)


# Prim's maze generator
def prims(grid):
    # Randomly select a starting node
    x, y = randrange(GRID_SIZE), randrange(GRID_SIZE)

    # [0] = row of middle node between current frontier and previous frontier
    # [1] = col of middle node between current frontier and previous frontier
    # [2] = row of current frontier
    # [3] = col of current frontier
    frontiers = [[x, y, x, y]]

    while len(frontiers) > 0:
        frontier = choice(frontiers)
        frontiers.remove(frontier)
        x, y = frontier[2], frontier[3]

        if grid[x][y].is_barrier():
            # Create a passage
            if grid[frontier[0]][frontier[1]].is_barrier():
                grid[frontier[0]][frontier[1]].set_free()

            if grid[x][y].is_barrier():
                grid[x][y].set_free()

            draw_grid(grid)

            # If in grid, add fontiers of the current frontier (with nodes in between them) to the list of frontiers
            if (x >= 2 and grid[x-2][y].is_barrier()):
                frontiers.append([x-1, y, x-2, y])
            if (y >= 2 and grid[x][y-2].is_barrier()):
                frontiers.append([x, y-1, x, y-2])
            if (x < GRID_SIZE-2 and grid[x+2][y].is_barrier()):
                frontiers.append([x+1, y, x+2, y])
            if (y < GRID_SIZE-2 and grid[x][y+2].is_barrier()):
                frontiers.append([x, y+1, x, y+2])


# Helper function for backtrack()
def in_grid(row, col, offset=0):
    return row in range(offset, GRID_SIZE-offset) and col in range(offset, GRID_SIZE-offset)


# Helper function for divide()
def choose_orientation(width, height):
    # True for horizontal, False for vertical
    if width < height:
        return True
    elif width > height:
        return False
    else:
        return choice([True, False])


if __name__ == "__main__":
    main()
