from parameters import *
import pygame
from math import inf


class Graph:
    def __init__(self, size, gridlines=False):
        self.grid = [[GraphNode(row, col) for col in range(size)]
                     for row in range(size)]
        self.gridlines = gridlines
        self.size = size
        self.node_size = GRAPH_WIDTH // size  # Width and height of each node

    def draw(self, window, update=True):
        # Draws the graph and grid if toggled
        for row in self.grid:
            for node in row:
                node.draw(window, self.gridlines, update=False)
        if update:
            pygame.display.update()

    def get_grid_pos(self, pos):
        """
            Turns (x,y) position on the screen to its respective (row, col) coords on the grid.
        """
        x, y = pos
        col = (y - TB_SIZE) // self.node_size
        row = (x - SIDE_SIZE) // self.node_size

        return row, col

    def fill(self):
        for row in self.grid:
            for node in row:
                node.set_barrier()

    def add_border(self, depth=0):
        for i in range(self.size):
            self.grid[depth][i].set_barrier()
            self.grid[depth][i].draw()

            self.grid[self.size-1-depth][i].set_barrier()
            self.grid[self.size-1-depth][i].draw()

            self.grid[i][depth].set_barrier()
            self.grid[i][depth].draw()

            self.grid[i][self.size-1-depth].set_barrier()
            self.grid[i][self.size-1-depth].draw()

            pygame.time.delay(2 * DELAYS[animation_speed][self.size])

    def clear_graph(self, save_barriers=True):
        for row in range(self.size):
            for col in range(self.size):
                node = self.grid[row][col]
                if (node.is_barrier() and save_barriers) or node.is_start() or node.is_end():
                    self.grid[row][col].reset(keep_color=True)
                else:
                    self.grid[row][col].reset(keep_color=False)

    def toggle_gridlines(self):
        self.gridlines = not self.gridlines


class GraphNode:
    def __init__(self, row, col):
        self.x = SIDE_SIZE + row * self.node_size
        self.y = TB_SIZE + col * self.node_size
        self.row = row
        self.col = col
        self.color = FREE_COLOR
        self.source_dist = inf  # g score in a*
        self.target_dist = inf  # f score in a*

    def __lt__(self, other):
        if self.target_dist is not inf:
            return self.target_dist < other.target_dist

        return self.source_dist < other.source_dist

    def draw(self, window, gridlines, update=True):
        pygame.draw.rect(window, self.color,
                         (self.x, self.y, self.node_size, self.node_size))

        if gridlines:
            pygame.draw.line(window, LINE_COLOR, (self.x, self.y),
                             (self.x + self.node_size, self.y))

            pygame.draw.line(window, LINE_COLOR, (self.x, self.y),
                             (self.x, self.y + self.node_size))

            pygame.draw.line(window, LINE_COLOR, (self.x + self.node_size, self.y),
                             (self.x + self.node_size, self.y + self.node_size))

            pygame.draw.line(window, LINE_COLOR, (self.x, self.y + self.node_size),
                             (self.x + self.node_size, self.y + self.node_size))

        if update:
            pygame.display.update()

    def get_neighbors(self, graph):
        def valid(row, col):
            return 0 <= row < self.size and 0 <= col < self.size and not graph.grid[row][col].is_barrier()

        neighbors = []
        for dr, dc in DIRECTIONS:
            if valid(self.row+dr, self.col+dc):
                neighbors.append(graph.grid[self.row+dr][self.col+dc])

        return self.neighbors

    def pos(self):
        return self.row, self.col

    def set_start(self):
        self.color = START_COLOR

    def set_end(self):
        self.color = END_COLOR

    def set_free(self):
        self.color = FREE_COLOR

    def set_barrier(self):
        if self.is_free():
            self.color = BARRIER_COLOR

    def set_visited(self):
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
        self.source_dist = inf
        self.target_dist = inf
