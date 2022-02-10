import pygame
from collections import deque


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
        self.source_dist = None
        self.path = None

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
    def __init__(self, text, x, y, offset=0):
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
    buttons = [Button("BFS", 50, 60), Button("DFS", 50, 200),
               Button("Dijkstra's", 50, 340, -54), Button("A*", 50, 480, 20)]
    while True:
        WINDOW.fill(BLACK)
        draw(grid, buttons)
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
                if event.key in [pygame.K_RETURN, pygame.K_SPACE] and start and end:
                    # Run selected algorithm
                    for row in range(GRID_SIZE):
                        for col in range(GRID_SIZE):
                            current = grid[row][col]
                            current.reset_neighbors(grid)

                    path = BFS(grid, start, end)
                    if not path:
                        print("PATH NOT FOUND")
                        return 0
                    else:
                        draw_path(grid, path, start, end)

                if event.key in [pygame.K_BACKSPACE, pygame.K_ESCAPE]:
                    grid = [[GraphNode(row, col) for col in range(GRID_SIZE)]
                            for row in range(GRID_SIZE)]
                    start, end = None, None


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


def BFS(grid, start, end):
    path = [start]
    bfs_queue = deque([[start, path]])

    while bfs_queue:
        current, path = bfs_queue.popleft()

        if not current.is_start:
            current.set_visited()

        draw(grid)
        for neighbor in current.neighbors:
            if not neighbor.been_visited() and not neighbor.is_start():
                if neighbor is end:
                    return path + [neighbor]
                else:
                    neighbor.set_visited()
                    bfs_queue.append([neighbor, path + [neighbor]])


if __name__ == "__main__":
    main()
