from parameters import *

import pygame


class Legend:
    def __init__(self) -> None:
        self.nodes = []

    def draw(self, window):
        for node in self.nodes:
            node.draw(window)

    def add_node(self, node):
        self.nodes.append(node)


class LegendNode:
    def __init__(self, label, x, y, color=None, action="") -> None:
        self.label = label
        self.x = x
        self.y = y
        self.color = color
        self.action = action

    def draw(self, window):
        font = pygame.font.SysFont(FONT, 32)
        if self.action != "" or self.color is not None:
            label = font.render(self.action + " - " + self.label, True, WHITE)
        else:
            label = font.render(self.label, True, WHITE)

        label_rect = pygame.Rect(self.x + 30, self.y, 100, 50)
        if self.action != "":
            label_rect = pygame.Rect(self.x, self.y, 100, 50)

        if self.color:
            pygame.draw.rect(window, self.color, (self.x, self.y, 30, 30))
            pygame.draw.rect(window, LINE_COLOR, (self.x, self.y, 30, 30), 1)

        window.blit(label, label_rect)
