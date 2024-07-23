from parameters import *
from helpers import run_checks

import pygame
from collections import deque


# Breadth-first search algorithm
def BFS(screen):
    graph = screen.graph
    queue = deque([(graph.start, [graph.start])])

    while queue:
        run_checks()

        current, path = queue.popleft()
        for neighbor in current.get_neighbors(graph):
            if not neighbor.been_visited():
                if neighbor.is_end():
                    return path + [neighbor]
                else:
                    neighbor.set_visited()
                    neighbor.draw(screen.window, graph.gridlines)
                    pygame.time.delay(
                        DELAYS[screen.animation_speed][graph.size])
                    queue.append((neighbor, path + [neighbor]))
