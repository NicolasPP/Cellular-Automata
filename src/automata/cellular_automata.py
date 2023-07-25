import pygame

from src.automata.board import Board
from src.automata.cell import Cell
from src.automata.cell import CellState
from src.automata.variation_manager import VariationManager
from src.config import IT_DELAY
from src.config import MOUSECLICK_LEFT
from src.gui.gui_manager import GuiManager


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
    def __init__(self, board_rect: pygame.rect.Rect, cell_size: int) -> None:
        self.cell_size: int = cell_size
        self.board: Board = Board(board_rect, cell_size)
        self.iterate_board: bool = False
        self.gui_manager: GuiManager = GuiManager(self.board.rect)

    def draw(self) -> None:
        self.board.draw()
        pygame.display.get_surface().blit(self.board.container, self.board.rect)
        self.gui_manager.draw()

    def iterate_switch(self) -> None:
        self.iterate_board = not self.iterate_board

    def iterate(self, delta_time: float, acc: Accumulator = Accumulator(IT_DELAY)) -> None:
        if not self.iterate_board: return
        if not acc.delay(delta_time): return

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
                self.gui_manager.variation_title.handle_left_click()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.iterate_switch()

            if event.key == pygame.K_r:
                self.board.randomise()

            if event.key == pygame.K_RIGHT:
                VariationManager.cycle(1)
                self.gui_manager.variation_title.update_title()

            if event.key == pygame.K_LEFT:
                VariationManager.cycle(-1)
                self.gui_manager.variation_title.update_title()

            if event.key == pygame.K_c:
                self.board.clear()
