from parameters import *
import pygame


class BigButton:
    def __init__(self, label, x, y, color=WHITE, width_offset=0, height_offset=0, algorithm=None, visible=True):
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
    def __init__(self, label, x, y, width_offset=0, color=WHITE):
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


def initialize_buttons(graph, animation_speed):
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

    return size_buttons, animation_buttons
