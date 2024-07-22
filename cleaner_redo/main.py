from parameters import *
from graph import *
from buttons import *
from legend import *
import pygame

# from collections import deque
# from math import floor, inf, sqrt
# from heapq import heappop, heappush
# from queue import PriorityQueue
# from random import randrange, choice, shuffle


def main():
    def draw(buttons=[]):
        WINDOW.fill(BARRIER_COLOR)
        graph.draw(WINDOW, update=False)
        draw_legend(WINDOW)
        for button in (buttons):
            button.draw(WINDOW)
        pygame.display.update()

    pygame.init()
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Algorithms Visualizer")

    size_buttons, animation_buttons = initialize_buttons()

    graph = Graph(45, gridlines=True)
    start, end = None, None
    pathfinding_done = False
    selected_algorithm = None
    clock = pygame.time.Clock()

    while True:
        draw(size_buttons+animation_buttons)
        clock.tick(60)

        # For preventing multi-clicks
        wait = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if pygame.mouse.get_pressed()[0]:
                row, col = graph.get_grid_pos(pygame.mouse.get_pos())
                # Update the selected node
                if 0 <= row < graph.size and 0 <= col < graph.size:
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
                if 0 <= row < graph.size and 0 <= col < graph.size:
                    node = graph.grid[row][col]
                    if node.is_start():
                        start = None
                    elif node.is_end():
                        end = None
                    node.set_free()
                    node.draw(WINDOW, graph.gridlines)


if __name__ == "__main__":
    main()
