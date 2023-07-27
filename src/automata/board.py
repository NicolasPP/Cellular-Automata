import typing
import random

import pygame

from automata.cell import Cell
from automata.cell import CellState
from config import BACKGROUND
from config import CELL_HOVER_ALPHA
from config import ALIVE_COLOR
from config import DEAD_COLOR
from config import PENCIL
from config import ERASER
from config import IMMEDIATE_NEIGHBOURS
from utils.callback_vars import StrCB
from utils.callback_vars import IntCB

BoardGrid: typing.TypeAlias = list[list[Cell]]


class Board:

    @staticmethod
    def create_grid(container: pygame.surface.Surface, cell_size: int) -> BoardGrid:
        board_grid: BoardGrid = []
        container_width, container_height = container.get_rect().size
        cols: int = container_width // cell_size
        rows: int = container_height // cell_size
        cols_offset: int = (container_width - (cols * cell_size)) // 2
        rows_offset: int = (container_width - (rows * cell_size)) // 2

        for row in range(rows):
            grid_row: list[Cell] = []
            for col in range(cols):
                neighbours: list[tuple[int, int]] = []

                for offset in IMMEDIATE_NEIGHBOURS:
                    x_offset, y_offset = offset

                    if 0 <= (row + y_offset) < rows and 0 <= (col + x_offset) < cols:
                        neighbours.append((col + x_offset, row + y_offset))
                x: int = (col * cell_size) + cols_offset
                y: int = (row * cell_size) + rows_offset
                grid_row.append(Cell(x, y, cell_size, neighbours, container))

            board_grid.append(grid_row)

        return board_grid

    def __init__(self, rect: pygame.rect.Rect, cell_size: int) -> None:
        self.container: pygame.surface.Surface = pygame.surface.Surface(rect.size)
        self.container.fill(BACKGROUND)
        self.grid: list[list[Cell]] = Board.create_grid(self.container, cell_size)
        self.cell_size: int = cell_size
        self.rect: pygame.rect.Rect = rect
        self.hover_surface: pygame.surface.Surface = pygame.surface.Surface((cell_size, cell_size))
        self.hover_surface.set_alpha(CELL_HOVER_ALPHA)
        self.current_tool: StrCB = StrCB(PENCIL)
        self.tool_size: IntCB = IntCB(1)

    def cells_gen(self) -> typing.Generator[Cell, None, None]:
        for grid_row in self.grid:
            for cell in grid_row:
                yield cell

    def randomise(self) -> None:
        state: dict[int, CellState] = {0: CellState.ALIVE, 1: CellState.DEAD}
        for cell in self.cells_gen(): cell.set_state(state[random.randint(0, 1)])

    def clear(self) -> None:
        for cell in self.cells_gen(): cell.set_state(CellState.DEAD)

    def draw(self) -> None:
        for cell in self.cells_gen(): cell.draw()
        collision_index: tuple[int, int] | None = self.check_collision()
        if collision_index is None: return
        col, row = collision_index
        cells_to_change: list[Cell] = [self.grid[col][row]]

        if self.tool_size.get() == 2:
            for index_offset in IMMEDIATE_NEIGHBOURS:
                c, r = index_offset
                if col + c < 0 or col + c >= len(self.grid): continue
                if row + r < 0 or row + r >= len(self.grid[0]): continue
                cells_to_change.append(self.grid[col + c][row + r])

        for cell in cells_to_change:
            if cell.state is CellState.ALIVE:
                self.hover_surface.fill(DEAD_COLOR)

            elif cell.state is CellState.DEAD:
                self.hover_surface.fill(ALIVE_COLOR)

            self.container.blit(self.hover_surface, cell.rect)

    def check_collision(self) -> tuple[int, int] | None:
        x, y = pygame.mouse.get_pos()
        col: int = (y - self.rect.y) // self.cell_size
        row: int = (x - self.rect.x) // self.cell_size

        guard_clauses: list[bool] = [col >= self.rect.height // self.cell_size,  # row_overflow
                                     row >= self.rect.width // self.cell_size,  # col_overflow
                                     x < self.rect.x or x >= (self.rect.x + self.rect.width),  # x_out_of_bounds
                                     y < self.rect.y or y >= (self.rect.y + self.rect.height)]  # y_out_of_bounds
        if any(guard_clauses): return None

        return col, row

    def modify(self) -> None:
        collide_index: tuple[int, int] | None = self.check_collision()
        if collide_index is None: return
        col, row = collide_index
        cells_to_change: list[Cell] = [self.grid[col][row]]

        if self.current_tool.get() == PENCIL:
            new_state = CellState.ALIVE

        elif self.current_tool.get() == ERASER:
            new_state = CellState.DEAD

        else:
            raise Exception(f"tool name : {self.current_tool.get()} is not valid")

        if self.tool_size.get() == 2:
            for index_offset in IMMEDIATE_NEIGHBOURS:
                c, r = index_offset
                if col + c < 0 or col + c >= len(self.grid): continue
                if row + r < 0 or row + r >= len(self.grid[0]): continue
                cells_to_change.append(self.grid[col + c][row + r])

        for cell in cells_to_change:
            cell.set_state(new_state)

    def get_alive_neighbours_count(self, cell: Cell) -> int:
        alive_neighbour_count: int = 0
        for index in cell.neighbours:
            x, y = index
            if self.grid[y][x].state is CellState.ALIVE:
                alive_neighbour_count += 1
        return alive_neighbour_count
