from parameters import *
import pygame
from math import inf


class Graph:
    def __init__(self, size, gridlines=False):
        self.grid = [[GraphNode(row, col) for col in range(size)]
                     for row in range(size)]
        self.gridlines = gridlines

    def draw(self, window):
        # Draw the graph and grid if toggled
        for row in self.grid:
            for node in row:
                node.draw(window, self.gridlines, update=False)

        pygame.display.update()

    def get_grid_pos(self, pos):
        """
            Turns (x,y) position on the screen to its respective (row, col) coords on the grid.
        """
        x, y = pos
        col = (y - TB_SIZE) // NODE_SIZE
        row = (x - SIDE_SIZE) // NODE_SIZE

        return row, col

    def fill(self):
        for row in self.grid:
            for node in row:
                node.set_barrier()

    def add_border(self, depth=0):
        for i in range(GRAPH_SIZE):
            self.grid[depth][i].set_barrier()
            self.grid[depth][i].draw()

            self.grid[GRAPH_SIZE-1-depth][i].set_barrier()
            self.grid[GRAPH_SIZE-1-depth][i].draw()

            self.grid[i][depth].set_barrier()
            self.grid[i][depth].draw()

            self.grid[i][GRAPH_SIZE-1-depth].set_barrier()
            self.grid[i][GRAPH_SIZE-1-depth].draw()

            pygame.time.delay(2 * DELAYS[animation_speed][GRAPH_SIZE])

    def clear_graph(self, save_barriers=True):
        for row in range(GRAPH_SIZE):
            for col in range(GRAPH_SIZE):
                node = self.grid[row][col]
                if (node.is_barrier() and save_barriers) or node.is_start() or node.is_end():
                    self.grid[row][col].reset(keep_color=True)
                else:
                    self.grid[row][col].reset(keep_color=False)

    def toggle_gridlines(self):
        self.gridlines = not self.gridlines


class GraphNode:
    def __init__(self, row, col):
        self.x = SIDE_SIZE + row * NODE_SIZE
        self.y = TB_SIZE + col * NODE_SIZE
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
                         (self.x, self.y, NODE_SIZE, NODE_SIZE))

        if gridlines:
            pygame.draw.line(window, LINE_COLOR, (self.x, self.y),
                             (self.x + NODE_SIZE, self.y))

            pygame.draw.line(window, LINE_COLOR, (self.x, self.y),
                             (self.x, self.y + NODE_SIZE))

            pygame.draw.line(window, LINE_COLOR, (self.x + NODE_SIZE, self.y),
                             (self.x + NODE_SIZE, self.y + NODE_SIZE))

            pygame.draw.line(window, LINE_COLOR, (self.x, self.y + NODE_SIZE),
                             (self.x + NODE_SIZE, self.y + NODE_SIZE))

        if update:
            pygame.display.update()

    def get_neighbors(self, graph):
        def valid(row, col):
            return 0 <= row < GRAPH_SIZE and 0 <= col < GRAPH_SIZE and not graph.grid[row][col].is_barrier()

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
