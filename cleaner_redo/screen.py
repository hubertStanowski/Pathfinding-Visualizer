import pygame


class Screen:
    def __init__(self, window=None, background=(0, 0, 0), animation_speed="N") -> None:
        self.window = window
        self.background = background
        self.animation_speed = animation_speed
        self.buttons = {}
        self.legend = None
        self.graph = None

    def draw(self):
        self.window.fill(self.background)
        if self.graph:
            self.graph.draw(self.window, update=False)
        if self.legend:
            self.legend.draw(self.window)
        if self.buttons:
            for current_buttons in self.buttons.values():
                for button in current_buttons.values():
                    button.draw(self.window)

        pygame.display.update()

    def resize_window(self, new_window):
        self.window = new_window

    def add_buttons(self, label, buttons):
        self.buttons[label] = buttons

    def set_legend(self, new_legend):
        self.legend = new_legend

    def set_graph(self, new_graph):
        self.graph = new_graph

    def set_animation_speed(self, new_animation_speed):
        self.animation_speed = new_animation_speed
