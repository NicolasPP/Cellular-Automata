import pygame.rect

from src.config import BLOCK_FONT
from src.config import TITLE_FONT_SIZE
from src.config import ALIVE_COLOR


class VariationTitleGui:
    def __init__(self, board_rect: pygame.rect.Rect) -> None:
        self.font: pygame.font.Font = pygame.font.Font(BLOCK_FONT, TITLE_FONT_SIZE)

    def draw(self) -> None:
        render = self.font.render("hello world!", False, ALIVE_COLOR)
        pygame.display.get_surface().blit(render, (20, 20))
