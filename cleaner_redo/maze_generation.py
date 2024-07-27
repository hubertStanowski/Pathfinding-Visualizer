from constants import *
from helpers import run_checks

from random import choice, shuffle, randrange
from math import floor


# Recursive division maze generator
def divide(screen, min_x, max_x, min_y,  max_y):
    width, height = max_x - min_x, max_y - min_y
    horizontal = choose_orientation(width, height)
    grid = screen.graph.grid

    if horizontal:
        if width < 2:
            return

        # Randomly generate a wall
        y = floor(randrange(min_y, max_y+1) / 2) * 2

        # Randomly generate a hole
        hole = floor(randrange(min_x, max_x+1) / 2) * 2 + 1

        for x in range(min_x, max_x+1):
            run_checks(screen)
            current = grid[y][x]
            if x == hole and not current.is_start() and not current.is_end():
                current.set_free()
            else:
                current.set_barrier()

            current.draw(screen)

        divide(screen, min_x, max_x, min_y, y-1)
        divide(screen, min_x, max_x, y+1, max_y)
    else:
        if height < 2:
            return

        # Randomly generate a wall
        x = floor(randrange(min_x, max_x+1) / 2) * 2

        # Randomly generate a hole
        hole = floor(randrange(min_y, max_y+1) / 2) * 2 + 1

        for y in range(min_y, max_y+1):
            run_checks(screen)
            current = grid[y][x]
            if y == hole and not current.is_start() and not current.is_end():
                current.set_free()
            else:
                current.set_barrier()

            current.draw(screen)

        divide(screen, min_x, x-1, min_y, max_y)
        divide(screen, x+1, max_x, min_y, max_y)


# Helper function for divide()
def choose_orientation(width, height):
    # True for horizontal, False for vertical
    if width < height:
        return True
    elif width > height:
        return False
    else:
        return choice([True, False])


# Recursive backtracker maze generator
def backtrack(screen, row, col):
    graph = screen.graph
    grid = graph.grid
    current = grid[row][col]
    if current.is_barrier():
        current.set_free()
        current.draw(screen)

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
                        link.draw(screen)

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
                node.draw(screen)
