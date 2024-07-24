from constants import *
from screen import *
from graph import *
from helpers import *
from buttons import *
from legend import initialize_legend

import pygame


def main():
    pygame.init()
    window = pygame.display.set_mode(
        (1500, 1000), pygame.RESIZABLE)
    pygame.display.set_caption("Pathfinding Algorithms Visualizer")

    screen = Screen(window)
    screen.set_graph(Graph(window, size=45))
    screen.set_legend(initialize_legend(screen))
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
            if event.type == pygame.QUIT:
                return 0

            if event.type == pygame.VIDEORESIZE:
                new_width, new_height = max(event.w, 850), max(event.h, 500)
                ratio = new_height/new_width
                if not (0.50 <= ratio <= 0.75):
                    new_width = max(new_width, new_height)
                    new_height = new_width * 2/3

                window = pygame.display.set_mode(
                    (new_width, new_height), pygame.RESIZABLE)
                screen.resize_window(window)

                #! TESTING
                print("RATIO ", new_height/new_width)
                print("WINDOW ", window.get_size())
                print("GRID ", get_grid_size(window, graph))
                print("TB ", get_tb_tab_size(window, graph))
                print("SIDE ", get_side_tab_size(window, graph))
                print("SMALL BUTTON ", get_small_button_size(window, graph))
                #! TESTING

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = graph.get_grid_pos(window, pos)
                if graph.is_valid_node(row, col):
                    node = graph.grid[row][col]
                    graph.select_node(node)
                    node.draw(window, graph)
                else:
                    for label, button in screen.buttons["size_buttons"].items():
                        if button.rect.collidepoint(pos):
                            screen.set_graph(
                                Graph(window, label, graph.gridlines))
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
                                    Graph(window, graph.size, graph.gridlines))
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
                row, col = graph.get_grid_pos(window, pygame.mouse.get_pos())
                if graph.is_valid_node(row, col):
                    node = graph.grid[row][col]
                    graph.unselect_node(node)
                    node.draw(window, graph)


if __name__ == "__main__":
    main()
