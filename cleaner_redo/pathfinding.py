from parameters import *
from helpers import run_checks

import pygame
from collections import deque


# Breadth-first search algorithm
def BFS(window, start, graph, animation_speed):
    queue = deque([(start, [start])])

    while queue:
        run_checks()

        current, path = queue.popleft()
        for neighbor in current.get_neighbors(graph):
            if not neighbor.been_visited():
                if neighbor.is_end():
                    return path + [neighbor]
                else:
                    neighbor.set_visited()
                    neighbor.draw(window, graph.gridlines)
                    pygame.time.delay(DELAYS[animation_speed][graph.size])
                    queue.append((neighbor, path + [neighbor]))


def search(window, start, end, graph, selected_algorithm, animation_speed):
    if selected_algorithm == "BFS":
        return BFS(window, start, graph, animation_speed)
