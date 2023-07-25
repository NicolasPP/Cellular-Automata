import typing

import pygame

from src.automata.variation_manager import VariationManager
from src.config import ALIVE_COLOR
from src.config import BLOCK_FONT
from src.config import DEFAULT_PAD
from src.config import LEFT_ARROW
from src.config import RIGHT_ARROW
from src.config import TITLE_FONT_SIZE


class CollisionResult(typing.NamedTuple):
    left_arrow: bool
    right_arrow: bool


class VariationTitleGui:
    def __init__(self, board_rect: pygame.rect.Rect) -> None:
        self.board_rect: pygame.rect.Rect = board_rect
        self.font: pygame.font.Font = pygame.font.Font(BLOCK_FONT, TITLE_FONT_SIZE)
        self.title_render: pygame.surface.Surface | None = None
        self.left_arrow: pygame.surface.Surface = self.font.render(LEFT_ARROW, False, ALIVE_COLOR)
        self.right_arrow: pygame.surface.Surface = self.font.render(RIGHT_ARROW, False, ALIVE_COLOR)
        self.title_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, 0, 0)
        self.right_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, 0, 0)
        self.left_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, 0, 0)
        self.hover_surface: pygame.surface.Surface = pygame.surface.Surface(self.left_arrow.get_rect().size)
        self.hover_surface.set_alpha(20)
        self.hover_surface.fill("white")

    def draw(self) -> None:
        if self.title_render is None: return
        pygame.display.get_surface().blit(self.left_arrow, self.left_pos)
        collision_result: CollisionResult = self.check_collision()

        if collision_result.left_arrow:
            pygame.display.get_surface().blit(self.hover_surface, self.left_pos)

        pygame.display.get_surface().blit(self.title_render, self.title_pos)

        if collision_result.right_arrow:
            pygame.display.get_surface().blit(self.hover_surface, self.right_pos)

        pygame.display.get_surface().blit(self.right_arrow, self.right_pos)

    def check_collision(self) -> CollisionResult:
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        right_collision: bool = self.right_pos.collidepoint(mouse_pos)
        left_collision: bool = self.left_pos.collidepoint(mouse_pos)
        return CollisionResult(left_collision, right_collision)

    def update_title(self) -> None:
        self.title_render = self.font.render(VariationManager.get_current_variation().name, False, ALIVE_COLOR)
        self.update_pos()

    def update_pos(self) -> None:
        if self.title_render is None: return

        title_pos: pygame.rect.Rect = self.title_render.get_rect()
        title_pos.midbottom = self.board_rect.midtop
        title_pos.y -= DEFAULT_PAD

        left_pos: pygame.rect.Rect = self.left_arrow.get_rect()
        left_pos.midright = title_pos.midleft
        left_pos.x -= DEFAULT_PAD

        right_pos: pygame.rect.Rect = self.right_arrow.get_rect()
        right_pos.midleft = title_pos.midright
        right_pos.x += DEFAULT_PAD

        self.title_pos = title_pos
        self.left_pos = left_pos
        self.right_pos = right_pos

    def handle_left_click(self) -> None:
        collision_result: CollisionResult = self.check_collision()

        if collision_result.left_arrow:
            VariationManager.cycle(-1)
            self.update_title()

        elif collision_result.right_arrow:
            VariationManager.cycle(1)
            self.update_title()
