from constants import *
from helpers import *
from screen import initialize_screen

import pygame


def main():
    pygame.init()
    display_info = pygame.display.Info()
    window = pygame.display.set_mode(
        (display_info.current_w, display_info.current_h), pygame.RESIZABLE)
    pygame.display.set_caption("Pathfinding Visualizer")

    screen = initialize_screen(window)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        screen.draw()
        old_width, old_height = screen.window.get_size()
        graph = screen.graph

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(screen)
                return

            if event.type == pygame.VIDEORESIZE:
                new_width, new_height = get_updated_screen_dimensions(
                    (old_width, old_height), (event.w, event.h))
                new_window = pygame.display.set_mode(
                    (new_width, new_height), pygame.RESIZABLE)
                screen.resize(new_window)

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = graph.get_grid_pos(window, pos)
                if graph.is_valid_node(row, col):
                    node = graph.grid[row][col]
                    graph.select_node(node)
                    node.draw(screen)
                else:
                    for label, button in screen.buttons["size_buttons"].items():
                        if button.clicked(pos):
                            screen.update_graph_size(label)
                            update_size_buttons(screen)

                    for label, button in screen.buttons["animation_buttons"].items():
                        if button.clicked(pos):
                            screen.update_animation_speed(label)
                            update_animation_buttons(screen)

                    for label, button in screen.buttons["action_buttons"].items():
                        if button.clicked(pos):
                            if label == "RUN":
                                if graph.start and graph.end and screen.selected_algorithm:
                                    toggle_run_finish_buttons(screen)
                                    path = graph.search(screen)
                                    screen.animate = True
                                    if path:
                                        draw_path(screen, path)
                                    else:
                                        handle_no_path(screen)
                                    toggle_run_finish_buttons(screen)

                            elif label == "CLEAR":
                                graph.clear()
                            elif label == "RESET":
                                screen.graph.reset()

                    for button in screen.buttons["gridline_buttons"].values():
                        if button.clicked(pos):
                            toggle_gridline_buttons(screen)
                            graph.toggle_gridlines()

                    for label, button in screen.buttons["pathfinding_buttons"].items():
                        if button.clicked(pos):
                            screen.selected_algorithm = label
                            update_pathfinding_buttons(screen)

                    for label, button in screen.buttons["maze_buttons"].items():
                        if button.clicked(pos):
                            toggle_run_finish_buttons(screen)
                            graph.generate_maze(screen, label)
                            toggle_run_finish_buttons(screen)

            elif pygame.mouse.get_pressed()[2]:
                row, col = graph.get_grid_pos(window, pygame.mouse.get_pos())
                if graph.is_valid_node(row, col):
                    node = graph.grid[row][col]
                    graph.unselect_node(node)
                    node.draw(screen)


if __name__ == "__main__":
    main()
