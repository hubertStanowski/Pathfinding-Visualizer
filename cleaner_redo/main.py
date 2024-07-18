from parameters import *
from graph import *
import pygame

# from collections import deque
# from math import floor, inf, sqrt
# from heapq import heappop, heappush
# from queue import PriorityQueue
# from random import randrange, choice, shuffle


def main():
    pygame.init()
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Algorithms Visualizer")

    graph = Graph(GRAPH_SIZE, gridlines=True)
    start, end = None, None
    pathfinding_done = False
    selected_algorithm = None
    clock = pygame.time.Clock()

    while True:
        graph.draw(WINDOW)
        clock.tick(60)

        # For preventing multiple clicks
        wait = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if pygame.mouse.get_pressed()[0]:
                row, col = graph.get_grid_pos(pygame.mouse.get_pos())
                # Update the selected node
                if 0 <= row < GRAPH_SIZE and 0 <= col < GRAPH_SIZE:
                    node = graph.grid[row][col]
                    if start is None:
                        node.set_start()
                        start = node
                    elif end is None and not node.is_start():
                        node.set_end()
                        end = node
                    else:
                        node.set_barrier()
                    node.draw(WINDOW, graph.gridlines)

            elif pygame.mouse.get_pressed()[2]:
                row, col = graph.get_grid_pos(pygame.mouse.get_pos())
                # Unselect the selected node
                if 0 <= row < GRAPH_SIZE and 0 <= col < GRAPH_SIZE:
                    node = graph.grid[row][col]
                    if node.is_start():
                        start = None
                    elif node.is_end():
                        end = None
                    node.set_free()
                    node.draw(WINDOW, graph.gridlines)


if __name__ == "__main__":
    main()
