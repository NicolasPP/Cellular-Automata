import typing

import pygame

from src.automata.variation_manager import VariationManager
from src.config import ALIVE_COLOR
from src.config import BLOCK_FONT
from src.config import DEFAULT_PAD
from src.config import HOVER_ALPHA
from src.config import HOVER_COLOR
from src.config import LEFT_ARROW
from src.config import RIGHT_ARROW
from src.config import TITLE_FONT_SIZE


class CollisionResult(typing.NamedTuple):
    left_arrow: bool
    right_arrow: bool


class CycleButtonsGui:
    def __init__(self, board_rect: pygame.rect.Rect) -> None:
        self.board_rect: pygame.rect.Rect = board_rect
        self.font: pygame.font.Font = pygame.font.Font(BLOCK_FONT, TITLE_FONT_SIZE)
        self.left_arrow: pygame.surface.Surface = self.font.render(LEFT_ARROW, False, ALIVE_COLOR)
        self.right_arrow: pygame.surface.Surface = self.font.render(RIGHT_ARROW, False, ALIVE_COLOR)
        self.hover_surface: pygame.surface.Surface = pygame.surface.Surface(self.left_arrow.get_rect().size)

        self.hover_surface.set_alpha(HOVER_ALPHA)
        self.hover_surface.fill(HOVER_COLOR)

        self.right_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *self.left_arrow.get_size())
        self.left_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *self.right_arrow.get_size())
        self.left_pos.bottomleft = board_rect.topleft
        self.right_pos.midleft = self.left_pos.midright
        self.left_pos.y -= DEFAULT_PAD
        self.right_pos.y -= DEFAULT_PAD
        self.right_pos.x += DEFAULT_PAD

    def check_collision(self) -> CollisionResult:
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        right_collision: bool = self.right_pos.collidepoint(mouse_pos)
        left_collision: bool = self.left_pos.collidepoint(mouse_pos)
        return CollisionResult(left_collision, right_collision)

    def draw(self) -> None:
        collision_result: CollisionResult = self.check_collision()

        def draw_arrow(arrow: pygame.surface.Surface, pos: pygame.rect.Rect, collided: bool) -> None:
            pygame.display.get_surface().blit(arrow, pos)
            if collided:
                pygame.display.get_surface().blit(self.hover_surface, pos)

        draw_arrow(self.left_arrow, self.left_pos, collision_result.left_arrow)
        draw_arrow(self.right_arrow, self.right_pos, collision_result.right_arrow)

    def handle_left_click(self) -> None:
        collision_result: CollisionResult = self.check_collision()

        if collision_result.left_arrow:
            VariationManager.cycle(-1)

        elif collision_result.right_arrow:
            VariationManager.cycle(1)
