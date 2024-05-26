from gamestate import GameState
from cellgroup import CellGroup
import pygame
import colors
from slider import Slider

class Game:
    __slots__ = ['cellgrid', 'state', 'title_font', 'play_rect', 'quit_rect', 'running',
                 'menu_rect', 'play_again_rect', 'exit_rect', 'width_slider',
                 'height_slider', 'minecount_slider', 'minecount']
    
    WIDTH_BOUNDS = HEIGHT_BOUNDS = [2, 20]


    def __init__(self):
        self.running = True
        self.cellgrid = CellGroup(200, 200, 15, 15, 50, 50)
        self.state = GameState.Setup
        self.title_font = pygame.font.SysFont("monospace", 50, bold=True)
        self.play_rect = pygame.rect.Rect(500, 650, 200, 100)
        self.quit_rect = pygame.rect.Rect(500, 800, 200, 100)
        self.menu_rect = pygame.rect.Rect(1000, 300, 200, 100)
        self.play_again_rect = pygame.rect.Rect(1000, 450, 200, 100)
        self.exit_rect = pygame.rect.Rect(1000, 600, 200, 100)
        self.width_slider = Slider(400, 300, 500, 50, 0.5, colors.black, colors.red)
        self.height_slider = Slider(400, 400, 500, 50, 0.5, colors.black, colors.red)
        self.minecount_slider = Slider(400, 500, 500, 50, 0.5, colors.black, colors.red)
        self.minecount = 10
    
    def draw_setup(self, surface: pygame.Surface):
        button_font = pygame.font.SysFont("monospace", 50,bold=False)
        pygame.draw.rect(surface, colors.lime, self.play_rect)
        pygame.draw.rect(surface, colors.pink, self.quit_rect)
        play_label = button_font.render("Play", False, colors.black)
        quit_label = button_font.render("Quit", False, colors.black)
        surface.blit(play_label, (self.play_rect.left + 40, self.play_rect.top + 20))
        surface.blit(quit_label, (self.quit_rect.left + 40, self.quit_rect.top + 20))

        width_text = button_font.render("Width:", False, colors.red)
        height_text = button_font.render("Height: ", False, colors.red)
        mine_text = button_font.render("# Mines: ", False, colors.red)

        surface.blit(width_text, (self.width_slider.left - 300, self.width_slider.top))
        surface.blit(height_text, (self.height_slider.left - 300, self.height_slider.top))
        surface.blit(mine_text, (self.minecount_slider.left - 300, self.minecount_slider.top))

        self.width_slider.draw(surface)
        self.height_slider.draw(surface)
        self.minecount_slider.draw(surface)

        width_value = self.get_value(self.width_slider, self.WIDTH_BOUNDS)
        height_value = self.get_value(self.height_slider, self.HEIGHT_BOUNDS)
        mine_value = self.get_value(self.minecount_slider, self.get_mine_bounds())

        width_label = button_font.render(str(width_value), False, colors.red)
        height_label = button_font.render(str(height_value), False, colors.red)
        mine_label = button_font.render(str(mine_value), False, colors.red)

        width_x = self.width_slider.left + self.width_slider.width + self.width_slider.height
        height_x = self.height_slider.left + self.height_slider.height + self.height_slider.width
        mine_x = self.minecount_slider.left + self.minecount_slider.width + self.minecount_slider.height

        surface.blit(width_label, (width_x, self.width_slider.top))
        surface.blit(height_label, (height_x, self.height_slider.top))
        surface.blit(mine_label, (mine_x, self.minecount_slider.top))



    def draw(self, surface: pygame.Surface):
        label = self.title_font.render("n Mines", False, colors.navyblue)
        title_x = 500 
        surface.blit(label, (title_x, 100))
        if self.state == GameState.Setup:
            self.draw_setup(surface)
        else:
            self.cellgrid.draw(surface)
            self.draw_controls(surface)
            if self.state in [GameState.Win, GameState.Lose]:
                label = None
                if self.state == GameState.Win:
                    label = self.title_font.render("You Win!!", False, colors.darkgreen)
                else:
                    label = self.title_font.render("You lost.", False, colors.red)
                surface.blit(label, (975, 200))

    
    def handle_click(self):
        x, y = pygame.mouse.get_pos()
        if self.state == GameState.Setup:
            if self.play_rect.left <= x < self.play_rect.right and \
            self.play_rect.top <= y < self.play_rect.bottom:
                width = self.get_value(self.width_slider, self.WIDTH_BOUNDS)
                height = self.get_value(self.height_slider, self.HEIGHT_BOUNDS)
                cell_width = int(750 / width)
                cell_height = int(750 / height)
                cell_side = min(cell_width, cell_height)
                self.cellgrid = CellGroup(200, 200, width, height, cell_side, cell_side)
                self.minecount = self.get_value(self.minecount_slider, self.get_mine_bounds())
                self.reset_grid()
            elif self.quit_rect.left <= x < self.quit_rect.right and \
            self.quit_rect.top <= y < self.quit_rect.bottom:
                self.running = False
        elif self.state == GameState.Play:
            self.cellgrid.handle_click(x, y)
            self.implement_controls(x, y)
        elif self.state in [GameState.Win, GameState.Lose]:
            self.implement_controls(x, y)

    def handle_key(self, event: pygame.event.Event):
        if self.state == GameState.Play:
            if event.key == pygame.K_f:
                self.cellgrid.handle_flag(*pygame.mouse.get_pos())

    def handle_hover(self):
        if self.state == GameState.Setup:
            self.width_slider.update()
            self.height_slider.update()
            self.minecount_slider.update()
    
    def update_state(self):
        if self.state == GameState.Play:
            self.state = self.cellgrid.derive_state()
        

    def draw_controls(self, screen: pygame.Surface):
        button_font = pygame.font.SysFont("monospace", 25,bold=False)
        menu_label = button_font.render("Menu", False, colors.white)
        play_again_label = button_font.render("Restart", False, colors.black)
        exit_label = button_font.render("Exit", False, colors.black)
        pygame.draw.rect(screen, colors.blueviolet, self.menu_rect)
        pygame.draw.rect(screen, colors.aquamarine, self.play_again_rect)
        pygame.draw.rect(screen, colors.hotpink, self.exit_rect)
        screen.blit(menu_label,
                    (self.menu_rect.left + 75, self.menu_rect.top + 37))
        screen.blit(play_again_label, 
                    (self.play_again_rect.left + 50, self.play_again_rect.top + 37))
        screen.blit(exit_label, 
                    (self.exit_rect.left + 75, self.exit_rect.top + 37))
        
    def implement_controls(self, mouse_x, mouse_y):
        if self.play_again_rect.left <= mouse_x < self.play_again_rect.right and \
        self.play_again_rect.top <= mouse_y < self.play_again_rect.bottom:
             self.reset_grid()  
        elif self.exit_rect.left <= mouse_x < self.exit_rect.right and \
        self.exit_rect.top <= mouse_y < self.exit_rect.bottom:
            self.running = False
        elif self.menu_rect.left <= mouse_x <self.menu_rect.right and \
        self.menu_rect.top <= mouse_y < self.menu_rect.bottom:
            self.state = GameState.Setup

    def reset_grid(self):
        self.state = GameState.Play
        self.cellgrid.reset()
        self.cellgrid.init_mines(self.minecount)
        self.cellgrid.update_adjacencies()

    def get_mine_bounds(self):
        width_range = self.get_value(self.width_slider, self.WIDTH_BOUNDS)
        height_range = self.get_value(self.height_slider, self.HEIGHT_BOUNDS)
        return [1, width_range * height_range - 1]
    
    def get_value(self, slider: Slider, bounds: tuple[int, int]):
        return round(slider.pos * (bounds[1] - bounds[0]) + bounds[0])
        
    