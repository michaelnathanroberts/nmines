from gamestate import GameState
from cellgroup import CellGroup
import pygame
import colors

class Game:
    __slots__ = ['cellgrid', 'state', 'title_font', 'play_rect', 'quit_rect', 'running']

    def __init__(self):
        self.running = True
        self.cellgrid = CellGroup(200, 200, 10, 10, 50, 50)
        self.state = GameState.Setup
        self.title_font = pygame.font.SysFont("monospace", 50, bold=True)
        self.play_rect = pygame.rect.Rect(500, 650, 200, 100)
        self.quit_rect = pygame.rect.Rect(500, 800, 200, 100)
    
    def draw_setup(self, surface: pygame.Surface):
        button_font = pygame.font.SysFont("monospace", 50,bold=False)
        pygame.draw.rect(surface, colors.lime, self.play_rect)
        pygame.draw.rect(surface, colors.pink, self.quit_rect)
        play_label = button_font.render("Play", False, colors.black)
        quit_label = button_font.render("Quit", False, colors.black)
        surface.blit(play_label, (self.play_rect.left + 40, self.play_rect.top + 20))
        surface.blit(quit_label, (self.quit_rect.left + 40, self.quit_rect.top + 20))

    def draw(self, surface: pygame.Surface):
        label = self.title_font.render("n Mines", False, colors.navyblue)
        surface.blit(label, (500, 100))
        if self.state == GameState.Setup:
            self.draw_setup(surface)
        else:
            self.cellgrid.draw(surface)

    
    def handle_click(self):
        x, y = pygame.mouse.get_pos()
        if self.state == GameState.Setup:
            if self.play_rect.left <= x < self.play_rect.right and \
            self.play_rect.top <= y < self.play_rect.bottom:
                self.state = GameState.Play
                self.cellgrid.init_mines(10)
                self.cellgrid.update_adjacencies()
            elif self.quit_rect.left <= x < self.quit_rect.right and \
            self.quit_rect.top <= y < self.quit_rect.bottom:
                self.running = False
        elif self.state == GameState.Play:
            self.cellgrid.handle_click(x, y)

    def handle_key(self, event: pygame.event.Event):
        if self.state == GameState.Play:
            if event.key == pygame.K_f:
                self.cellgrid.handle_flag(*pygame.mouse.get_pos())


    