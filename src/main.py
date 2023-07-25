import time

import pygame

from src.automata.cellular_automata import CellularAutomata
from src.automata.variation_manager import VariationManager
from src.config import CELL_SIZE
from src.config import WINDOW_HEIGHT
from src.config import WINDOW_WIDTH

done: bool = False
automata_manager: CellularAutomata = CellularAutomata(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)
prev_time: float = time.time()
delta_time: float = 0.0

pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

while not done:

    now: float = time.time()
    delta_time = now - prev_time
    prev_time = now

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            automata_manager.check_collision()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                automata_manager.iterate_switch()

            if event.key == pygame.K_r:
                automata_manager.randomise()

            if event.key == pygame.K_RIGHT:
                VariationManager.cycle(1)

            if event.key == pygame.K_LEFT:
                VariationManager.cycle(-1)

    pygame.display.get_surface().fill("black")
    automata_manager.draw()
    automata_manager.iterate(delta_time)

    pygame.display.update()

pygame.quit()
