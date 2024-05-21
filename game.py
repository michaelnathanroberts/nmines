from gamestate import GameState
from cellgroup import CellGroup
import pygame
import colors

class Game:
    __slots__ = ['cellgrid', 'state', 'title_font', 'play_rect', 'quit_rect', 'running',
                 'play_again_rect', 'exit_rect']

    def __init__(self):
        self.running = True
        self.cellgrid = CellGroup(200, 200, 10, 10, 50, 50)
        self.state = GameState.Setup
        self.title_font = pygame.font.SysFont("monospace", 50, bold=True)
        self.play_rect = pygame.rect.Rect(500, 650, 200, 100)
        self.quit_rect = pygame.rect.Rect(500, 800, 200, 100)
        self.play_again_rect = pygame.rect.Rect(800, 450, 200, 100)
        self.exit_rect = pygame.rect.Rect(800, 600, 200, 100)
    
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
        title_x = 500 if self.state == GameState.Setup else 350
        surface.blit(label, (title_x, 100))
        if self.state == GameState.Setup:
            self.draw_setup(surface)
        else:
            self.cellgrid.draw(surface)
            if self.state in [GameState.Win, GameState.Lose]:
                self.draw_postgame(surface)
                label = None
                if self.state == GameState.Win:
                    label = self.title_font.render("You Win!!", False, colors.darkgreen)
                else:
                    label = self.title_font.render("You lost.", False, colors.red)
                surface.blit(label, (775, 200))

    
    def handle_click(self):
        x, y = pygame.mouse.get_pos()
        if self.state == GameState.Setup:
            if self.play_rect.left <= x < self.play_rect.right and \
            self.play_rect.top <= y < self.play_rect.bottom:
                self.state = GameState.Play
                self.cellgrid.reset()
                self.cellgrid.init_mines(10)
                self.cellgrid.update_adjacencies()
            elif self.quit_rect.left <= x < self.quit_rect.right and \
            self.quit_rect.top <= y < self.quit_rect.bottom:
                self.running = False
        elif self.state == GameState.Play:
            self.cellgrid.handle_click(x, y)
        elif self.state in [GameState.Win, GameState.Lose]:
            if self.play_again_rect.left <= x < self.play_again_rect.right and \
            self.play_again_rect.top <= y < self.play_again_rect.bottom:
               self.state = GameState.Play
               self.cellgrid.reset()
               self.cellgrid.init_mines(10)
               self.cellgrid.update_adjacencies()
            elif self.exit_rect.left <= x < self.exit_rect.right and \
            self.exit_rect.top <= y < self.exit_rect.bottom:
                self.running = False

    def handle_key(self, event: pygame.event.Event):
        if self.state == GameState.Play:
            if event.key == pygame.K_f:
                self.cellgrid.handle_flag(*pygame.mouse.get_pos())
    
    def update_state(self):
        if self.state == GameState.Play:
            self.state = self.cellgrid.derive_state()

    def draw_postgame(self, screen: pygame.Surface):
        button_font = pygame.font.SysFont("monospace", 25,bold=False)
        play_again_label = button_font.render("Play Again", False, colors.black)
        exit_label = button_font.render("Exit", False, colors.black)
        pygame.draw.rect(screen, colors.aquamarine, self.play_again_rect)
        pygame.draw.rect(screen, colors.yellow, self.exit_rect)
        screen.blit(play_again_label, 
                    (self.play_again_rect.left + 25, self.play_again_rect.top + 37))
        screen.blit(exit_label, 
                    (self.exit_rect.left + 75, self.exit_rect.top + 37))
        
    