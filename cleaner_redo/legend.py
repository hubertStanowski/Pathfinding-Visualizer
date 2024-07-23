from parameters import *
from helpers import *

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


def initialize_legend(screen):
    legend = Legend()
    x = get_side_tab_size(screen.window, screen.graph) + \
        get_grid_size(screen.window, screen.graph) + 30
    y = get_tb_tab_size(screen.window, screen.graph) + 8
    diff = 50

    legend.add_node(LegendNode("Start node", x, y, START_COLOR))
    legend.add_node(LegendNode("End node", x, y+diff, END_COLOR))
    legend.add_node(LegendNode("Free node", x, y+diff*2, FREE_COLOR))
    legend.add_node(LegendNode("Barrier node", x, y+diff*3, BARRIER_COLOR))
    legend.add_node(LegendNode("Visited node", x, y+diff*4, VISITED_COLOR))
    legend.add_node(LegendNode("Path node", x, y+diff*5, PATH_COLOR))
    legend.add_node(LegendNode("Select a node", x,
                    y + diff*5+40, action="LMB"))
    legend.add_node(LegendNode("Unselect a node",  x,
                               y+diff*6+20, action="RMB"))
    legend.add_node(LegendNode("Graph size", x+33, y+diff*8+10))
    legend.add_node(LegendNode("Animation speed", x, y+diff*9+38))

    return legend
