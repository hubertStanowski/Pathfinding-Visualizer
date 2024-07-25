from constants import *
from helpers import run_checks

import pygame
from collections import deque


# Breadth-first search algorithm
def BFS(screen):
    graph = screen.graph
    queue = deque([(graph.start, [graph.start])])

    while queue:
        run_checks(screen)

        current, path = queue.popleft()
        for neighbor in current.get_neighbors(graph):
            if not neighbor.been_visited():
                if neighbor.is_end():
                    return path + [neighbor]
                else:
                    neighbor.set_visited()
                    neighbor.draw(screen.window, graph)
                    pygame.time.delay(
                        DELAYS[screen.animation_speed][graph.size])
                    queue.append((neighbor, path + [neighbor]))


# Depth-first search algorithm
def DFS(screen):
    graph = screen.graph
    stack = [graph.start]
    visited = []

    while stack:
        run_checks(screen)

        current = stack.pop()
        current.set_visited()
        visited.append(current)

        current.draw(screen.window, graph)
        pygame.time.delay(DELAYS[screen.animation_speed][graph.size])

        if current.is_end():
            return visited

        for neighbor in current.get_neighbors(graph):
            if not neighbor.been_visited():
                stack.append(neighbor)
