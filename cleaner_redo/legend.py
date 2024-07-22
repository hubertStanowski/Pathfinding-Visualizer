from parameters import *
import pygame


# Draws the information legend
def draw_legend(window):
    x, y = SIDE_SIZE + GRAPH_WIDTH + 30, TB_SIZE + 8
    whitespace = 50
    draw_legend_node(window, "Start node", x, y, START_COLOR)
    draw_legend_node(window, "End node", x, y+whitespace, END_COLOR)
    draw_legend_node(window, "Free node", x, y+whitespace*2, FREE_COLOR)
    draw_legend_node(window, "Barrier node", x, y+whitespace*3, BARRIER_COLOR)
    draw_legend_node(window, "Visited node", x, y+whitespace*4, VISITED_COLOR)
    draw_legend_node(window, "Path node", x, y+whitespace*5, PATH_COLOR)
    draw_legend_node(window, "Select a node", x, y +
                     whitespace*5+40, action="LMB")
    draw_legend_node(window, "Unselect a node",  x,
                     y+whitespace*6+20, action="RMB")
    draw_legend_node(window, "Graph size", x+33, y+whitespace*8+10)
    draw_legend_node(window, "Animation speed", x, y+whitespace*9+38)


# Helper function for draw_legend
def draw_legend_node(window, text,  x, y, color=None, action=""):

    current_font = pygame.font.SysFont(FONT, 32)

    if action != "" or color is not None:
        label = current_font.render(action + " - " + text, True, WHITE)
    else:
        label = current_font.render(text, True, WHITE)

    text_rect = pygame.Rect(x + 30, y, 100, 50)
    if action != "":
        text_rect = pygame.Rect(x, y, 100, 50)

    if color:
        pygame.draw.rect(window, color, (x, y, 30, 30))
        pygame.draw.rect(window, LINE_COLOR, (x, y, 30, 30), 1)

    window.blit(label, text_rect)
