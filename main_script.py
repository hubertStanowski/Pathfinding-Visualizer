import pygame
from collections import deque
from math import inf, sqrt
from heapq import heappop, heappush
from queue import PriorityQueue
from datetime import datetime
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000
GRID_WIDTH, GRID_HEIGHT = 900, 900

GRID_SIZE = 30
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
BUTTON_COLOR = PATH_COLOR

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
        return self.x, self.y

    def select_start(self):
        self.color = START_COLOR

    def unselect(self):
        self.color = FREE_COLOR

    def select_end(self):
        self.color = END_COLOR

    def select_barrier(self):
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


def main():
    grid = [[GraphNode(row, col) for col in range(GRID_SIZE)]
            for row in range(GRID_SIZE)]
    start, end = None, None
    finished = False
    selected_algorithm = None
    algo_buttons = [Button(BFS, "BFS", 50, 50), Button(DFS, "DFS", 50, 170),
                    Button(dijkstras, "Dijkstra's", 50, 290, offset=-54), Button(astar, "A*", 50, 410, offset=20)]
    other_buttons = [Button(None, "RUN", 50, 570, color=GREEN), Button(None, "CLEAR", 50, 690, offset=-35, color=YELLOW), Button(None, "RESET", 50, 810, offset=-25,
                                                                                                                                 color=RED)]
    while True:
        WINDOW.fill(BLACK)
        draw(grid, algo_buttons, other_buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_grid_pos(pos)

                if row < GRID_SIZE and row >= 0 and col < GRID_SIZE and col >= 0:
                    node = grid[row][col]
                    if node.is_free():
                        if start is None:
                            node.select_start()
                            start = node
                        elif end is None:
                            node.select_end()
                            end = node
                        else:
                            node.select_barrier()
                else:
                    for button in algo_buttons:
                        if button.rect.collidepoint(pos):
                            button.color = BUTTON_COLOR
                            selected_algorithm = button.algorithm
                            button.draw()
                            for other in algo_buttons:
                                if other is not button:
                                    other.color = WHITE
                                    other.draw()
                    for button in other_buttons:
                        if button.rect.collidepoint(pos):
                            if button.text == "RESET":
                                grid = [[GraphNode(row, col) for col in range(GRID_SIZE)]
                                        for row in range(GRID_SIZE)]
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
                                        pygame.time.delay(1500)
                                        print("PATH NOT FOUND")
                                    else:
                                        draw_path(grid, path, start, end)
                            elif button.text == "CLEAR":
                                grid, start, end = clear(grid, start, end)
                                finished = False
                                draw_grid(grid)

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


def draw(grid, algo_buttons=[], other_buttons=[]):
    for button in (algo_buttons + other_buttons):
        button.draw()
    draw_grid(grid)
    pygame.display.update()


def draw_path(grid, path, start, end):
    start.color = GREEN

    for node in path:
        if node is not start and node is not end:
            node.color = PATH_COLOR

    end.color = RED

    draw(grid)


def draw_grid(grid):
    # Draw nodes
    for row in grid:
        for node in row:
            pygame.draw.rect(WINDOW, node.color,
                             (node.x, node.y, SQUARE_SIZE, SQUARE_SIZE))

    # Draw lines
    line_color = GRAY
    x, y = SIDE_SIZE, TB_SIZE
    width, height = GRID_WIDTH, GRID_HEIGHT

    for i in range(GRID_SIZE + 1):
        pygame.draw.line(WINDOW, line_color, (x, y + i *
                         SQUARE_SIZE), (x + width, y + i * SQUARE_SIZE))

        for j in range(GRID_SIZE + 1):
            pygame.draw.line(WINDOW, line_color, (x + j *
                             SQUARE_SIZE, y), (x + j * SQUARE_SIZE, y + height))


def get_grid_pos(pos):
    x, y = pos
    col = (y - TB_SIZE) // SQUARE_SIZE
    row = (x - SIDE_SIZE) // SQUARE_SIZE

    return row, col


def clear(grid, start=None, end=None):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            node = grid[row][col]
            if node.is_barrier() or node.is_start() or node.is_end():
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

    print("Saved the grid")


def read_grid(input):
    with open(input, "r") as file:
        grid = []
        start, end = None, None
        for line in file:
            line = line.replace("\n", "")
            row = line.split(", ")
            grid.append(row)

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


# End parameter left for simplicity when calling selected_algorithm
def BFS(grid, start, end):
    path = [start]
    bfs_queue = deque([[start, path]])

    while bfs_queue:
        current, path = bfs_queue.popleft()

        draw(grid)
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

    draw(grid)
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

        draw(grid)
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
    # TODO refactor into get_pos
    start.source_dist = h((start.row, start.col), (end.row, end.col))
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

            return path

        draw(grid)
        for neighbor in current.neighbors:
            new_g_score = current.source_dist + 1
            if new_g_score < neighbor.source_dist:
                parents[neighbor] = current
                neighbor.source_dist = new_g_score
                neighbor.target_dist = new_g_score + \
                    h((neighbor.row, neighbor.col), (end.row, end.col))
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


if __name__ == "__main__":
    main()
