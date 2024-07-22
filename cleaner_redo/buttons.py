from parameters import *
import pygame


class BigButton:
    def __init__(self, label, x, y, color=FREE_COLOR, width_offset=0, height_offset=0, algorithm=None, visible=True):
        self.algorithm = algorithm
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
        text_rect = pygame.Rect(
            self.x + 60 + self.width_offset, self.y + 16 - self.height_offset // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        window.blit(label, text_rect)


class SmallButton:
    def __init__(self, label, x, y, width_offset=0, color=FREE_COLOR):
        self.label = label
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.width_offset = width_offset

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        current_font = pygame.font.SysFont(FONT, 45)
        label = current_font.render(self.label, True, BLACK)
        text_rect = pygame.Rect(
            self.x + 11 + self.width_offset, self.y + 7, 40, 40)
        window.blit(label, text_rect)

    def select(self):
        self.color = PATH_COLOR

    def unselect(self):
        self.color = FREE_COLOR


def update_size_buttons(graph, size_buttons):
    for label, button in size_buttons.items():
        if graph.size == label:
            button.select()
        else:
            button.unselect()


def update_animation_buttons(animation_speed, animation_buttons):
    for label, button in animation_buttons.items():
        if label == animation_speed:
            button.select()
        else:
            button.unselect()


def toggle_gridline_buttons(control_buttons):
    control_buttons["GRID ON"].visible = not control_buttons["GRID ON"].visible
    control_buttons["GRID OFF"].visible = not control_buttons["GRID OFF"].visible


def update_gridline_buttons(gridlines, control_buttons):
    if gridlines:
        control_buttons["GRID ON"].visible = True
        control_buttons["GRID OFF"].visible = False
    else:
        control_buttons["GRID ON"].visible = False
        control_buttons["GRID OFF"].visible = True


def initialize_buttons(graph, animation_speed, gridlines):
    # Initialize buttons for changing graph size
    diff = 60
    size_buttons = {25: SmallButton("S", SIDE_SIZE + GRAPH_WIDTH + 70, TB_SIZE + 445, width_offset=-1),
                    45: SmallButton("M", SIDE_SIZE + GRAPH_WIDTH + 70 + diff,
                                    TB_SIZE + 445, width_offset=-4),
                    75: SmallButton("L", SIDE_SIZE + GRAPH_WIDTH + 70 + diff*2, TB_SIZE + 445)}

    update_size_buttons(graph, size_buttons)

    # Initialize buttons for changing animation speed
    animation_buttons = {"S": SmallButton("S", SIDE_SIZE + GRAPH_WIDTH + 70, TB_SIZE + 523, width_offset=-1, ),
                         "N": SmallButton("N", SIDE_SIZE + GRAPH_WIDTH + 70 + diff,
                                          TB_SIZE + 523, width_offset=-2),
                         "F": SmallButton("F", SIDE_SIZE + GRAPH_WIDTH + 70 + diff*2, TB_SIZE + 523)}

    update_animation_buttons(animation_speed, animation_buttons)

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

    update_gridline_buttons(gridlines, control_buttons)

    return control_buttons, size_buttons, animation_buttons
