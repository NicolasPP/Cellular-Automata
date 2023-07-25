import enum

import pygame

from config import ALIVE_COLOR
from config import DEAD_COLOR


class CellState(enum.Enum):
    ALIVE = enum.auto()
    DEAD = enum.auto()


class Cell:
    state_colors: dict[CellState, tuple[int, int, int]] = {CellState.ALIVE: ALIVE_COLOR, CellState.DEAD: DEAD_COLOR}

    def __init__(self, x: int, y: int, size: int, neighbours: list[tuple[int, int]],
                 container: pygame.surface.Surface) -> None:
        self.rect: pygame.rect.Rect = pygame.rect.Rect(x, y, size, size)
        self.surface: pygame.surface.Surface = pygame.surface.Surface((size, size))
        self.state: CellState = CellState.DEAD
        self.neighbours: list[tuple[int, int]] = neighbours
        self.container: pygame.surface.Surface = container

    def set_state(self, state: CellState) -> None:
        self.state = state

    def draw(self) -> None:
        self.surface.fill(Cell.state_colors[self.state])
        self.container.blit(self.surface, self.rect)
