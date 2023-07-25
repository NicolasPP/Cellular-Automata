import typing
import pygame

from config import ALIVE_COLOR
from config import BLOCK_FONT
from config import DEFAULT_PAD
from config import HOVER_ALPHA
from config import HOVER_COLOR
from config import CONTROL_FONT_SIZE
from config import RANDO
from config import RESET


class CollisionResult(typing.NamedTuple):
    rando: bool
    reset: bool


class BoardControlGui:
    def __init__(self, board_rect: pygame.rect.Rect) -> None:
        self.board_rect: pygame.rect.Rect = board_rect
        self.font: pygame.font.Font = pygame.font.Font(BLOCK_FONT, CONTROL_FONT_SIZE)
        self.rando_button: pygame.surface.Surface = self.font.render(RANDO, False, ALIVE_COLOR)
        self.reset_button: pygame.surface.Surface = self.font.render(RESET, False, ALIVE_COLOR)
        self.hover_surface: pygame.surface.Surface = pygame.surface.Surface(self.rando_button.get_size())
        self.hover_surface.set_alpha(HOVER_ALPHA)
        self.hover_surface.fill(HOVER_COLOR)

        self.reset_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *self.reset_button.get_size())
        self.reset_pos.topright = self.board_rect.bottomright

        self.rando_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *self.rando_button.get_size())
        self.rando_pos.topright = self.reset_pos.topleft

        self.reset_pos.y += DEFAULT_PAD
        self.rando_pos.y += DEFAULT_PAD

        self.rando_pos.x -= DEFAULT_PAD * 2

    def check_collision(self) -> CollisionResult:
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        rando_collision: bool = self.rando_pos.collidepoint(mouse_pos)
        reset_collision: bool = self.reset_pos.collidepoint(mouse_pos)
        return CollisionResult(rando_collision, reset_collision)

    def draw(self) -> None:
        collide_result: CollisionResult = self.check_collision()

        def draw_button(button: pygame.surface.Surface, pos: pygame.rect.Rect, is_collided: bool) -> None:
            pygame.display.get_surface().blit(button, pos)
            if is_collided:
                pygame.display.get_surface().blit(self.hover_surface, pos)

        draw_button(self.rando_button, self.rando_pos, collide_result.rando)
        draw_button(self.reset_button, self.reset_pos, collide_result.reset)

    def handle_left_click(self, rando_func: typing.Callable[[], None],
                          reset_func: typing.Callable[[], None]) -> None:
        collide_result: CollisionResult = self.check_collision()

        if collide_result.rando: rando_func()

        elif collide_result.reset: reset_func()
