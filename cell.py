import pygame
import colors

class Cell:
    __slots__ = ['x', 'y', 'width', 'height', 'is_mine', 'is_visible',
                  'num_adjacent_mines', 'flagged', '__font']

    MINE_COLORS = [colors.darkred, colors.red, colors.orange, colors.yellow,
                   colors.chartreuse, colors.lime, colors.springgreen,
                   colors.cyan, colors.blue]
    
    EDGE_COLOR = colors.purple

    FLAG_COLOR = colors.hotpink

    def __init__(self, x: int, y: int, width: int, height: int, is_mine: bool=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_mine = is_mine
        self.is_visible = False
        self.num_adjacent_mines = 0
        self.__font = None
        self.flagged = False

    def draw(self, screen: pygame.Surface, color: colors.Color):
        rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        half_width = self.width // 2
        half_height = self.height // 2
        quarter_width = self.width // 4
        quarter_height = self.height // 4
        effect_x = quarter_width + self.x
        effect_y = quarter_height + self.y
        effect_rect = pygame.rect.Rect(effect_x, effect_y, half_width, half_height)
        
        if not self.is_visible:
            pygame.draw.rect(screen, colors.grey, rect)
            pygame.draw.rect(screen, color, rect, 2)
            if self.flagged:
                pygame.draw.rect(screen, self.FLAG_COLOR, effect_rect)
            return
         
        if self.is_mine:
            pygame.draw.rect(screen, colors.grey, rect)
            pygame.draw.rect(screen, color, rect, 2)
            pygame.draw.ellipse(screen, self.MINE_COLORS[0], effect_rect, 0)
            return
        else:
            pygame.draw.rect(screen, colors.black, rect)
            pygame.draw.rect(screen, color, rect, 2)
        
        if self.__font == None:
            self.__font = pygame.font.SysFont("monospace", min(half_width, half_height), bold=True)

        if self.num_adjacent_mines > 0:
            label = self.__font.render(str(self.num_adjacent_mines), False, 
                               self.MINE_COLORS[self.num_adjacent_mines])
            screen.blit(label, (effect_x, effect_y))



    

