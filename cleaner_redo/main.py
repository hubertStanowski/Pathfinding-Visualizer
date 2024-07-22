from parameters import *
from graph import *
from buttons import *
from legend import *
import pygame

# from collections import deque
# from math import floor, inf, sqrt
# from heapq import heappop, heappush
# from queue import PriorityQueue
# from random import randrange, choice, shuffle


def main():
    def draw(buttons=[]):
        WINDOW.fill(BARRIER_COLOR)
        graph.draw(WINDOW, update=False)
        draw_legend(WINDOW)

        for button in size_buttons.values():
            button.draw(WINDOW)

        for button in animation_buttons.values():
            button.draw(WINDOW)

        for button in control_buttons.values():
            button.draw(WINDOW)

        for button in pathfinding_buttons.values():
            button.draw(WINDOW)

        pygame.display.update()

    pygame.init()
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Algorithms Visualizer")

    animation_speed = "N"
    graph = Graph(45, True)

    pathfinding_buttons, control_buttons, size_buttons, animation_buttons = initialize_buttons(
        graph, animation_speed, graph.gridlines)

    start, end = None, None
    path = None
    selected_algorithm = None
    clock = pygame.time.Clock()

    while True:
        draw()
        clock.tick(60)
        wait = False    # For preventing multi-clicks

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = graph.get_grid_pos(pos)
                if 0 <= row < graph.size and 0 <= col < graph.size:
                    # Update the selected node
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
                else:
                    # Run checks on the buttons
                    for label, button in size_buttons.items():
                        if button.rect.collidepoint(pos):
                            graph = Graph(label, graph.gridlines)
                            update_size_buttons(graph, size_buttons)
                            start, end = None, None
                            path = None
                    for label, button in animation_buttons.items():
                        if button.rect.collidepoint(pos):
                            animation_speed = label
                            update_animation_buttons(
                                animation_speed, animation_buttons)
                    for label, button in control_buttons.items():
                        if button.rect.collidepoint(pos):
                            if label == "RUN":
                                if start and end and selected_algorithm and path is None:
                                    # path = search(start, end, selected_algorithm)
                                    if not path:
                                        # Inform that no path has been found
                                        font = pygame.font.SysFont(FONT, 120)
                                        label = font.render(
                                            "PATH NOT FOUND!", True, RED)
                                        text_rect = label.get_rect(
                                            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                                        WINDOW.blit(label, text_rect)
                                        pygame.display.update()
                                        pygame.time.delay(500)
                                        path = None
                                        print("PATH NOT FOUND")
                                    else:
                                        draw_path(path)
                            elif label == "CLEAR":
                                # Clear the graph (keep the barriers)
                                graph.clear()
                                path = None
                            elif label == "RESET":
                                # Reset the graph (create a completely new one)
                                graph = Graph(graph.size, graph.gridlines)
                                start, end = None, None
                                path = None
                            elif not wait:
                                update_gridline_buttons(
                                    graph.gridlines, control_buttons, toggle=True)
                                graph.toggle_gridlines()
                                wait = True

                    # Select a pathfinding algorithm
                    for label, button in pathfinding_buttons.items():
                        if button.rect.collidepoint(pos):
                            selected_algorithm = label
                            update_pathfinding_buttons(
                                label, pathfinding_buttons)

            elif pygame.mouse.get_pressed()[2]:
                row, col = graph.get_grid_pos(pygame.mouse.get_pos())
                # Unselect the selected node
                if 0 <= row < graph.size and 0 <= col < graph.size:
                    node = graph.grid[row][col]
                    if node.is_start():
                        start = None
                    elif node.is_end():
                        end = None
                    node.set_free()
                    node.draw(WINDOW, graph.gridlines)


# Helper function for handling events within algorithms
def run_checks():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise Exception(
                "Exiting the program while executing an algorithm! (current settings will not be saved)")


# Draw the path between start and end
def draw_path(path, graph, animation_speed):
    length = len(path)
    prev = path[0]
    for node in path[1:]:
        run_checks()
        if not prev.is_start():
            prev.color = PATH_COLOR
            prev.draw(update=True)
        if not node.is_start() and not node.is_end():
            node.color = YELLOW
            node.draw(update=True)
            prev = node
        # Delay based on length relative to GRAPH_SIZE and base delay
        delay = round(4 * graph.size / length * 6 *
                      DELAYS[animation_speed][graph.size])
        if delay > 80:
            delay = 80
        pygame.time.delay(delay)


if __name__ == "__main__":
    main()
