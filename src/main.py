import pygame
import time

from config import WINDOW_WIDTH
from config import WINDOW_HEIGHT
from config import CELL_SIZE
from cellular_automata import CellularAutomata
from rules import Rules

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

        if event.type == pygame.QUIT: done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            automata_manager.check_collision()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                automata_manager.iterate_switch()

            if event.key == pygame.K_r:
                automata_manager.randomise()

            if event.key == pygame.K_RIGHT:
                Rules.cycle(1)

            if event.key == pygame.K_LEFT:
                Rules.cycle(-1)

    pygame.display.get_surface().fill("black")
    automata_manager.draw()
    automata_manager.iterate(delta_time)

    pygame.display.update()

pygame.quit()
