import pygame

from automata.variation_manager import VariationManager
from config import ALIVE_COLOR
from config import BLOCK_FONT
from config import DEFAULT_PAD
from config import TITLE_FONT_SIZE


class VariationTitleGui:
    def __init__(self, board_rect: pygame.rect.Rect) -> None:
        self.board_rect: pygame.rect.Rect = board_rect
        self.font: pygame.font.Font = pygame.font.Font(BLOCK_FONT, TITLE_FONT_SIZE)
        self.title_render: pygame.surface.Surface | None = None
        self.title_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, 0, 0)
        VariationManager.get_index().add_callback(lambda value: self.update_title())

    def draw(self) -> None:
        if self.title_render is None: return
        pygame.display.get_surface().blit(self.title_render, self.title_pos)

    def update_title(self) -> None:
        self.title_render = self.font.render(VariationManager.get_current_variation().name, False, ALIVE_COLOR)
        self.update_pos()

    def update_pos(self) -> None:
        if self.title_render is None: return

        title_pos: pygame.rect.Rect = self.title_render.get_rect()
        title_pos.midbottom = self.board_rect.midtop
        title_pos.y -= DEFAULT_PAD

        self.title_pos = title_pos
