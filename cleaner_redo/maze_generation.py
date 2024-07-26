from constants import *
from helpers import run_checks

import pygame
from random import choice, shuffle


# Recurisve backtracker maze generator
def backtrack(screen, row, col):
    graph = screen.graph
    grid = graph.grid
    current = grid[row][col]
    if current.is_barrier():
        current.set_free()
        current.draw(screen.window, graph, update=screen.animate)
        if screen.animate:
            pygame.time.delay(DELAYS[screen.animation_speed][graph.size])

    valid_directions = DIRECTIONS.copy()
    shuffle(valid_directions)

    while valid_directions:
        run_checks(screen)

        # Pick a random far neighbor of current
        direction = valid_directions.pop()
        new_row, new_col = row + direction[0] * 2, col + direction[1] * 2
        if graph.is_valid_node(new_row, new_col, offset=1):
            far_neighbor = grid[new_row][new_col]

            if not far_neighbor.is_free():
                new_row, new_col = row + direction[0], col + direction[1]
                if graph.is_valid_node(new_row, new_col, offset=1):
                    # Turn the node between current and far_neighbor into a passage
                    link = grid[new_row][new_col]
                    if link.is_barrier():
                        link.set_free()
                        link.draw(screen.window, graph, update=screen.animate)
                        if screen.animate:
                            pygame.time.delay(
                                DELAYS[screen.animation_speed][graph.size])

                # Recursive call
                backtrack(screen, far_neighbor.row, far_neighbor.col)


# Random maze generator (1/3 chance for barrier)
def random_maze(screen):
    graph_size = screen.graph.size
    for row in range(graph_size):
        for col in range(graph_size):
            run_checks(screen)

            node = screen.graph.grid[row][col]
            if choice([True, False, False]):
                node.set_barrier()
                node.draw(screen.window, screen.graph, update=screen.animate)
                if screen.animate:
                    pygame.time.delay(
                        DELAYS[screen.animation_speed][graph_size] // 2)
