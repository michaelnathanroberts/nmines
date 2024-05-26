import pygame
import colors

class Slider:
    __slots__ = ['left', 'width', 'top', 'height', 'pos', 'background_color', 'point_color']

    def __init__(self, left: int, top: int, width: int, height: int, init_pos: float,
                 background_color: colors.Color, point_color: colors.Color):
        self.left = left
        self.width = width
        self.top = top
        self.height = height
        self.pos = init_pos
        self.background_color = background_color
        self.point_color = point_color

    def draw(self, surface: pygame.Surface):
        rect = pygame.rect.Rect(self.left, self.top, self.width, self.height)
        pygame.draw.rect(surface, self.background_color, rect)
        
        center_x = self.left + (self.pos) * self.width
        center_y = self.top + (self.height) / 2
        pygame.draw.circle(surface, self.point_color, (center_x, center_y), self.height / 2)

    
    def update(self):
        x, y = pygame.mouse.get_pos()
        if self.left <= x <= (self.left + self.width) and self.top <= y <= (self.top + self.height):
            self.pos = (x + 1 - self.left) / self.width