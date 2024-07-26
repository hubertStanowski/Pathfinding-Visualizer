from constants import *

import pygame


# Helper function for handling events within algorithms
def run_checks(screen):
    # TODO allow for toggling gridlines while running algorithms
    # TODO allow for changing animation speed while running algorithms
    old_width, old_height = screen.window.get_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise Exception(
                "Exiting the program while executing an algorithm! (current settings will not be saved)")

        if event.type == pygame.VIDEORESIZE:
            new_width, new_height = get_updated_screen_dimensions(
                (old_width, old_height), (event.w, event.h))
            window = pygame.display.set_mode(
                (new_width, new_height), pygame.RESIZABLE)
            screen.resize_window(window)

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            finish_button = screen.buttons["control_buttons"]["FINISH"]
            if finish_button.rect.collidepoint(pos) and finish_button.is_visible():
                screen.animate = False


def get_updated_screen_dimensions(old_dimensions, new_dimensions):
    old_width, old_height = old_dimensions
    new_width, new_height = new_dimensions

    new_width, new_height = max(new_width, 850), max(new_height, 567)
    ratio = new_height/new_width
    delta_width = new_width - old_width
    delta_height = new_height - old_height

    if not (0.53 <= ratio <= 0.70):
        if abs(delta_width) >= abs(delta_height):
            new_height = new_width * 2/3
        else:
            new_width = 3/2 * new_height

    return new_width, new_height


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


def get_big_button_size(window):
    small_button_size = get_small_button_size(window)

    button_width = small_button_size * 5
    button_height = 7/4 * small_button_size

    return button_width, button_height


def get_small_button_size(window):
    _, window_height = window.get_size()
    return window_height * 0.042


def get_legend_font_size(window, graph):
    return round(get_small_button_size(window) * 1/2 + get_side_tab_size(window, graph) * 0.03)


def get_small_button_font_size(window):
    return round(get_small_button_size(window) * 0.95)


def get_big_button_font_size(window):
    _, big_button_height = get_big_button_size(window)

    return round(5/7 * big_button_height)


# Draw the path between start and end
def draw_path(screen, path):
    graph = screen.graph
    prev = path[0]
    for node in path[1:]:
        run_checks(screen)
        if not prev.is_start():
            prev.color = PATH_COLOR
            prev.draw(screen.window, graph, update=True)
        if not node.is_start() and not node.is_end():
            node.color = YELLOW
            node.draw(screen.window, graph, update=True)
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
    window_width, window_height = screen.window.get_size()
    label = font.render(
        "PATH NOT FOUND!", True, RED)
    label_rect = label.get_rect(
        center=(window_width // 2, window_height // 2))

    screen.window.blit(label, label_rect)
    pygame.display.update()
    pygame.time.delay(500)
