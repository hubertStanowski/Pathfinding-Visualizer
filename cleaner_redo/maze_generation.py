from constants import *
from helpers import run_checks

import pygame
from random import choice


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
