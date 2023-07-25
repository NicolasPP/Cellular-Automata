import pygame

from automata.board import Board
from automata.cell import Cell
from automata.cell import CellState
from automata.variation_manager import VariationManager
from config import IT_DELAY
from config import MOUSECLICK_LEFT
from gui.gui_manager import GuiManager
from utils.accumulator import Accumulator


class CellularAutomata:
    def __init__(self, board_rect: pygame.rect.Rect, cell_size: int) -> None:
        self.accumulator: Accumulator = Accumulator(IT_DELAY)
        self.cell_size: int = cell_size
        self.board: Board = Board(board_rect, cell_size)
        self.iterate_board: bool = False
        self.gui_manager: GuiManager = GuiManager(self.board.rect)
        self._iteration_count: int = 0
        self.iteration_delay: float = IT_DELAY

    @property
    def iteration_count(self) -> int:
        return self._iteration_count

    @iteration_count.setter
    def iteration_count(self, count: int) -> None:
        self._iteration_count = count
        self.gui_manager.iteration_count.update_counter(count)

    @iteration_count.deleter
    def iteration_count(self) -> None:
        del self._iteration_count

    def draw(self) -> None:
        self.board.draw()
        pygame.display.get_surface().blit(self.board.container, self.board.rect)
        self.gui_manager.draw()

    def iterate_switch(self) -> None:
        self.iterate_board = not self.iterate_board

    def iterate(self, delta_time: float) -> None:
        if not self.iterate_board: return
        if not self.accumulator.delay(delta_time): return

        self.iteration_count += 1

        cells_to_change: list[Cell] = VariationManager.get_cells_to_change(self.board)

        for cell in cells_to_change:
            if cell.state is CellState.ALIVE:
                cell.set_state(CellState.DEAD)

            elif cell.state is CellState.DEAD:
                cell.set_state(CellState.ALIVE)

    def handle_user_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.board.pencil()

            if event.button == MOUSECLICK_LEFT:
                self.gui_manager.cycle_buttons.handle_left_click()
                self.gui_manager.iteration_speed.handle_left_click(self.accumulator)
                self.gui_manager.board_control.handle_left_click(self.rando, self.reset)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.iterate_switch()

            if event.key == pygame.K_RIGHT:
                VariationManager.cycle(1)

            if event.key == pygame.K_LEFT:
                VariationManager.cycle(-1)

    def reset(self) -> None:
        self.board.clear()
        self.iteration_count = 0

    def rando(self) -> None:
        self.board.randomise()
        self.iteration_count = 0
