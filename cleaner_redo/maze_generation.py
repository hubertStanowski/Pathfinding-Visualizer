from constants import *
from helpers import run_checks

from random import choice, shuffle, randrange
from math import floor


# Prim's maze generator
def prims(screen):
    graph = screen.graph
    grid = graph.grid
    row, col = randrange(graph.size), randrange(graph.size)

    # [0] = middle node between current frontier and previous frontier
    # [1] = current frontier
    frontiers = [[(row, col), (row, col)]]

    while frontiers:
        run_checks(screen)

        frontier = choice(frontiers)
        frontiers.remove(frontier)
        row, col = frontier.pop()
        current = grid[row][col]

        if current.is_barrier():
            mid_row, mid_col = frontier.pop()
            mid = grid[mid_row][mid_col]

            # Create a passage
            current.set_free()
            current.draw(screen)
            if mid.is_barrier():
                mid.set_free()
                mid.draw(screen)

            # If in the graph, add fontiers of the current frontier (with nodes in between them) to the list of frontiers
            if (row >= 2 and grid[row-2][col].is_barrier()):
                frontiers.append([(row-1, col), (row-2, col)])
            if (col >= 2 and grid[row][col-2].is_barrier()):
                frontiers.append([(row, col-1), (row, col-2)])
            if (row < graph.size-2 and grid[row+2][col].is_barrier()):
                frontiers.append([(row+1, col), (row+2, col)])
            if (col < graph.size-2 and grid[row][col+2].is_barrier()):
                frontiers.append([(row, col+1), (row, col+2)])


# Recursive division maze generator
def divide(screen, min_row, max_row, min_col,  max_col):
    width, height = max_row - min_row, max_col - min_col
    horizontal = choose_orientation(width, height)
    grid = screen.graph.grid

    if horizontal:
        if width < 2:
            return

        # Randomly generate a wall
        col = floor(randrange(min_col, max_col+1) / 2) * 2

        # Randomly generate a hole
        hole = floor(randrange(min_row, max_row+1) / 2) * 2 + 1

        for row in range(min_row, max_row+1):
            run_checks(screen)
            current = grid[col][row]
            if row == hole and not current.is_start() and not current.is_end():
                current.set_free()
            else:
                current.set_barrier()

            current.draw(screen)

        divide(screen, min_row, max_row, min_col, col-1)
        divide(screen, min_row, max_row, col+1, max_col)
    else:
        if height < 2:
            return

        # Randomly generate a wall
        row = floor(randrange(min_row, max_row+1) / 2) * 2

        # Randomly generate a hole
        hole = floor(randrange(min_col, max_col+1) / 2) * 2 + 1

        for col in range(min_col, max_col+1):
            run_checks(screen)
            current = grid[col][row]
            if col == hole and not current.is_start() and not current.is_end():
                current.set_free()
            else:
                current.set_barrier()

            current.draw(screen)

        divide(screen, min_row, row-1, min_col, max_col)
        divide(screen, row+1, max_row, min_col, max_col)


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
