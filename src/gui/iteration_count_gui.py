import pygame

from config import BLOCK_FONT
from config import TITLE_FONT_SIZE
from config import ALIVE_COLOR


class IterationCountGui:
    def __init__(self, board_rect: pygame.rect.Rect) -> None:
        self.board_rect: pygame.rect.Rect = board_rect
        self.font: pygame.font.Font = pygame.font.Font(BLOCK_FONT, TITLE_FONT_SIZE)
        self.count_render: pygame.surface.Surface = self.font.render("0", False, ALIVE_COLOR)

    def draw(self) -> None:
        pos: pygame.rect.Rect = self.count_render.get_rect(bottomright=self.board_rect.topright)
        pygame.display.get_surface().blit(self.count_render, pos)

    def update_counter(self, count: int) -> None:
        self.count_render = self.font.render(str(count), False, ALIVE_COLOR)
