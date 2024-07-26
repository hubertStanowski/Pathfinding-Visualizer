from constants import *
from helpers import run_checks

import pygame
from collections import deque
from heapq import heappush, heappop
from math import sqrt


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
                    neighbor.draw(screen.window, graph,
                                  update=screen.animate)
                    if screen.animate:
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

        current.draw(screen.window, graph, update=screen.animate)
        if screen.animate:
            pygame.time.delay(DELAYS[screen.animation_speed][graph.size])

        if current.is_end():
            return visited

        for neighbor in current.get_neighbors(graph):
            if not neighbor.been_visited():
                stack.append(neighbor)


# Dijkstra's algorithm
def dijkstras(screen):
    graph = screen.graph
    start = graph.get_start()

    start.update_source_dist(0)
    to_visit = [start]

    while to_visit:
        run_checks(screen)

        current = heappop(to_visit)
        current.set_visited()
        current.draw(screen.window, graph, update=screen.animate)
        if screen.animate:
            pygame.time.delay(DELAYS[screen.animation_speed][graph.size])

        for neighbor in current.get_neighbors(graph):
            new_dist = current.get_source_dist() + 1
            new_path = current.get_path() + [current]

            if new_dist < neighbor.get_source_dist():
                neighbor.update_source_dist(new_dist)
                neighbor.update_path(new_path)
                heappush(to_visit, neighbor)

            if current.is_end():
                return current.get_path() + [current]


# A* algorithm
def astar(screen):
    h = h_manhattan
    graph = screen.graph
    start, end = graph.get_start(), graph.get_end()

    open_list = [start]
    start.update_source_dist(0)
    start.update_target_dist(h(start.get_pos(), end.get_pos()))

    while open_list:
        run_checks(screen)

        current = heappop(open_list)
        current.set_visited()
        current.draw(screen.window, graph, update=screen.animate)
        if screen.animate:
            pygame.time.delay(DELAYS[screen.animation_speed][graph.size])

        if current.is_end():
            path = [end]
            temp = end
            while not temp.is_start():
                temp = temp.get_parent()
                path.append(temp)
            path.reverse()

            return path

        for neighbor in current.get_neighbors(graph):
            new_source_dist = current.get_source_dist() + 1

            if new_source_dist < neighbor.get_source_dist():
                neighbor.update_parent(current)
                neighbor.update_source_dist(new_source_dist)
                neighbor.update_target_dist(
                    new_source_dist + h(neighbor.get_pos(), end.get_pos()))

                if neighbor not in open_list:
                    heappush(open_list, neighbor)
                    neighbor.set_visited()
                    neighbor.draw(screen.window, graph,
                                  update=screen.animate)
                    if screen.animate:
                        pygame.time.delay(
                            DELAYS[screen.animation_speed][graph.size])


# Heuristic function for A* (Manhattan distance)
def h_manhattan(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    h = abs(x1 - x2) + abs(y1 - y2)

    return h


# Heuristic function for A* (Euclidean distance)
def h_euclidean(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    h = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return h
