from pathfinding import *
from parameters import *


import pygame


# Helper function for handling events within algorithms
def run_checks():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise Exception(
                "Exiting the program while executing an algorithm! (current settings will not be saved)")

# GRAPH_WIDTH, GRAPH_HEIGHT = 900, 900
# WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000
# SIDE_SIZE = (WINDOW_WIDTH - GRAPH_WIDTH) // 2  # Left and right tab size
# TB_SIZE = (WINDOW_HEIGHT - GRAPH_HEIGHT) // 2  # Top and bottom tab size
# BUTTON_WIDTH, BUTTON_HEIGHT = (SIDE_SIZE - 100) + 5, 70
# SMALL_BUTTON_SIZE = 40


def get_grid_size(window):
    return round(min(window.get_size()) * 0.9)


# Top and bottom tab size
def get_tb_tab_size(window):
    _, window_height = window.get_size()

    return round((window_height - get_grid_size(window)) / 2)


def get_side_tab_size(window):
    window_width, _ = window.get_size()

    return round((window_width - get_grid_size(window)) / 2)


def get_big_button_size(window):
    window_width, window_height = window.get_size()
    button_width = get_side_tab_size(window) - (1/15 * window_width)
    button_height = 7/100 * window_height

    return button_width, button_height


def get_small_button_size(window):
    return get_side_tab_size(window) * 4/30


# Draw the path between start and end
def draw_path(screen, path):
    graph = screen.graph
    prev = path[0]
    for node in path[1:]:
        run_checks()
        if not prev.is_start():
            prev.color = PATH_COLOR
            prev.draw(screen.window, graph.gridlines, update=True)
        if not node.is_start() and not node.is_end():
            node.color = YELLOW
            node.draw(screen.window, graph.gridlines, update=True)
            prev = node
        # Delay based on length relative to GRAPH_SIZE and base delay
        delay = round(4 * graph.size / len(path) * 6 *
                      DELAYS[screen.animation_speed][graph.size])
        if delay > 80:
            delay = 80
        pygame.time.delay(delay)


# Inform that no path has been found
def handle_no_path(screen):
    font = pygame.font.SysFont(FONT, 120)
    label = font.render(
        "PATH NOT FOUND!", True, RED)
    label_rect = label.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    screen.window.blit(label, label_rect)
    pygame.display.update()
    pygame.time.delay(500)
