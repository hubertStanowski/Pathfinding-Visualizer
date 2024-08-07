from constants import *
from buttons import initialize_buttons
from legend import initialize_legend
from graph import Graph

import pygame


class Screen:
    def __init__(self, window=None, background=BLACK, animation_speed=NORMAL) -> None:
        self.window = window
        self.background = background
        self.animation_speed = animation_speed
        self.animate = True
        self.buttons = {}
        self.legend = None
        self.graph = None
        self.selected_algorithm = None
        self.delay_multiplier = 1

    def draw(self):
        self.animate = False
        self.window.fill(self.background)

        if self.graph:
            self.graph.draw(self)
            if self.legend:
                self.legend.draw(self.window, self.graph)

        self.draw_buttons()

        self.animate = True
        pygame.display.update()

    def draw_buttons(self):
        if self.buttons:
            for current_buttons in self.buttons.values():
                for button in current_buttons.values():
                    button.draw(self.window)

        pygame.display.update()

    def resize(self, new_window):
        self.window = new_window
        if self.graph:
            self.graph.resize_nodes(new_window)
            if self.legend:
                initialize_legend(self)
            if self.buttons:
                algorithm_running = not self.buttons["action_buttons"]["RUN"].visible
                initialize_buttons(self, algorithm_running)

        self.draw()

    def reset_delay_multiplier(self):
        self.delay_multiplier = 1

    def add_buttons(self, label, buttons):
        self.buttons[label] = buttons

    def update_legend(self, new_legend):
        self.legend = new_legend

    def update_graph_size(self, new_graph_size):
        if new_graph_size != self.graph.size:
            self.graph = Graph(self.window, new_graph_size,
                               self.graph.gridlines)

    def update_animation_speed(self, new_animation_speed):
        self.animation_speed = new_animation_speed


def initialize_screen(window):
    screen = Screen(window, background=BARRIER_COLOR)
    try:
        with open("settings.txt", "r") as file:
            graph_size, gridlines, animation_speed = file.readline().split(" ")
            screen.graph = (Graph(window, size=int(graph_size)))
            screen.graph.gridlines = bool(int(gridlines))
            screen.animation_speed = animation_speed
    except FileNotFoundError:
        screen.graph.gridlines = False
        screen.graph = (Graph(window, size=MEDIUM))
        screen.animation_speed = NORMAL

    initialize_buttons(screen)
    initialize_legend(screen)

    return screen
