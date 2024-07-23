from pathfinding import *
from parameters import *
from legend import *
from buttons import *


import pygame


# Helper function for handling events within algorithms
def run_checks():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise Exception(
                "Exiting the program while executing an algorithm! (current settings will not be saved)")


def initialize_legend():
    legend = Legend()
    x, y = SIDE_SIZE + GRAPH_WIDTH + 30, TB_SIZE + 8
    diff = 50

    legend.add_node(LegendNode("Start node", x, y, START_COLOR))
    legend.add_node(LegendNode("End node", x, y+diff, END_COLOR))
    legend.add_node(LegendNode("Free node", x, y+diff*2, FREE_COLOR))
    legend.add_node(LegendNode("Barrier node", x, y+diff*3, BARRIER_COLOR))
    legend.add_node(LegendNode("Visited node", x, y+diff*4, VISITED_COLOR))
    legend.add_node(LegendNode("Path node", x, y+diff*5, PATH_COLOR))
    legend.add_node(LegendNode("Select a node", x,
                    y + diff*5+40, action="LMB"))
    legend.add_node(LegendNode("Unselect a node",  x,
                               y+diff*6+20, action="RMB"))
    legend.add_node(LegendNode("Graph size", x+33, y+diff*8+10))
    legend.add_node(LegendNode("Animation speed", x, y+diff*9+38))

    return legend


def initialize_buttons(screen):
    # Initialize buttons for changing graph size
    diff = 60
    size_buttons = {25: SmallButton("S", SIDE_SIZE + GRAPH_WIDTH + 70, TB_SIZE + 445, width_offset=-1),
                    45: SmallButton("M", SIDE_SIZE + GRAPH_WIDTH + 70 + diff,
                                    TB_SIZE + 445, width_offset=-4),
                    75: SmallButton("L", SIDE_SIZE + GRAPH_WIDTH + 70 + diff*2, TB_SIZE + 445)}

    screen.add_buttons("size_buttons", size_buttons)
    update_size_buttons(screen)

    # Initialize buttons for changing animation speed
    animation_buttons = {"S": SmallButton("S", SIDE_SIZE + GRAPH_WIDTH + 70, TB_SIZE + 523, width_offset=-1, ),
                         "N": SmallButton("N", SIDE_SIZE + GRAPH_WIDTH + 70 + diff,
                                          TB_SIZE + 523, width_offset=-2),
                         "F": SmallButton("F", SIDE_SIZE + GRAPH_WIDTH + 70 + diff*2, TB_SIZE + 523)}

    screen.add_buttons("animation_buttons", animation_buttons)
    update_animation_buttons(screen)

    # Initialize buttons for graph management and view
    diff = 115
    control_buttons = {"GRID OFF": BigButton("GRID OFF", WINDOW_WIDTH -
                                             (BUTTON_WIDTH + 50), TB_SIZE + 360, width_offset=-59, height_offset=20, color=FREE_COLOR),
                       "GRID ON": BigButton("GRID ON", WINDOW_WIDTH -
                                            (BUTTON_WIDTH + 50), TB_SIZE + 360, width_offset=-49, height_offset=20, color=BLUE),
                       "RUN": BigButton("RUN", WINDOW_WIDTH -
                                        (BUTTON_WIDTH + 50), TB_SIZE + 10 + diff*5, width_offset=-2, color=START_COLOR),
                       "CLEAR": BigButton("CLEAR", WINDOW_WIDTH -
                                          (BUTTON_WIDTH + 50), TB_SIZE + 10 + diff*6, width_offset=-31, color=YELLOW),
                       "RESET": BigButton("RESET", WINDOW_WIDTH -
                                          (BUTTON_WIDTH + 50), TB_SIZE + 10 + diff*7, width_offset=-24, color=END_COLOR)}

    screen.add_buttons("control_buttons", control_buttons)
    update_gridline_buttons(screen)

    # Initialize buttons for pathfinding algorithms
    pathfinding_buttons = {"BFS": BigButton("BFS", 50, TB_SIZE + 10),
                           "DFS": BigButton("DFS", 50, TB_SIZE +
                                            10 + diff),
                           "Dijkstra's": BigButton("Dijkstra's", 50,
                                                   TB_SIZE + 10 + diff*2, width_offset=-51),
                           "A*": BigButton("A*", 50, TB_SIZE + 10 + diff*3, width_offset=20)}

    screen.add_buttons("pathfinding_buttons", pathfinding_buttons)

    # Initialize buttons for maze-generating algorithms
    maze_buttons = {"Prim's": BigButton("Prim's", 50, TB_SIZE + 10 + diff*4,
                                        width_offset=-20, color=LIGHT_GREEN),
                    "Division": BigButton("Division", 50,
                                          TB_SIZE + 10 + diff*5, width_offset=-43, color=LIGHT_GREEN),
                    "Backtrack": BigButton("Backtrack", 50, TB_SIZE + 10 + diff*6,
                                           width_offset=-60, color=LIGHT_GREEN),
                    "Random": BigButton("Random", 50, TB_SIZE + 10 +
                                        diff*7, width_offset=-43, color=LIGHT_GREEN)}

    screen.add_buttons("maze_buttons", maze_buttons)


def update_size_buttons(screen):
    for label, button in screen.buttons["size_buttons"].items():
        if screen.graph.size == label:
            button.select()
        else:
            button.unselect()


def update_animation_buttons(screen):
    for label, button in screen.buttons["animation_buttons"].items():
        if label == screen.animation_speed:
            button.select()
        else:
            button.unselect()


def update_gridline_buttons(screen, toggle=False):
    grid_on = screen.buttons["control_buttons"]["GRID ON"]
    grid_off = screen.buttons["control_buttons"]["GRID OFF"]
    if screen.graph.gridlines:
        grid_on.visible = True
        grid_off.visible = False
    else:
        grid_on.visible = False
        grid_off.visible = True

    if toggle:
        grid_on.visible = not grid_on.visible
        grid_off.visible = not grid_off.visible


def update_pathfinding_buttons(screen, selected):
    for label, button in screen.buttons["pathfinding_buttons"].items():
        if label != selected:
            button.color = FREE_COLOR
        else:
            button.color = PATH_COLOR


# Draw the path between start and end
def draw_path(screen, path):
    graph = screen.graph
    prev = path[0]
    for node in path[1:]:
        run_checks()
        if not prev.is_start():
            prev.color = PATH_COLOR
            prev.draw(screen.window, graph.gridlines, update=True)
        if not node.is_start() and not node.is_end():
            node.color = YELLOW
            node.draw(screen.window, graph.gridlines, update=True)
            prev = node
        # Delay based on length relative to GRAPH_SIZE and base delay
        delay = round(4 * graph.size / len(path) * 6 *
                      DELAYS[screen.animation_speed][graph.size])
        if delay > 80:
            delay = 80
        pygame.time.delay(delay)


# Inform that no path has been found
def handle_no_path(screen):
    font = pygame.font.SysFont(FONT, 120)
    label = font.render(
        "PATH NOT FOUND!", True, RED)
    label_rect = label.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    screen.window.blit(label, label_rect)
    pygame.display.update()
    pygame.time.delay(500)
