from parameters import *
from screen import *
from graph import *
from pathfinding import *
from buttons import *
from helpers import *
from legend import *

import pygame


def main():
    def draw():
        screen.draw()

        pygame.display.update()

    pygame.init()
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Algorithms Visualizer")

    screen = Screen(WINDOW)
    screen.add_graph(Graph(size=45))
    screen.add_legend(initialize_legend())
    initialize_buttons(screen)

    start, end = None, None
    path = None
    selected_algorithm = None
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        draw()
        wait = False    # For preventing multi-clicks

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = screen.graph.get_grid_pos(pos)
                if 0 <= row < screen.graph.size and 0 <= col < screen.graph.size:
                    # Update the selected node
                    node = screen.graph.grid[row][col]
                    if screen.graph.start is None:
                        node.set_start()
                        screen.graph.set_start(node)
                    elif screen.graph.end is None and not node.is_start():
                        node.set_end()
                        screen.graph.set_end(node)
                    else:
                        node.set_barrier()
                    node.draw(WINDOW, screen.graph.gridlines)
                else:
                    # Run checks on the buttons
                    for label, button in screen.buttons["size_buttons"].items():
                        if button.rect.collidepoint(pos):
                            screen.add_graph(
                                Graph(label, screen.graph.gridlines))
                            update_size_buttons(screen)
                            path = None

                    for label, button in screen.buttons["animation_buttons"].items():
                        if button.rect.collidepoint(pos):
                            screen.set_animation_speed(label)
                            update_animation_buttons(screen)

                    for label, button in screen.buttons["control_buttons"].items():
                        if button.rect.collidepoint(pos):
                            if label == "RUN":
                                if screen.graph.start and screen.graph.end and selected_algorithm and path is None:
                                    # path = search(
                                    #     WINDOW, start, end, graph, selected_algorithm, animation_speed)
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
                                        draw_path(WINDOW, path, screen.graph,
                                                  screen.animation_speed)
                            elif label == "CLEAR":
                                # Clear the graph (keep the barriers)
                                screen.graph.clear()
                                path = None
                            elif label == "RESET":
                                # Reset the graph (create a completely new one)
                                screen.add_graph(
                                    Graph(screen.graph.size, screen.graph.gridlines))
                                path = None
                            elif not wait:
                                # Toggle gridlines
                                update_gridline_buttons(screen, toggle=True)
                                screen.graph.toggle_gridlines()
                                wait = True

                    # Select a pathfinding algorithm
                    for label, button in screen.buttons["pathfinding_buttons"].items():
                        if button.rect.collidepoint(pos):
                            selected_algorithm = label
                            update_pathfinding_buttons(
                                screen, selected_algorithm)

                    # Select and generate a maze
                    for label, button in screen.buttons["maze_buttons"].items():
                        if button.rect.collidepoint(pos) and not wait:
                            screen.graph.clear(save_barriers=False)
                            path = None
                            wait = True
                            # generate_maze(label)

            elif pygame.mouse.get_pressed()[2]:
                row, col = screen.graph.get_grid_pos(pygame.mouse.get_pos())
                # Unselect the selected node
                if 0 <= row < screen.graph.size and 0 <= col < screen.graph.size:
                    node = screen.graph.grid[row][col]
                    if node.is_start():
                        screen.graph.reset_start()
                    elif node.is_end():
                        screen.graph.reset_end()
                    node.set_free()
                    node.draw(WINDOW, screen.graph.gridlines)


if __name__ == "__main__":
    main()
