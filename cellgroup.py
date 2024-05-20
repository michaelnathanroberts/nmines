import pygame 
import cell
import random

class CellGroup:
    __slots__ = ['left', 'top', 'width', 'height', 'cell_width', 'cell_height', 'cell_rows']

    def __init__(self, left: int, top: int, width: int, height: int, 
                 cell_width: int, cell_height: int):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_rows: list[list[cell.Cell]] = []

        for i in range(height):
            row = []
            for j in range(width):
                c = cell.Cell(left + j*cell_width, top + i*cell_height, cell_width, cell_height, False)
                row.append(c)
            self.cell_rows.append(row)

    
    def draw(self, screen: pygame.Surface):
        # Draw each cell
        for row in self.cell_rows:
            for c in row:
                c.draw(screen, cell.Cell.EDGE_COLOR)

    def init_mines(self, num_mines: int):
        pool = list(range(self.width * self.height))
        for i in range(num_mines):
            ordinal = random.choice(pool)
            pool.remove(ordinal)

            row, column = divmod(ordinal, self.width)
            self.cell_rows[row][column].is_mine = True

    def update_adjacencies(self):
        for i in range(self.width):
            for j in range(self.height):
                current_cell = self.cell_rows[j][i]
                current_cell.num_adjacent_mines = 0
                for k in range(-1, 2):
                    x = i + k
                    if x < 0 or x >= self.width:
                        continue
                    for l in range(-1, 2):
                        if k == 0 and l == 0:
                            continue
                        y = j + l
                        if y < 0 or y >= self.height:
                            continue
                        if self.cell_rows[y][x].is_mine:
                            current_cell.num_adjacent_mines += 1

    def show_all(self):
        for row in self.cell_rows:
            for cellobj in row:
                cellobj.is_visible = True

    def handle_click(self, mouse_x: int, mouse_y: int):
        right = self.left + (self.cell_width)*self.width
        bottom = self.top + (self.cell_height)*self.height
        if mouse_x < self.left or mouse_x >= right:
            return
        if mouse_y < self.top or mouse_y >= bottom:
            return
        column = (mouse_x - self.left) // self.cell_width
        row = (mouse_y - self.top) // self.cell_height
        self.show(row, column)

    def show(self, row, column):
        queue = [(row, column)]
        while queue:
            row, column = queue.pop(0)
            current_cell = self.cell_rows[row][column]
            if current_cell.is_visible:
                continue
            current_cell.is_visible = True
            if (current_cell.is_mine or current_cell.num_adjacent_mines > 0):
                continue
            
            for k in range(-1, 2):
                x = column + k
                if x < 0 or x >= self.width:
                    continue
                for l in range(-1, 2):
                    if k == 0 and l == 0:
                        continue
                    y = row + l
                    if y < 0 or y >= self.height:
                        continue
                    queue.append((y, x))
        
            