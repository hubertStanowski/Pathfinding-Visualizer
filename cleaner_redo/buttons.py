from constants import *
from helpers import *
import pygame


class BigButton:
    def __init__(self, label, x, y, color=FREE_COLOR,  visible=True):
        self.label = label
        self.x = x
        self.y = y
        self.rect = pygame.Rect(
            x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.color = color
        self.visible = visible

    def draw(self, window, graph):
        if not self.visible:
            return

        pygame.draw.rect(window, self.color, self.rect)
        current_font = pygame.font.SysFont(FONT, 60)
        label = current_font.render(self.label, True, BLACK)
        text_rect = label.get_rect(center=(
            self.x + BUTTON_WIDTH // 2, self.y + (BUTTON_HEIGHT) // 2))
        window.blit(label, text_rect)


# default scale x + 5
class SmallButton:
    def __init__(self, screen, label, x, y, color=FREE_COLOR):
        self.label = label
        self.x = x
        self.y = y
        self.color = color
        self.size = get_small_button_size(screen.window)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, window, graph):
        pygame.draw.rect(window, self.color, self.rect)
        current_font = pygame.font.SysFont(
            FONT, get_small_button_font_size(window))
        label = current_font.render(self.label, True, BLACK)
        text_rect = label.get_rect(
            center=(self.x + self.size // 2, self.y + self.size // 2))
        window.blit(label, text_rect)

    def select(self):
        self.color = PATH_COLOR

    def unselect(self):
        self.color = FREE_COLOR


def initialize_buttons(screen):
    window, graph = screen.window, screen.graph
    window_width, window_height = window.get_size()
    tb_size = get_tb_tab_size(window, graph)
    side_size = get_side_tab_size(window, graph)
    grid_size = get_grid_size(window, graph)
    small_button_size = get_small_button_size(window)
    legend_font_size = get_legend_font_size(window, graph)

    # Initialize buttons for changing graph size
    x = side_size * (1.41) + grid_size - small_button_size * 0.95
    y = tb_size + 10.1 * small_button_size + legend_font_size
    diff = small_button_size * 1.2

    size_buttons = {25: SmallButton(screen, "S", x, y),
                    45: SmallButton(screen, "M", x + diff, y),
                    75: SmallButton(screen, "L", x + diff*2, y)}

    screen.add_buttons("size_buttons", size_buttons)
    update_size_buttons(screen)

    # Initialize buttons for changing animation speed
    y += small_button_size * 2

    animation_buttons = {"S": SmallButton(screen, "S", x, y),
                         "N": SmallButton(screen, "N", x + diff, y),
                         "F": SmallButton(screen, "F", x + diff*2, y)}

    screen.add_buttons("animation_buttons", animation_buttons)
    update_animation_buttons(screen)

    # Initialize buttons for graph management and view
    diff = 115
    control_buttons = {"GRID OFF": BigButton("GRID OFF", window_width - (BUTTON_WIDTH + 50), tb_size + 360, color=FREE_COLOR),
                       "GRID ON": BigButton("GRID ON", window_width - (BUTTON_WIDTH + 50), tb_size + 360, color=BLUE),
                       "RUN": BigButton("RUN", window_width - (BUTTON_WIDTH + 50), tb_size + 10 + diff*5, color=START_COLOR),
                       "CLEAR": BigButton("CLEAR", window_width - (BUTTON_WIDTH + 50), tb_size + 10 + diff*6, color=YELLOW),
                       "RESET": BigButton("RESET", window_width - (BUTTON_WIDTH + 50), tb_size + 10 + diff*7, color=END_COLOR)}

    screen.add_buttons("control_buttons", control_buttons)
    update_gridline_buttons(screen)

    # Initialize buttons for pathfinding algorithms
    pathfinding_buttons = {"BFS": BigButton("BFS", 50, tb_size + 10),
                           "DFS": BigButton("DFS", 50, tb_size + 10 + diff),
                           "Dijkstra's": BigButton("Dijkstra's", 50, tb_size + 10 + diff*2),
                           "A*": BigButton("A*", 50, tb_size + 10 + diff*3)}

    screen.add_buttons("pathfinding_buttons", pathfinding_buttons)

    # Initialize buttons for maze-generating algorithms
    maze_buttons = {"Prim's": BigButton("Prim's", 50, tb_size + 10 + diff*4, color=LIGHT_GREEN),
                    "Division": BigButton("Division", 50, tb_size + 10 + diff*5,  color=LIGHT_GREEN),
                    "Backtrack": BigButton("Backtrack", 50, tb_size + 10 + diff*6, color=LIGHT_GREEN),
                    "Random": BigButton("Random", 50, tb_size + 10 + diff*7,  color=LIGHT_GREEN)}

    screen.add_buttons("maze_buttons", maze_buttons)


def update_size_buttons(screen):
    for label, button in screen.buttons["size_buttons"].items():
        if screen.graph.size == label:
            button.select()
        else:
            button.unselect()


def update_animation_buttons(screen):
    for label, button in screen.buttons["animation_buttons"].items():
        if label == screen.animation_speed:
            button.select()
        else:
            button.unselect()


def update_gridline_buttons(screen, toggle=False):
    grid_on = screen.buttons["control_buttons"]["GRID ON"]
    grid_off = screen.buttons["control_buttons"]["GRID OFF"]
    if screen.graph.gridlines:
        grid_on.visible = True
        grid_off.visible = False
    else:
        grid_on.visible = False
        grid_off.visible = True

    if toggle:
        grid_on.visible = not grid_on.visible
        grid_off.visible = not grid_off.visible


def update_pathfinding_buttons(screen, selected):
    for label, button in screen.buttons["pathfinding_buttons"].items():
        if label != selected:
            button.color = FREE_COLOR
        else:
            button.color = PATH_COLOR
