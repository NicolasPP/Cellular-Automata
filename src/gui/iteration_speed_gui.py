import typing

import pygame

from config import ALIVE_COLOR
from config import BLOCK_FONT
from config import DEFAULT_PAD
from config import HOVER_ALPHA
from config import HOVER_COLOR
from config import IT_DELAY
from config import LEFT_ARROW
from config import RIGHT_ARROW
from config import SPEED_STEP
from config import TITLE_FONT_SIZE
from utils.accumulator import Accumulator


class CollisionResult(typing.NamedTuple):
    left: bool
    right: bool


class IterationSpeedGui:
    def __init__(self, board_rect: pygame.rect.Rect) -> None:
        self.board_rect: pygame.rect.Rect = board_rect
        self.font: pygame.font.Font = pygame.font.Font(BLOCK_FONT, TITLE_FONT_SIZE)
        self.font.set_italic(True)
        self.speed_render: pygame.surface.Surface = self.font.render(f"{1 / IT_DELAY} t/s", False, ALIVE_COLOR)
        self.font.set_italic(False)
        self.left_arrow: pygame.surface.Surface = self.font.render(LEFT_ARROW, False, ALIVE_COLOR)
        self.right_arrow: pygame.surface.Surface = self.font.render(RIGHT_ARROW, False, ALIVE_COLOR)
        self.hover_surface: pygame.surface.Surface = pygame.surface.Surface(self.left_arrow.get_size())
        self.hover_surface.set_alpha(HOVER_ALPHA)
        self.hover_surface.fill(HOVER_COLOR)

        self.left_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *self.left_arrow.get_size())
        self.right_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *self.right_arrow.get_size())
        self.speed_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *self.speed_render.get_size())

        self.update_pos()

    def draw(self) -> None:
        collision_result: CollisionResult = self.check_collision()

        def draw_arrow(arrow: pygame.surface.Surface, pos: pygame.rect.Rect, is_collided: bool) -> None:
            pygame.display.get_surface().blit(arrow, pos)
            if is_collided:
                pygame.display.get_surface().blit(self.hover_surface, pos)

        draw_arrow(self.left_arrow, self.left_pos, collision_result.left)
        draw_arrow(self.right_arrow, self.right_pos, collision_result.right)
        pygame.display.get_surface().blit(self.speed_render, self.speed_pos)

    def check_collision(self) -> CollisionResult:
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        left_collision: bool = self.left_pos.collidepoint(mouse_pos)
        right_collision: bool = self.right_pos.collidepoint(mouse_pos)
        return CollisionResult(left_collision, right_collision)

    def handle_left_click(self, accumulator: Accumulator) -> None:
        collision_result: CollisionResult = self.check_collision()

        if collision_result.left:
            accumulator.set_limit(accumulator.get_limit() * SPEED_STEP)

        elif collision_result.right:
            accumulator.set_limit(accumulator.get_limit() / SPEED_STEP)

        if collision_result.left or collision_result.right:
            self.update_speed(accumulator.get_limit())

    def update_pos(self) -> None:
        self.left_pos.topleft = self.board_rect.bottomleft
        self.right_pos.topleft = self.left_pos.topright
        self.speed_pos.topleft = self.right_pos.topright

        self.left_pos.y += DEFAULT_PAD
        self.right_pos.y += DEFAULT_PAD
        self.right_pos.x += DEFAULT_PAD
        self.speed_pos.y += DEFAULT_PAD
        self.speed_pos.x += DEFAULT_PAD * 2

    def update_speed(self, it_delay: float) -> None:
        self.font.set_italic(True)
        self.speed_render = self.font.render(f"{round(1 / it_delay, 2)} t/s", False, ALIVE_COLOR)
