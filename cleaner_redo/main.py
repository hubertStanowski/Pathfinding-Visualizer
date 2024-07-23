from parameters import *
from screen import *
from graph import *
from helpers import *

import pygame


def main():
    pygame.init()
    window = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Pathfinding Algorithms Visualizer")

    screen = Screen(window)
    screen.set_graph(Graph(size=45))
    screen.set_legend(initialize_legend())
    initialize_buttons(screen)

    path = None
    selected_algorithm = None
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        screen.draw()
        graph = screen.graph
        wait = False    # For preventing multi-clicks

        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                window = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE)
                screen.window = window
            if event.type == pygame.QUIT:
                return 0

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = graph.get_grid_pos(pos)
                if graph.is_valid_node(row, col):
                    node = graph.grid[row][col]
                    graph.select_node(node)
                    node.draw(window, graph.gridlines)
                else:
                    for label, button in screen.buttons["size_buttons"].items():
                        if button.rect.collidepoint(pos):
                            screen.set_graph(
                                Graph(label, graph.gridlines))
                            update_size_buttons(screen)
                            path = None

                    for label, button in screen.buttons["animation_buttons"].items():
                        if button.rect.collidepoint(pos):
                            screen.set_animation_speed(label)
                            update_animation_buttons(screen)

                    for label, button in screen.buttons["control_buttons"].items():
                        if button.rect.collidepoint(pos):
                            if label == "RUN":
                                if graph.start and graph.end and selected_algorithm and not path:
                                    path = graph.search(
                                        screen, selected_algorithm)
                                    if path:
                                        draw_path(screen, path)
                                    else:
                                        handle_no_path(screen)
                            elif label == "CLEAR":
                                graph.clear()
                                path = None
                            elif label == "RESET":
                                screen.set_graph(
                                    Graph(graph.size, graph.gridlines))
                                path = None
                            elif not wait:
                                update_gridline_buttons(screen, toggle=True)
                                graph.toggle_gridlines()
                                wait = True

                    for label, button in screen.buttons["pathfinding_buttons"].items():
                        if button.rect.collidepoint(pos):
                            selected_algorithm = label
                            update_pathfinding_buttons(
                                screen, selected_algorithm)

                    for label, button in screen.buttons["maze_buttons"].items():
                        if button.rect.collidepoint(pos) and not wait:
                            graph.clear(save_barriers=False)
                            path = None
                            wait = True
                            # generate_maze(label)

            elif pygame.mouse.get_pressed()[2]:
                row, col = graph.get_grid_pos(pygame.mouse.get_pos())
                if graph.is_valid_node(row, col):
                    node = graph.grid[row][col]
                    graph.unselect_node(node)
                    node.draw(window, graph.gridlines)


if __name__ == "__main__":
    main()
