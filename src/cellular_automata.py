import random
import typing

import pygame

from config import IT_DELAY
from rules import Rules
from cell import Cell
from cell import CellState


class Accumulator:
    def __init__(self, limit: float) -> None:
        self.limit: float = limit
        self.value: float = 0.0

    def delay(self, delta_time: float) -> bool:
        self.value += delta_time
        if self.value >= self.limit:
            self.value = 0
            return True
        return False


class CellularAutomata:

    @staticmethod
    def create_board(window_width: int, window_height: int, cell_size: int) -> list[list[Cell]]:
        board: list[list[Cell]] = []
        columns: int = window_width // cell_size
        rows: int = window_height // cell_size

        possible_neighbours: list[tuple[int, int]] = [
            (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)
        ]

        for row in range(rows):
            board_row: list[Cell] = []
            for col in range(columns):

                neighbours: list[tuple[int, int]] = []

                for n_offset in possible_neighbours:
                    x_offset, y_offset = n_offset

                    if 0 <= (row + y_offset) < rows and 0 <= (col + x_offset) < columns:
                        neighbours.append((col + x_offset, row + y_offset))

                cell: Cell = Cell(col * cell_size, row * cell_size, cell_size)
                cell.set_neighbours(neighbours)
                board_row.append(cell)

            board.append(board_row)

        return board

    def __init__(self, window_width: int, window_height: int, cell_size: int) -> None:
        Rules.load_rules()
        self.width: int = window_width
        self.height: int = window_height
        self.cell_size: int = cell_size
        self.board: list[list[Cell]] = CellularAutomata.create_board(window_width, window_height, cell_size)
        self.iterate_board: bool = False

    def board_it(self) -> typing.Generator[Cell, None, None]:
        for board_rows in self.board:
            for cell in board_rows:
                yield cell

    def draw(self) -> None:
        for cell in self.board_it():
            cell.draw()

    def iterate_switch(self) -> None:
        self.iterate_board = not self.iterate_board

    def check_collision(self) -> None:
        x, y = pygame.mouse.get_pos()
        col: int = y // self.cell_size
        row: int = x // self.cell_size
        if col >= self.height // self.cell_size or row >= self.width // self.cell_size:
            return
        self.board[col][row].set_state(CellState.ALIVE)

    def iterate(self, delta_time: float, acc: Accumulator = Accumulator(IT_DELAY)) -> None:
        if not self.iterate_board: return
        if not acc.delay(delta_time): return

        cells_to_change: list[Cell] = Rules.get_cells_to_change(self.board)

        for cell in cells_to_change:
            if cell.state is CellState.ALIVE:
                cell.set_state(CellState.DEAD)

            elif cell.state is CellState.DEAD:
                cell.set_state(CellState.ALIVE)

    def randomise(self) -> None:
        state: dict[int, CellState] = {0: CellState.ALIVE, 1: CellState.DEAD}
        for cell in self.board_it(): cell.set_state(state[random.randint(0, 1)])
