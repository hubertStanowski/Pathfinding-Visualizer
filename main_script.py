import pygame
from collections import deque
from math import inf, sqrt
from heapq import heappop, heappush
from queue import PriorityQueue
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


FONT = None


BARRIER_COLOR = BLACK
FREE_COLOR = WHITE
PATH_COLOR = (186, 85, 211)
VISITED_COLOR = BLUE
START_COLOR = GREEN
END_COLOR = RED

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

    def not_barrier(self):
        return self.color != BARRIER_COLOR

    def been_visited(self):
        return self.color == VISITED_COLOR

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

    # DEBUGGING TOOL
    def select_neighbors(self, grid):
        self.reset_neighbors(grid)
        print(f"<<< ({self.row}, {self.col}) >>>")
        for neighbor in self.neighbors:
            neighbor.color = VISITED_COLOR
            print((neighbor.row, neighbor.col))

        draw(grid)


class Button:
    def __init__(self, algorithm, text, x, y, offset=0):
        self.algorithm = algorithm
        self.text = text
        self.x = x
        self.y = y
        self.offset = offset
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.color = WHITE

    def draw(self):
        pygame.draw.rect(WINDOW, self.color, self.rect)
        font = pygame.font.SysFont(FONT, 60)
        label = font.render(self.text, 30, BLACK)
        text_rect = pygame.Rect(
            self.x + 60 + self.offset, self.y + 15, BUTTON_WIDTH, BUTTON_HEIGHT)
        WINDOW.blit(label, text_rect)


def main():
    grid = [[GraphNode(row, col) for col in range(GRID_SIZE)]
            for row in range(GRID_SIZE)]
    start, end = None, None
    algo_buttons = [Button(BFS, "BFS", 50, 60), Button(DFS, "DFS", 50, 200),
                    Button(dijkstras, "Dijkstra's", 50, 340, -54), Button(astar, "A*", 50, 480, 20)]
    finished = False
    selected_algorithm = None
    while True:
        WINDOW.fill(BLACK)
        draw(grid, algo_buttons)
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
                            button.color = PATH_COLOR
                            selected_algorithm = button.algorithm
                            button.draw()
                            for other in algo_buttons:
                                if other is not button:
                                    other.color = WHITE
                                    other.draw()

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

            if pygame.mouse.get_pressed()[1]:
                pos = pygame.mouse.get_pos()
                print("################")
                print(pos)
                row, col = get_grid_pos(pos)
                print((row, col))
                print("################")
                if row < GRID_SIZE and row >= 0 and col < GRID_SIZE and col >= 0:
                    node = grid[row][col]
                    node.select_neighbors(grid)

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE] and start and end and not finished and selected_algorithm:
                    # Run selected algorithm
                    for row in range(GRID_SIZE):
                        for col in range(GRID_SIZE):
                            current = grid[row][col]
                            current.reset_neighbors(grid)

                    path = selected_algorithm(grid, start, end)

                    finished = True
                    if not path:
                        print("PATH NOT FOUND")
                        return 0
                    else:
                        draw_path(grid, path, start, end)

                if event.key in [pygame.K_BACKSPACE, pygame.K_ESCAPE]:
                    grid = [[GraphNode(row, col) for col in range(GRID_SIZE)]
                            for row in range(GRID_SIZE)]
                    start, end = None, None
                    finished = False


def draw(grid, buttons=[]):
    for button in buttons:
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


# <<< Remove target from parameters when buttons done >>>
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
    # refactor into get_pos?
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
