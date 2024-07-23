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


# Draws the information legend
# def draw_legend(window):
#     x, y = SIDE_SIZE + GRAPH_WIDTH + 30, TB_SIZE + 8
#     diff = 50
#     draw_legend_node(window, "Start node", x, y, START_COLOR)
#     draw_legend_node(window, "End node", x, y+diff, END_COLOR)
#     draw_legend_node(window, "Free node", x, y+diff*2, FREE_COLOR)
#     draw_legend_node(window, "Barrier node", x, y+diff*3, BARRIER_COLOR)
#     draw_legend_node(window, "Visited node", x, y+diff*4, VISITED_COLOR)
#     draw_legend_node(window, "Path node", x, y+diff*5, PATH_COLOR)
#     draw_legend_node(window, "Select a node", x, y +
#                      diff*5+40, action="LMB")
#     draw_legend_node(window, "Unselect a node",  x,
#                      y+diff*6+20, action="RMB")
#     draw_legend_node(window, "Graph size", x+33, y+diff*8+10)
#     draw_legend_node(window, "Animation speed", x, y+diff*9+38)


# # Helper function for draw_legend
# def draw_legend_node(window, text,  x, y, color=None, action=""):

#     current_font = pygame.font.SysFont(FONT, 32)

#     if action != "" or color is not None:
#         label = current_font.render(action + " - " + text, True, WHITE)
#     else:
#         label = current_font.render(text, True, WHITE)

#     text_rect = pygame.Rect(x + 30, y, 100, 50)
#     if action != "":
#         text_rect = pygame.Rect(x, y, 100, 50)

#     if color:
#         pygame.draw.rect(window, color, (x, y, 30, 30))
#         pygame.draw.rect(window, LINE_COLOR, (x, y, 30, 30), 1)

#     window.blit(label, text_rect)
