from constants import *
from helpers import *
from pathfinding import *

import pygame
from math import inf


class Graph:
    def __init__(self, window, size, gridlines=False):
        self.gridlines = gridlines
        self.size = size
        self.node_size = round(get_grid_size(window, self) / size)
        self.grid = [[GraphNode(row, col) for col in range(size)]
                     for row in range(size)]
        self.start = None
        self.end = None

    def draw(self, window, update=True):
        # Draws the graph and gridlines if toggled
        for row in self.grid:
            for node in row:
                node.draw(window, self, update=False)
        if update:
            pygame.display.update()

    def resize_nodes(self, window):
        self.node_size = round(get_grid_size(window, self) / self.size)

    def search(self, screen, selected_algorithm):
        if selected_algorithm == "BFS":
            return BFS(screen)
        elif selected_algorithm == "DFS":
            return DFS(screen)

    def get_grid_pos(self, window, pos):
        """
            Turns (x,y) position on the screen to its respective (row, col) coords on the grid.
        """
        x, y = pos
        col = (y - get_tb_tab_size(window, self)) // self.node_size
        row = (x - get_side_tab_size(window, self)) // self.node_size

        return row, col

    def fill(self):
        for row in self.grid:
            for node in row:
                node.set_barrier()

    def add_border(self, animation_speed, depth=0):
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

    def clear(self, save_barriers=True):
        for row in range(self.size):
            for col in range(self.size):
                node = self.grid[row][col]
                if (node.is_barrier() and save_barriers) or node.is_start() or node.is_end():
                    node.reset(keep_color=True)
                else:
                    node.reset(keep_color=False)

    def toggle_gridlines(self):
        self.gridlines = not self.gridlines

    def select_node(self, node):
        if not self.start:
            self.set_start(node)
        elif not self.end and not node.is_start():
            self.set_end(node)
        else:
            node.set_barrier()

    def unselect_node(self, node):
        if node.is_start():
            self.reset_start()
        elif node.is_end():
            self.reset_end()

        node.set_free()

    def is_valid_node(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def set_start(self, node):
        self.start = node
        node.set_start()

    def set_end(self, node):
        self.end = node
        node.set_end()

    def reset_start(self):
        self.start = None

    def reset_end(self):
        self.end = None


class GraphNode:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = FREE_COLOR
        self.source_dist = inf  # g score in a*
        self.target_dist = inf  # f score in a*

    def __lt__(self, other):
        if self.target_dist is not inf:
            return self.target_dist < other.target_dist

        return self.source_dist < other.source_dist

    def draw(self, window, graph, update=True):
        x = get_side_tab_size(window, graph) + self.row * graph.node_size
        y = get_tb_tab_size(window, graph) + self.col * graph.node_size

        pygame.draw.rect(window, self.color,
                         (x, y, graph.node_size, graph.node_size))

        if graph.gridlines:
            pygame.draw.line(window, LINE_COLOR, (x, y),
                             (x + graph.node_size, y))

            pygame.draw.line(window, LINE_COLOR, (x, y),
                             (x, y + graph.node_size))

            pygame.draw.line(window, LINE_COLOR, (x + graph.node_size, y),
                             (x + graph.node_size, y + graph.node_size))

            pygame.draw.line(window, LINE_COLOR, (x, y + graph.node_size),
                             (x + graph.node_size, y + graph.node_size))

        if update:
            pygame.display.update()

    def get_neighbors(self, graph):
        def valid_neighbor(row, col):
            return graph.is_valid_node(row, col) and not graph.grid[row][col].is_barrier()

        neighbors = []
        for dr, dc in DIRECTIONS:
            if valid_neighbor(self.row+dr, self.col+dc):
                neighbors.append(graph.grid[self.row+dr][self.col+dc])

        return neighbors

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
