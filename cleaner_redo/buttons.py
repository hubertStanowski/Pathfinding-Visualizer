from parameters import *
from screen import *
import pygame


class BigButton:
    def __init__(self, label, x, y, color=FREE_COLOR, width_offset=0, height_offset=0, visible=True):
        self.label = label
        self.x = x
        self.y = y
        self.width_offset = width_offset
        self.height_offset = height_offset
        self.rect = pygame.Rect(
            x, y, BUTTON_WIDTH, BUTTON_HEIGHT-height_offset)
        self.color = color
        self.visible = visible

    def draw(self, window):
        if not self.visible:
            return

        pygame.draw.rect(window, self.color, self.rect)
        current_font = pygame.font.SysFont(FONT, 60)
        label = current_font.render(self.label, True, BLACK)
        text_rect = label.get_rect(center=(
            self.x + BUTTON_WIDTH // 2, self.y + (BUTTON_HEIGHT - self.height_offset) // 2))
        window.blit(label, text_rect)


# default scale x + 5
class SmallButton:
    def __init__(self, label, x, y, color=FREE_COLOR):
        self.label = label
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        current_font = pygame.font.SysFont(FONT, 45)
        label = current_font.render(self.label, True, BLACK)
        text_rect = label.get_rect(center=(
            self.x + SMALL_BUTTON_SIZE // 2, self.y + (SMALL_BUTTON_SIZE) // 2))
        window.blit(label, text_rect)

    def select(self):
        self.color = PATH_COLOR

    def unselect(self):
        self.color = FREE_COLOR


def initialize_buttons(screen):
    # Initialize buttons for changing graph size
    diff = 60
    size_buttons = {25: SmallButton("S", SIDE_SIZE + GRAPH_WIDTH + 70, TB_SIZE + 445),
                    45: SmallButton("M", SIDE_SIZE + GRAPH_WIDTH + 70 + diff,
                                    TB_SIZE + 445),
                    75: SmallButton("L", SIDE_SIZE + GRAPH_WIDTH + 70 + diff*2, TB_SIZE + 445)}

    screen.add_buttons("size_buttons", size_buttons)
    update_size_buttons(screen)

    # Initialize buttons for changing animation speed
    animation_buttons = {"S": SmallButton("S", SIDE_SIZE + GRAPH_WIDTH + 70, TB_SIZE + 523),
                         "N": SmallButton("N", SIDE_SIZE + GRAPH_WIDTH + 70 + diff,
                                          TB_SIZE + 523),
                         "F": SmallButton("F", SIDE_SIZE + GRAPH_WIDTH + 70 + diff*2, TB_SIZE + 523)}

    screen.add_buttons("animation_buttons", animation_buttons)
    update_animation_buttons(screen)

    # Initialize buttons for graph management and view
    diff = 115
    control_buttons = {"GRID OFF": BigButton("GRID OFF", WINDOW_WIDTH -
                                             (BUTTON_WIDTH + 50), TB_SIZE + 360, width_offset=-59, height_offset=20, color=FREE_COLOR),
                       "GRID ON": BigButton("GRID ON", WINDOW_WIDTH -
                                            (BUTTON_WIDTH + 50), TB_SIZE + 360, width_offset=-49, height_offset=20, color=BLUE),
                       "RUN": BigButton("RUN", WINDOW_WIDTH -
                                        (BUTTON_WIDTH + 50), TB_SIZE + 10 + diff*5, width_offset=-2, color=START_COLOR),
                       "CLEAR": BigButton("CLEAR", WINDOW_WIDTH -
                                          (BUTTON_WIDTH + 50), TB_SIZE + 10 + diff*6, width_offset=-31, color=YELLOW),
                       "RESET": BigButton("RESET", WINDOW_WIDTH -
                                          (BUTTON_WIDTH + 50), TB_SIZE + 10 + diff*7, width_offset=-24, color=END_COLOR)}

    screen.add_buttons("control_buttons", control_buttons)
    update_gridline_buttons(screen)

    # Initialize buttons for pathfinding algorithms
    pathfinding_buttons = {"BFS": BigButton("BFS", 50, TB_SIZE + 10),
                           "DFS": BigButton("DFS", 50, TB_SIZE +
                                            10 + diff),
                           "Dijkstra's": BigButton("Dijkstra's", 50,
                                                   TB_SIZE + 10 + diff*2, width_offset=-51),
                           "A*": BigButton("A*", 50, TB_SIZE + 10 + diff*3, width_offset=20)}

    screen.add_buttons("pathfinding_buttons", pathfinding_buttons)

    # Initialize buttons for maze-generating algorithms
    maze_buttons = {"Prim's": BigButton("Prim's", 50, TB_SIZE + 10 + diff*4,
                                        width_offset=-20, color=LIGHT_GREEN),
                    "Division": BigButton("Division", 50,
                                          TB_SIZE + 10 + diff*5, width_offset=-43, color=LIGHT_GREEN),
                    "Backtrack": BigButton("Backtrack", 50, TB_SIZE + 10 + diff*6,
                                           width_offset=-60, color=LIGHT_GREEN),
                    "Random": BigButton("Random", 50, TB_SIZE + 10 +
                                        diff*7, width_offset=-43, color=LIGHT_GREEN)}

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
