from parameters import *
import pygame


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
