import pygame 
import cell
import colors

class CellGroup:
    __slots__ = ['left', 'top', 'width', 'height', 'cell_width', 'cell_height', 'cells']

    def __init__(self, left: int, top: int, width: int, height: int, 
                 cell_width: int, cell_height: int):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cells: list[list[cell.Cell]] = []

        for i in range(width):
            row = []
            for j in range(height):
                c = cell.Cell(left + j*cell_width, top + i*cell_height, cell_width, cell_height, False)
                row.append(c)
            self.cells.append(row)

    
    def draw(self, screen: pygame.Surface):
        # Four lines
        right = self.left + self.cell_width*self.width
        bottom = self.top + self.cell_height*self.height
        pygame.draw.line(screen, colors.green, (self.left, self.top), (self.left, bottom), 2)
        pygame.draw.line(screen, colors.green, (self.left, self.top), (right, self.top), 2)
        pygame.draw.line(screen, colors.green, (self.left, bottom), (right, bottom), 2)
        pygame.draw.line(screen, colors.green, (right, self.top), (right, bottom), 2)

        for row in self.cells:
            for c in row:
                c.draw(screen, colors.green)
            