from constants import *
from screen import *
from graph import *
from helpers import *
from buttons import *
from legend import initialize_legend

import pygame


def main():
    pygame.init()
    display_info = pygame.display.Info()
    window = pygame.display.set_mode(
        (display_info.current_w, display_info.current_h), pygame.RESIZABLE)
    pygame.display.set_caption("Pathfinding Visualizer")

    screen = Screen(window)
    screen.set_graph(Graph(window, size=45))
    screen.set_legend(initialize_legend(screen))
    initialize_buttons(screen)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        screen.draw()
        graph = screen.graph
        old_width, old_height = screen.window.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if event.type == pygame.VIDEORESIZE:
                new_width, new_height = get_updated_screen_dimensions(
                    (old_width, old_height), (event.w, event.h))
                window = pygame.display.set_mode(
                    (new_width, new_height), pygame.RESIZABLE)
                screen.resize_window(window)

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

                    for label, button in screen.buttons["animation_buttons"].items():
                        if button.rect.collidepoint(pos):
                            screen.set_animation_speed(label)
                            update_animation_buttons(screen)

                    for label, button in screen.buttons["action_buttons"].items():
                        if button.rect.collidepoint(pos):
                            if label == "RUN":
                                if graph.start and graph.end and screen.selected_algorithm:
                                    graph.clear()
                                    toggle_run_finish_buttons(screen)
                                    screen.draw()
                                    path = graph.search(screen)
                                    toggle_run_finish_buttons(screen)
                                    screen.draw()
                                    if path:
                                        draw_path(screen, path)
                                    else:
                                        handle_no_path(screen)
                            elif label == "CLEAR":
                                graph.clear()
                            elif label == "RESET":
                                screen.set_graph(
                                    Graph(window, graph.size, graph.gridlines))

                    for button in screen.buttons["gridline_buttons"].values():
                        if button.rect.collidepoint(pos):
                            update_gridline_buttons(screen, toggle=True)
                            graph.toggle_gridlines()
                            break

                    for label, button in screen.buttons["pathfinding_buttons"].items():
                        if button.rect.collidepoint(pos):
                            screen.selected_algorithm = label
                            update_pathfinding_buttons(screen)

                    for label, button in screen.buttons["maze_buttons"].items():
                        if button.rect.collidepoint(pos):
                            graph.clear(save_barriers=False)
                            # generate_maze(label)
                            break

            elif pygame.mouse.get_pressed()[2]:
                row, col = graph.get_grid_pos(window, pygame.mouse.get_pos())
                if graph.is_valid_node(row, col):
                    node = graph.grid[row][col]
                    graph.unselect_node(node)
                    node.draw(window, graph)


if __name__ == "__main__":
    main()
