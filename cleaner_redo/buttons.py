from constants import *
from helpers import *
import pygame


class BigButton:
    def __init__(self, screen, label, x, y, color=FREE_COLOR,  visible=True):
        self.label = label
        self.x = x
        self.y = y
        self.width, self.height = get_big_button_size(screen.window)
        self.rect = pygame.Rect(
            x, y, self.width, self.height)
        self.color = color
        self.visible = visible

    def draw(self, window):
        if not self.visible:
            return

        pygame.draw.rect(window, self.color, self.rect)
        current_font = pygame.font.SysFont(
            FONT, get_big_button_font_size(window))
        label = current_font.render(self.label, True, BLACK)
        text_rect = label.get_rect(center=(
            self.x + self.width // 2, self.y + self.height // 2))
        window.blit(label, text_rect)

    def is_visible(self):
        return self.visible


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

    # Initialize control buttons
    x -= small_button_size * 0.95
    y += diff * 1.7
    diff_grid = small_button_size * 4.3 + legend_font_size + diff*1.7
    diff = big_button_height + small_button_size*0.5

    action_buttons = {"RUN": BigButton(screen, "RUN", x, y, color=START_COLOR),
                      "FINISH": BigButton(screen, "FINISH", x, y, color=VISITED_COLOR, visible=False),
                      "CLEAR": BigButton(screen, "CLEAR", x, y + diff, color=YELLOW),
                      "RESET": BigButton(screen, "RESET", x, y + diff*2, color=END_COLOR)}

    screen.add_buttons("action_buttons", action_buttons)

    # Initialize gridline buttons
    gridline_buttons = {"GRID OFF": BigButton(screen, "GRID OFF", x, y-diff_grid, color=FREE_COLOR),
                        "GRID ON": BigButton(screen, "GRID ON", x, y-diff_grid, color=BLUE)}

    screen.add_buttons("gridline_buttons", gridline_buttons)
    update_gridline_buttons(screen)

    # Initialize buttons for maze-generating algorithms
    x -= side_size + grid_size
    y += diff * 2
    diff = big_button_height + small_button_size

    maze_buttons = {"Prim's": BigButton(screen, "Prim's", x, y - diff*3, color=LIGHT_GREEN),
                    "Division": BigButton(screen, "Division", x, y - diff*2,  color=LIGHT_GREEN),
                    "Backtrack": BigButton(screen, "Backtrack", x, y - diff, color=LIGHT_GREEN),
                    "Random": BigButton(screen, "Random", x, y,  color=LIGHT_GREEN)}

    screen.add_buttons("maze_buttons", maze_buttons)

    # Initialize buttons for pathfinding algorithms
    pathfinding_buttons = {"BFS": BigButton(screen, "BFS", x, y - diff*7),
                           "DFS": BigButton(screen, "DFS", x, y - diff*6),
                           "Dijkstra's": BigButton(screen, "Dijkstra's", x, y - diff*5),
                           "A*": BigButton(screen, "A*", x, y - diff*4)}

    screen.add_buttons("pathfinding_buttons", pathfinding_buttons)
    update_pathfinding_buttons(screen)
