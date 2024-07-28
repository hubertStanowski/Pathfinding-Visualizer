from constants import *
from helpers import *

import pygame


class Legend:
    def __init__(self) -> None:
        self.nodes = []

    def draw(self, window, graph):
        for node in self.nodes:
            node.draw(window, graph)

    def add_node(self, node):
        self.nodes.append(node)


class LegendNode:
    def __init__(self, label, x, y, color=None, action="") -> None:
        self.label = label
        self.x = x
        self.y = y
        self.color = color
        self.action = action

    def draw(self, window, graph):
        font = pygame.font.SysFont(FONT, get_legend_font_size(window, graph))

        if self.action != "" or self.color is not None:
            label = font.render(self.action + " - " +
                                self.label, True, LEGEND_FONT_COLOR)
        else:
            label = font.render(self.label, True, LEGEND_FONT_COLOR)

        label_width, label_height = label.get_size()

        if self.color is None:
            label_rect = pygame.Rect(self.x, self.y, label_width, label_height)
        else:
            square_size = 3/4 * get_small_button_size(window)
            label_rect = pygame.Rect(
                self.x+square_size, self.y + square_size/7, label_width, square_size)
            pygame.draw.rect(window, self.color,
                             (self.x, self.y, square_size, square_size))
            pygame.draw.rect(window, LINE_COLOR,
                             (self.x, self.y, square_size, square_size), 1)

        window.blit(label, label_rect)


def initialize_legend(screen):
    legend = Legend()

    window, graph = screen.window, screen.graph
    small_button_size = get_small_button_size(window)
    grid_size = get_grid_size(window, graph)
    x = get_side_tab_size(window, graph) * (1.1) + grid_size
    y = get_tb_tab_size(window, graph)
    diff = small_button_size

    legend.add_node(LegendNode("Start node", x, y, START_COLOR))

    y += diff
    legend.add_node(LegendNode("End node", x, y, END_COLOR))

    y += diff
    legend.add_node(LegendNode("Free node", x, y, FREE_COLOR))

    y += diff
    legend.add_node(LegendNode("Barrier node", x, y, BARRIER_COLOR))

    y += diff
    legend.add_node(LegendNode("Visited node", x, y, VISITED_COLOR))

    y += diff
    legend.add_node(LegendNode("Path node", x, y, PATH_COLOR))

    y += diff
    legend.add_node(LegendNode("Select a node", x, y, action="LMB"))

    y += diff * 0.8
    legend.add_node(LegendNode("Unselect a node",  x, y, action="RMB"))

    y += 3.3 * diff
    x += get_side_tab_size(window, graph) * 0.25 - \
        get_legend_font_size(window, graph) * 0.15
    legend.add_node(LegendNode("Graph size", x, y))

    y += 2*diff
    x -= get_legend_font_size(window, graph) * 1.05
    legend.add_node(LegendNode("Animation speed", x, y))

    return legend
