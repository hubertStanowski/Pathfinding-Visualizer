from parameters import *

import pygame


# Helper function for handling events within algorithms
def run_checks():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise Exception(
                "Exiting the program while executing an algorithm! (current settings will not be saved)")


# def get_grid_size(window):
#     return round(min(window.get_size()) * 0.9)

def get_grid_size(window, graph):
    intended = round(min(window.get_size()) * 0.9)
    node_size = round(intended / graph.size)
    actual = node_size * graph.size

    return actual


# Top and bottom tab size
def get_tb_tab_size(window, graph):
    _, window_height = window.get_size()

    return round((window_height - get_grid_size(window, graph)) / 2)


def get_side_tab_size(window, graph):
    window_width, _ = window.get_size()

    return round((window_width - get_grid_size(window, graph)) / 2)


def get_big_button_size(window, graph):
    window_width, window_height = window.get_size()
    button_width = get_side_tab_size(window, graph) - (1/15 * window_width)
    button_height = 7/100 * window_height

    return button_width, button_height


def get_small_button_size(window, graph):
    return get_side_tab_size(window, graph) * 4/30


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
