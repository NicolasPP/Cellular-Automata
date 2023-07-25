import typing
import random

import pygame

from src.automata.cell import Cell
from src.automata.cell import CellState

BoardGrid: typing.TypeAlias = list[list[Cell]]


class Board:

    @staticmethod
    def create_grid(container: pygame.surface.Surface, cell_size: int) -> BoardGrid:
        board_grid: BoardGrid = []
        container_width, container_height = container.get_rect().size
        cols: int = container_width // cell_size
        rows: int = container_height // cell_size
        possible_neighbours: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1),
                                                      (-1, -1)]

        for row in range(rows):
            grid_row: list[Cell] = []
            for col in range(cols):
                neighbours: list[tuple[int, int]] = []

                for offset in possible_neighbours:
                    x_offset, y_offset = offset

                    if 0 <= (row + y_offset) < rows and 0 <= (col + x_offset) < cols:
                        neighbours.append((col + x_offset, row + y_offset))

                grid_row.append(Cell(col * cell_size, row * cell_size, cell_size, neighbours, container))

            board_grid.append(grid_row)

        return board_grid

    def __init__(self, rect: pygame.rect.Rect, cell_size: int) -> None:
        self.container: pygame.surface.Surface = pygame.surface.Surface(rect.size)
        self.grid: list[list[Cell]] = Board.create_grid(self.container, cell_size)
        self.cell_size: int = cell_size
        self.rect: pygame.rect.Rect = rect

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

    def pencil(self) -> None:
        collide_index: tuple[int, int] | None = self.check_collision()
        if collide_index is None: return
        col, row = collide_index
        self.grid[col][row].set_state(CellState.ALIVE)

    def get_alive_neighbours_count(self, cell: Cell) -> int:
        alive_neighbour_count: int = 0
        for index in cell.neighbours:
            x, y = index
            if self.grid[y][x].state is CellState.ALIVE:
                alive_neighbour_count += 1
        return alive_neighbour_count
