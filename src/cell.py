import enum
import pygame


class CellState(enum.Enum):
    ALIVE = "black"
    DEAD = "white"


class Cell:

    def __init__(self, x: int, y: int, size: int) -> None:
        self.rect: pygame.rect.Rect = pygame.rect.Rect(x, y, size, size)
        self.surface: pygame.surface.Surface = pygame.surface.Surface((size, size))
        self.state: CellState = CellState.DEAD
        self.neighbours: list[tuple[int, int]] = []

    def set_state(self, state: CellState) -> None:
        self.state = state

    def set_neighbours(self, neighbours: list[tuple[int, int]]) -> None:
        assert len(neighbours) > 0, "LifeCell must have more than 0 neighbours"
        self.neighbours = neighbours

    def draw(self) -> None:
        self.surface.fill(self.state.value)
        pygame.display.get_surface().blit(self.surface, self.rect)
