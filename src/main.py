import time

import pygame

from automata.cellular_automata import CellularAutomata
from automata.variation_manager import VariationManager
from config import BACKGROUND
from config import BOARD_SIZE
from config import CELL_SIZE
from config import WINDOW_HEIGHT
from config import WINDOW_WIDTH


class App:
    def __init__(self) -> None:
        pygame.font.init()
        VariationManager.load_rules()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.board_rect: pygame.rect.Rect = pygame.rect.Rect(0, 0, *BOARD_SIZE)
        self.board_rect.center = pygame.display.get_surface().get_rect().center
        self.automata: CellularAutomata = CellularAutomata(self.board_rect, CELL_SIZE)
        self.automata.gui_manager.variation_title.update_title()
        self.done: bool = False
        self.prev_time: float = 0.0
        self.delta_time: float = 0.0

    def main_loop(self) -> None:
        while not self.done:
            now: float = time.time()
            self.delta_time = now - self.prev_time
            self.prev_time = now

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.done = True

                self.automata.handle_user_input(event)

            pygame.display.get_surface().fill(BACKGROUND)
            self.automata.update()
            self.automata.draw()
            self.automata.iterate(self.delta_time)
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    App().main_loop()
