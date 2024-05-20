import pygame 
import cell
import colors
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

        for i in range(width):
            row = []
            for j in range(height):
                c = cell.Cell(left + i*cell_width, top + j*cell_height, cell_width, cell_height, False)
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
            self.cell_rows[column][row].is_mine = True

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
                        if self.cell_rows[j + l][i + k].is_mine:
                            current_cell.num_adjacent_mines += 1

    def show(self, row: int, column: int):
        coord_queue: list[tuple[int, int]] = [(row, column)]
        while coord_queue:
            row, column = coord_queue.pop(0)
            current_cell: cell.Cell = self.cell_rows[row][column]
            if not current_cell.is_visible:
                current_cell.is_visible = True
                if current_cell.num_adjacent_mines == 0:
                    for k in range(-1, 2):
                        x = row + k
                        if x < 0 or x >= self.width:
                            continue
                        for l in range(-1, 2):
                            if k == 0 and l == 0:
                                continue
                            y = column + l
                            if y < 0 or y >= self.height:
                                continue
                            coord_queue.append((x, y))

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
        row = (mouse_x - self.left) // self.cell_width
        column = (mouse_y - self.top) // self.cell_height
        print(row, column)
        self.show(row, column)
        
        
            