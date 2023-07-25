import dataclasses
import time

import pygame

from src.automata.cellular_automata import CellularAutomata
from src.automata.variation_manager import VariationManager
from src.config import BACKGROUND
from src.config import BOARD_SIZE
from src.config import CELL_SIZE
from src.config import WINDOW_HEIGHT
from src.config import WINDOW_WIDTH


@dataclasses.dataclass
class AppData:
    done: bool
    board_rect: pygame.rect.Rect
    automata: CellularAutomata
    prev_time: float
    delta_time: float


def init() -> AppData:
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    VariationManager.load_rules()
    board_rect: pygame.rect.Rect = pygame.rect.Rect(0, 0, *BOARD_SIZE)
    board_rect.center = pygame.display.get_surface().get_rect().center
    return AppData(False, board_rect, CellularAutomata(board_rect, CELL_SIZE), 0.0, 0.0)


def main_loop(app_data: AppData) -> None:
    while not app_data.done:
        now: float = time.time()
        app_data.delta_time = now - app_data.prev_time
        app_data.prev_time = now

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                app_data.done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                app_data.automata.board.check_collision()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    app_data.automata.iterate_switch()

                if event.key == pygame.K_r:
                    app_data.automata.board.randomise()

                if event.key == pygame.K_RIGHT:
                    VariationManager.cycle(1)

                if event.key == pygame.K_LEFT:
                    VariationManager.cycle(-1)

        pygame.display.get_surface().fill(BACKGROUND)
        app_data.automata.draw()
        app_data.automata.iterate(app_data.delta_time)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main_loop(init())
