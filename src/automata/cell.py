import enum

import pygame


class CellState(enum.Enum):
    ALIVE = "black"
    DEAD = "white"


class Cell:

    def __init__(self,
                 x: int,
                 y: int,
                 size: int,
                 neighbours: list[tuple[int, int]],
                 container: pygame.surface.Surface
                 ) -> None:
        self.rect: pygame.rect.Rect = pygame.rect.Rect(x, y, size, size)
        self.surface: pygame.surface.Surface = pygame.surface.Surface((size, size))
        self.state: CellState = CellState.DEAD
        self.neighbours: list[tuple[int, int]] = neighbours
        self.container: pygame.surface.Surface = container

    def set_state(self, state: CellState) -> None:
        self.state = state

    def draw(self) -> None:
        self.surface.fill(self.state.value)
        self.container.blit(self.surface, self.rect)
