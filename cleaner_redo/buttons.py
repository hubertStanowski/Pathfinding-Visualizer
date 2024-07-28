from constants import *
from helpers import *

import pygame
from math import inf


class BigButton:
    def __init__(self, screen, label, x, y, color=FREE_COLOR,  visible=True, cooldown=0):
        self.label = label
        self.x = x
        self.y = y
        self.width, self.height = get_big_button_size(screen.window)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = color
        self.visible = visible
        self.cooldown = cooldown
        self.last_click_time = -inf

    def draw(self, window):
        if self.visible:
            pygame.draw.rect(window, self.color, self.rect)
            current_font = pygame.font.SysFont(
                FONT, get_big_button_font_size(window))
            label = current_font.render(self.label, True, BUTTON_FONT_COLOR)
            text_rect = label.get_rect(
                center=(self.x + self.width // 2, self.y + self.height // 2))
            window.blit(label, text_rect)

    def clicked(self, pos):
        valid = (self.visible and self.rect.collidepoint(pos))
        if self.cooldown:
            current_time = pygame.time.get_ticks()
            valid = valid and (
                current_time-self.last_click_time) > self.cooldown
            if valid:
                self.last_click_time = current_time

        return valid


class SmallButton:
    def __init__(self, screen, label, x, y, color=FREE_COLOR):
        self.label = label
        self.x = x
        self.y = y
        self.color = color
        self.size = get_small_button_size(screen.window)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        current_font = pygame.font.SysFont(
            FONT, get_small_button_font_size(window))
        label = current_font.render(self.label, True, BUTTON_FONT_COLOR)
        text_rect = label.get_rect(
            center=(self.x + self.size // 2, self.y + self.size // 2))
        window.blit(label, text_rect)

    def select(self):
        self.color = PATH_COLOR

    def unselect(self):
        self.color = FREE_COLOR

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


def initialize_buttons(screen, algorithm_running=False):
    window, graph = screen.window, screen.graph
    tb_size = get_tb_tab_size(window, graph)
    side_size = get_side_tab_size(window, graph)
    grid_size = get_grid_size(window, graph)
    small_button_size = get_small_button_size(window)
    legend_font_size = get_legend_font_size(window, graph)
    _, big_button_height = get_big_button_size(window)

    # Initialize buttons for changing graph size
    x = side_size * (1.41) + grid_size - small_button_size * 0.95
    y = tb_size + 10.1 * small_button_size + legend_font_size
    diff = small_button_size * 1.2

    size_buttons = {SMALL: SmallButton(screen, "S", x, y),
                    MEDIUM: SmallButton(screen, "M", x + diff, y),
                    LARGE: SmallButton(screen, "L", x + diff*2, y)}

    screen.add_buttons("size_buttons", size_buttons)
    update_size_buttons(screen)

    # Initialize buttons for changing animation speed
    y += small_button_size * 2

    animation_buttons = {SLOW: SmallButton(screen, "S", x, y),
                         NORMAL: SmallButton(screen, "N", x + diff, y),
                         FAST: SmallButton(screen, "F", x + diff*2, y)}

    screen.add_buttons("animation_buttons", animation_buttons)
    update_animation_buttons(screen)

    # Initialize action buttons
    x -= small_button_size * 0.95
    y += diff * 1.7
    diff_grid = small_button_size * 4.3 + legend_font_size + diff*1.7
    diff = big_button_height + small_button_size*0.5

    action_buttons = {"RUN": BigButton(screen, "RUN", x, y, color=START_COLOR, visible=(not algorithm_running), cooldown=DEFAULT_BUTTON_COOLDOWN),
                      "FINISH": BigButton(screen, "FINISH", x, y, color=VISITED_COLOR, visible=algorithm_running, cooldown=DEFAULT_BUTTON_COOLDOWN),
                      "CLEAR": BigButton(screen, "CLEAR", x, y + diff, color=YELLOW),
                      "RESET": BigButton(screen, "RESET", x, y + diff*2, color=END_COLOR)}

    screen.add_buttons("action_buttons", action_buttons)

    # Initialize gridline buttons
    gridline_buttons = {"GRID OFF": BigButton(screen, "GRID OFF", x, y-diff_grid, color=FREE_COLOR, cooldown=DEFAULT_BUTTON_COOLDOWN),
                        "GRID ON": BigButton(screen, "GRID ON", x, y-diff_grid, color=PATH_COLOR, cooldown=DEFAULT_BUTTON_COOLDOWN)}

    screen.add_buttons("gridline_buttons", gridline_buttons)
    update_gridline_buttons(screen)

    # Initialize buttons for maze-generating algorithms
    x -= side_size + grid_size
    y += diff * 2
    diff = big_button_height + small_button_size

    maze_buttons = {"Prim's": BigButton(screen, "Prim's", x, y - diff*3, color=MAZE_BUTTON_COLOR),
                    "Division": BigButton(screen, "Division", x, y - diff*2,  color=MAZE_BUTTON_COLOR),
                    "Backtrack": BigButton(screen, "Backtrack", x, y - diff, color=MAZE_BUTTON_COLOR),
                    "Random": BigButton(screen, "Random", x, y,  color=MAZE_BUTTON_COLOR)}

    screen.add_buttons("maze_buttons", maze_buttons)

    # Initialize buttons for pathfinding algorithms
    pathfinding_buttons = {"BFS": BigButton(screen, "BFS", x, y - diff*7),
                           "DFS": BigButton(screen, "DFS", x, y - diff*6),
                           "Dijkstra's": BigButton(screen, "Dijkstra's", x, y - diff*5),
                           "A*": BigButton(screen, "A*", x, y - diff*4)}

    screen.add_buttons("pathfinding_buttons", pathfinding_buttons)
    update_pathfinding_buttons(screen)
