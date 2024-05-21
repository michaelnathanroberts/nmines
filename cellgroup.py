import pygame 
from cell import Cell
import random
from gamestate import GameState

class CellGroup:
    __slots__ = ['left', 'top', 'width', 'height', 'cell_width', 'cell_height',
                  'cell_rows']

    def __init__(self, left: int, top: int, width: int, height: int, 
                 cell_width: int, cell_height: int):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_rows: list[list[Cell]] = []

        for i in range(height):
            row = []
            for j in range(width):
                c = Cell(left + j*cell_width, top + i*cell_height, cell_width, cell_height, False)
                row.append(c)
            self.cell_rows.append(row)

    
    def draw(self, screen: pygame.Surface):
        # Draw each cell
        for row in self.cell_rows:
            for c in row:
                c.draw(screen, Cell.EDGE_COLOR)

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
    
    def reset(self):
        for row in self.cell_rows:
            for cellobj in row:
                cellobj.flagged = False
                cellobj.is_mine = False
                cellobj.is_visible = False

    def show_all(self):
        for row in self.cell_rows:
            for cellobj in row:
                cellobj.is_visible = True

    def handle_click(self, mouse_x: int, mouse_y: int):
        coords = self.get_cell(mouse_x, mouse_y)
        if coords is not None:
            self.show(*coords)

    def handle_flag(self, mouse_x: int, mouse_y: int):
        coords = self.get_cell(mouse_x, mouse_y)
        if coords is not None:
            row, column = coords
            c = self.cell_rows[row][column]
            c.flagged = not c.flagged

    def get_cell(self, mouse_x: int, mouse_y: int):
        right = self.left + (self.cell_width)*self.width
        bottom = self.top + (self.cell_height)*self.height
        if mouse_x < self.left or mouse_x >= right:
            return None
        if mouse_y < self.top or mouse_y >= bottom:
            return None
        column = (mouse_x - self.left) // self.cell_width
        row = (mouse_y - self.top) // self.cell_height
        return row, column

    def show(self, row, column):
        queue = [(row, column)]
        while queue:
            row, column = queue.pop(0)
            current_cell = self.cell_rows[row][column]
            if current_cell.is_visible or current_cell.flagged:
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

    def derive_state(self):
        state = GameState.Win
        for cell_row in self.cell_rows:
            for cell in cell_row:
                if cell.is_mine:
                    if cell.is_visible:
                        self.show_mines()
                        return GameState.Lose
                else:
                    if not cell.is_visible:
                        state = GameState.Play
        return state
    
    def show_mines(self):
         for cell_row in self.cell_rows:
            for cell in cell_row:
                if cell.is_mine:
                    cell.is_visible = True
        
            