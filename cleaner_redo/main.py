from parameters import *
from graph import *
import pygame

# from collections import deque
# from math import floor, inf, sqrt
# from heapq import heappop, heappush
# from queue import PriorityQueue
# from random import randrange, choice, shuffle


def main():
    def draw():
        WINDOW.fill(BARRIER_COLOR)
        graph.draw(WINDOW, update=False)
        draw_legend(WINDOW)
        pygame.display.update()

    pygame.init()
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Algorithms Visualizer")

    graph = Graph(GRAPH_SIZE, gridlines=True)
    start, end = None, None
    pathfinding_done = False
    selected_algorithm = None
    clock = pygame.time.Clock()

    while True:
        draw()
        clock.tick(60)

        # For preventing multi-clicks
        wait = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if pygame.mouse.get_pressed()[0]:
                row, col = graph.get_grid_pos(pygame.mouse.get_pos())
                # Update the selected node
                if 0 <= row < GRAPH_SIZE and 0 <= col < GRAPH_SIZE:
                    node = graph.grid[row][col]
                    if start is None:
                        node.set_start()
                        start = node
                    elif end is None and not node.is_start():
                        node.set_end()
                        end = node
                    else:
                        node.set_barrier()
                    node.draw(WINDOW, graph.gridlines)

            elif pygame.mouse.get_pressed()[2]:
                row, col = graph.get_grid_pos(pygame.mouse.get_pos())
                # Unselect the selected node
                if 0 <= row < GRAPH_SIZE and 0 <= col < GRAPH_SIZE:
                    node = graph.grid[row][col]
                    if node.is_start():
                        start = None
                    elif node.is_end():
                        end = None
                    node.set_free()
                    node.draw(WINDOW, graph.gridlines)


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
    draw_legend_node(window, "Graph size", x+44, y+whitespace*8+10)
    draw_legend_node(window, "Animation speed", x, y+whitespace*9+38)


# Helper function for draw_legend
def draw_legend_node(window, text,  x, y, color=None, action=""):

    current_font = pygame.font.SysFont(font, 32)

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


if __name__ == "__main__":
    main()
