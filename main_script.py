import pygame
from collections import deque
from math import floor, inf, sqrt
from heapq import heappop, heappush
from queue import PriorityQueue
from datetime import datetime
from random import randrange, choice
import sys
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000
GRID_WIDTH, GRID_HEIGHT = 900, 900


GRID_SIZE = 45
SQUARE_SIZE = GRID_WIDTH // GRID_SIZE
SIDE_SIZE = (WINDOW_WIDTH - GRID_WIDTH) // 2
TB_SIZE = (WINDOW_HEIGHT - GRID_HEIGHT) // 2  # Top and bottom tab size
BUTTON_WIDTH, BUTTON_HEIGHT = (SIDE_SIZE - 100), 70

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


FONT = None


BARRIER_COLOR = BLACK
FREE_COLOR = WHITE
PATH_COLOR = (186, 85, 211)
VISITED_COLOR = BLUE
START_COLOR = GREEN
END_COLOR = RED
LINE_COLOR = GRAY

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

    def select_start(self):
        self.color = START_COLOR

    def unselect(self):
        self.color = FREE_COLOR

    def select_end(self):
        self.color = END_COLOR

    def select_barrier(self):
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

    def reset_neighbors(self, grid):
        self.neighbors = []

        # DOWN
        if self.col + 1 < GRID_SIZE and grid[self.row][self.col+1].not_barrier():
            self.neighbors.append(grid[self.row][self.col+1])

        # RIGHT
        if self.row + 1 < GRID_SIZE and grid[self.row+1][self.col].not_barrier():
            self.neighbors.append(grid[self.row+1][self.col])

        # UP
        if self.col > 0 and grid[self.row][self.col-1].not_barrier():
            self.neighbors.append(grid[self.row][self.col-1])
        # LEFT
        if self.row > 0 and grid[self.row-1][self.col].not_barrier():
            self.neighbors.append(grid[self.row-1][self.col])

    def __lt__(self, other):
        if self.target_dist is not inf:
            return self.target_dist < other.target_dist

        return self.source_dist < other.source_dist


class Button:
    def __init__(self, algorithm, text, x, y, offset=0, color=WHITE):
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
    finished = False
    selected_algorithm = None
    algo_buttons = [Button(BFS, "BFS", 50, 50),
                    Button(DFS, "DFS", 50, 170),
                    Button(dijkstras, "Dijkstra's", 50, 290, offset=-54),
                    Button(astar, "A*", 50, 410, offset=20)]

    maze_buttons = [Button(random_maze, "Random", WINDOW_WIDTH - (BUTTON_WIDTH + 50), 570, offset=-45, color=(127, 255, 148)),
                    Button(divide, "Division", WINDOW_WIDTH - (BUTTON_WIDTH + 50), 690, offset=-45, color=(127, 255, 148))]

    other_buttons = [Button(None, "RUN", 50, 570, offset=-5, color=GREEN),
                     Button(None, "CLEAR", 50, 690, offset=-35, color=YELLOW),
                     Button(None, "RESET", 50, 810, offset=-25, color=RED),
                     Button(None, "SAVE", WINDOW_WIDTH -
                            (BUTTON_WIDTH + 50), 810, offset=-15, color=BLUE)]

    size_buttons = [SmallButton("S", SIDE_SIZE + GRID_WIDTH + 70, TB_SIZE + 400, offset=-1),
                    SmallButton("M", SIDE_SIZE + GRID_WIDTH + 130,
                                TB_SIZE + 400, offset=-4, color=PATH_COLOR),
                    SmallButton("L", SIDE_SIZE + GRID_WIDTH + 190, TB_SIZE + 400)]

    if len(sys.argv) == 2:
        try:
            grid, start, end = load_grid(sys.argv[1])
        except FileNotFoundError:
            print("Entered a wrong file path!")

    while True:
        WINDOW.fill(BLACK)
        draw(grid, algo_buttons, other_buttons, maze_buttons, size_buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_grid_pos(pos)

                if row < GRID_SIZE and row >= 0 and col < GRID_SIZE and col >= 0:
                    node = grid[row][col]
                    if start is None:
                        node.select_start()
                        start = node
                    elif end is None and not node.is_start():
                        node.select_end()
                        end = node
                    else:
                        node.select_barrier()
                else:
                    for button in algo_buttons:
                        if button.rect.collidepoint(pos):
                            button.color = (186, 85, 211)
                            selected_algorithm = button.algorithm
                            for other in algo_buttons:
                                if other is not button:
                                    other.color = WHITE
                                    other.draw()

                    for button in maze_buttons:
                        if button.rect.collidepoint(pos):
                            grid, start, end = clear(
                                grid, start, end, save_barriers=False)
                            finished = False
                            if button.text == "Random":
                                grid = button.algorithm(grid)
                            elif button.text == "Division":
                                button.algorithm(
                                    grid, 1, GRID_SIZE - 2, 1, GRID_SIZE-2)
                                add_border(grid)

                    for button in size_buttons:
                        if button.rect.collidepoint(pos):
                            for other in size_buttons:
                                if other is not button:
                                    other.color = WHITE
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
                            finished = False
                            draw_grid(grid)

                    for button in other_buttons:
                        if button.rect.collidepoint(pos):
                            if button.text == "RESET":
                                grid = create_grid()
                                start, end = None, None
                                finished = False
                            elif button.text == "RUN":
                                if start and end and not finished and selected_algorithm:
                                    # Run selected algorithm
                                    for row in range(GRID_SIZE):
                                        for col in range(GRID_SIZE):
                                            current = grid[row][col]
                                            current.reset_neighbors(grid)

                                    path = selected_algorithm(grid, start, end)

                                    finished = True
                                    if not path:
                                        font = pygame.font.SysFont(FONT, 120)
                                        label = font.render(
                                            "PATH NOT FOUND!", True, RED)
                                        text_rect = label.get_rect(
                                            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                                        WINDOW.blit(label, text_rect)
                                        pygame.display.update()
                                        pygame.time.delay(500)
                                        finished = False
                                        print("PATH NOT FOUND")
                                    else:
                                        draw_path(grid, path)
                            elif button.text == "CLEAR":
                                grid, start, end = clear(grid, start, end)
                                finished = False
                                draw_grid(grid)
                            elif button.text == "SAVE":
                                save_grid(grid, start, end)

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_grid_pos(pos)
                if row < GRID_SIZE and row >= 0 and col < GRID_SIZE and col >= 0:
                    node = grid[row][col]
                    if node.is_start():
                        start = None
                    elif node.is_end():
                        end = None
                    node.unselect()
            elif pygame.mouse.get_pressed()[1]:
                pos = pygame.mouse.get_pos()
                print(pos)


def draw(grid, algo_buttons=[], other_buttons=[], maze_buttons=[], size_buttons=[]):
    WINDOW.fill(BLACK)
    for button in (algo_buttons + other_buttons + maze_buttons + size_buttons):
        button.draw()
    draw_legend()
    draw_grid(grid)

    pygame.display.update()


def draw_path(grid, path):
    length = len(path)
    for node in path:
        if not node.is_start() and not node.is_end():
            node.color = PATH_COLOR
            # If path is too long, skip the animation
            if length < 200:
                pygame.time.delay(round(25 * 20 // length))
                draw_grid(grid)
    draw_grid(grid)


def draw_grid(grid):
    # Draw nodes
    for row in grid:
        for node in row:
            pygame.draw.rect(WINDOW, node.color,
                             (node.x, node.y, SQUARE_SIZE, SQUARE_SIZE))

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


def draw_legend():
    draw_legend_node("Start node", START_COLOR,  offset=0)
    draw_legend_node("End node", END_COLOR,  offset=50)
    draw_legend_node("Free node", FREE_COLOR,  offset=100)
    draw_legend_node("Barrier node", BARRIER_COLOR, offset=150)
    draw_legend_node("Visited node", VISITED_COLOR,  offset=200)
    draw_legend_node("Path node", PATH_COLOR,  offset=250)
    draw_legend_node("Select a node",  offset=300, action="LMB")
    draw_legend_node("Unselect a node",  offset=350, action="RMB")


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


def get_grid_pos(pos):
    x, y = pos
    col = (y - TB_SIZE) // SQUARE_SIZE
    row = (x - SIDE_SIZE) // SQUARE_SIZE

    return row, col


def clear(grid, start=None, end=None, save_barriers=True):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            node = grid[row][col]
            if (node.is_barrier() and save_barriers) or node.is_start() or node.is_end():
                grid[row][col] = node.copy()
            else:
                grid[row][col] = GraphNode(row, col)
    if start:
        start = grid[start.row][start.col]
        start.select_start()
    if end:
        end = grid[end.row][end.col]
        end.select_end()

    return grid, start, end


def save_grid(grid, start, end):
    grid, start, end = clear(grid, start, end)
    now = datetime.now()
    with open(f"saved_grid_{now.day}_{now.month}_{now.hour}_{now.minute}.txt", "w") as file:
        for row in range(GRID_SIZE):
            line = []
            for col in range(GRID_SIZE):
                node = grid[row][col]
                if node.is_barrier():
                    line.append("B")
                elif node.is_start():
                    line.append("S")
                elif node.is_end():
                    line.append("E")
                else:
                    line.append("F")
            file.write(str(line)[1:-1])
            file.write("\n")

    print("Saved the grid!")


def load_grid(input):
    with open(input, "r") as file:
        grid = []
        start, end = None, None
        for line in file:
            line = line.replace("\n", "")
            row = line.split(", ")
            grid.append(row)

        if len(grid) != GRID_SIZE:
            raise Exception("File can't be loaded (wrong grid size)!")

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # removing the parentheses left from saving the grid ([1])
                id = grid[row][col][1]
                node = GraphNode(row, col)
                if id == "B":
                    node.select_barrier()
                elif id == "S":
                    node.select_start()
                    start = node
                elif id == "E":
                    node.select_end()
                    end = node
                grid[row][col] = node

        return grid, start, end


def create_grid():
    grid = [[GraphNode(row, col) for col in range(GRID_SIZE)]
            for row in range(GRID_SIZE)]

    return grid


# End parameter left for simplicity when calling selected_algorithm
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


# End parameter left for simplicity when calling selected_algorithm
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


def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    h = abs(x1 - x2) + abs(y1 - y2)

    return h


def h_euclidean(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    h = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return h


# random 1/3 maze generator
def random_maze(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            node = grid[row][col]
            if choice([True, False, False]):
                node.select_barrier()

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
                node.unselect()
            else:
                node.select_barrier()

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
                node.unselect()
            else:
                node.select_barrier()

        # Recursive calls
        divide(grid, min_x, x-1, min_y, max_y)
        divide(grid, x+1, max_x, min_y, max_y)


# Helper function for division()
def choose_orientation(width, height):
    # True for horizontal, False for vertical
    if width < height:
        return True
    elif width > height:
        return False
    else:
        return choice([True, False])


# Adds a border for each side of the grid
def add_border(grid):
    for i in range(GRID_SIZE):
        grid[0][i].select_barrier()
        grid[GRID_SIZE-1][i].select_barrier()
        grid[i][0].select_barrier()
        grid[i][GRID_SIZE-1].select_barrier()

    draw_grid(grid)


if __name__ == "__main__":
    main()
