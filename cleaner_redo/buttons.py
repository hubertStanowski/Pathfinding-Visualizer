from parameters import *
from screen import *
import pygame


class BigButton:
    def __init__(self, label, x, y, color=FREE_COLOR, width_offset=0, height_offset=0, visible=True):
        self.label = label
        self.x = x
        self.y = y
        self.width_offset = width_offset
        self.height_offset = height_offset
        self.rect = pygame.Rect(
            x, y, BUTTON_WIDTH, BUTTON_HEIGHT-height_offset)
        self.color = color
        self.visible = visible

    def draw(self, window):
        if not self.visible:
            return

        pygame.draw.rect(window, self.color, self.rect)
        current_font = pygame.font.SysFont(FONT, 60)
        label = current_font.render(self.label, True, BLACK)
        text_rect = pygame.Rect(
            self.x + 60 + self.width_offset, self.y + 16 - self.height_offset // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
        window.blit(label, text_rect)


class SmallButton:
    def __init__(self, label, x, y, width_offset=0, color=FREE_COLOR):
        self.label = label
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.width_offset = width_offset

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        current_font = pygame.font.SysFont(FONT, 45)
        label = current_font.render(self.label, True, BLACK)
        text_rect = pygame.Rect(
            self.x + 11 + self.width_offset, self.y + 7, 40, 40)
        window.blit(label, text_rect)

    def select(self):
        self.color = PATH_COLOR

    def unselect(self):
        self.color = FREE_COLOR
