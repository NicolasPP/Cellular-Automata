import typing

import pygame

from config import BLOCK_FONT
from config import DEFAULT_PAD
from config import ERASER
from config import PENCIL
from config import TOOLS_FONT_SIZE
from config import SIZE_SQUARE_SIZE
from config import SIZE_SUB_SQUARE_SIZE
from config import BACKGROUND
from config import ALIVE_COLOR
from config import HOVER_COLOR
from config import HOVER_ALPHA
from config import OUTLINE_COLOR
from utils.callback_vars import StrCB
from utils.callback_vars import IntCB


class CollisionResult(typing.NamedTuple):
    pencil: bool
    eraser: bool
    size1: bool
    size2: bool


class BoardToolsGui:
    def __init__(self, board_rect: pygame.rect.Rect) -> None:
        self.board_rect: pygame.rect.Rect = board_rect
        self.font: pygame.font.Font = pygame.font.Font(BLOCK_FONT, TOOLS_FONT_SIZE)
        self.pencil: pygame.surface.Surface = self.font.render(PENCIL, False, ALIVE_COLOR)
        self.eraser: pygame.surface.Surface = self.font.render(ERASER, False, ALIVE_COLOR)

        size: tuple[int, int] = SIZE_SQUARE_SIZE, SIZE_SQUARE_SIZE
        self.size1: pygame.surface.Surface = pygame.surface.Surface(size)
        self.size2: pygame.surface.Surface = pygame.surface.Surface(size)

        self.pencil_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *self.pencil.get_size())
        self.pencil_pos.topright = self.board_rect.topleft
        self.pencil_pos.x -= DEFAULT_PAD

        self.eraser_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *self.eraser.get_size())
        self.eraser_pos.midtop = self.pencil_pos.midbottom
        self.eraser_pos.y += DEFAULT_PAD * 2

        self.size1_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *self.size1.get_size())
        self.size1_pos.midtop = self.eraser_pos.midbottom
        self.size1_pos.y += DEFAULT_PAD * 2

        self.size2_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *self.size2.get_size())
        self.size2_pos.midtop = self.size1_pos.midbottom
        self.size2_pos.y += DEFAULT_PAD * 2

        self.draw_size_surfaces()
        draw_outline(self.pencil)
        draw_outline(self.size1)

    def draw(self) -> None:
        collision_result: CollisionResult = self.check_collision()

        def draw_tool(tool: pygame.surface.Surface, pos: pygame.rect.Rect, is_collided: bool) -> None:
            pygame.display.get_surface().blit(tool, pos)
            if is_collided:
                hover_surface: pygame.surface.Surface = pygame.surface.Surface(tool.get_size())
                hover_surface.set_alpha(HOVER_ALPHA)
                hover_surface.fill(HOVER_COLOR)
                pygame.display.get_surface().blit(hover_surface, pos)

        draw_tool(self.pencil, self.pencil_pos, collision_result.pencil)
        draw_tool(self.eraser, self.eraser_pos, collision_result.eraser)
        draw_tool(self.size1, self.size1_pos, collision_result.size1)
        draw_tool(self.size2, self.size2_pos, collision_result.size2)

    def draw_size_surfaces(self) -> None:
        self.size1.fill(BACKGROUND)
        self.size2.fill(BACKGROUND)

        sub_square: pygame.surface.Surface = pygame.surface.Surface((SIZE_SUB_SQUARE_SIZE, SIZE_SUB_SQUARE_SIZE))
        sub_square.fill(ALIVE_COLOR)

        mid_pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, *sub_square.get_size())
        mid_pos.center = self.size1_pos.width // 2, self.size1_pos.height // 2

        self.size1.blit(sub_square, mid_pos)

        size_offset: int = SIZE_SUB_SQUARE_SIZE + 1
        self.size2.blit(sub_square, mid_pos)
        mid_pos.x += size_offset
        self.size2.blit(sub_square, mid_pos)
        mid_pos.x -= 2 * size_offset
        self.size2.blit(sub_square, mid_pos)
        mid_pos.y -= size_offset
        self.size2.blit(sub_square, mid_pos)
        mid_pos.y += 2 * size_offset
        self.size2.blit(sub_square, mid_pos)
        mid_pos.x += size_offset
        self.size2.blit(sub_square, mid_pos)
        mid_pos.x += size_offset
        self.size2.blit(sub_square, mid_pos)
        mid_pos.y -= 2 * size_offset
        self.size2.blit(sub_square, mid_pos)
        mid_pos.x -= size_offset
        self.size2.blit(sub_square, mid_pos)

    def check_collision(self) -> CollisionResult:
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        pencil_collision: bool = self.pencil_pos.collidepoint(mouse_pos)
        eraser_collision: bool = self.eraser_pos.collidepoint(mouse_pos)
        size1_collision: bool = self.size1_pos.collidepoint(mouse_pos)
        size2_collision: bool = self.size2_pos.collidepoint(mouse_pos)
        return CollisionResult(pencil_collision, eraser_collision, size1_collision, size2_collision)

    def handle_left_click(self, current_tool: StrCB, tool_size: IntCB) -> None:
        collision_result: CollisionResult = self.check_collision()

        if any([collision_result.size1, collision_result.size2]): self.draw_size_surfaces()
        if any([collision_result.eraser, collision_result.pencil]):
            self.pencil: pygame.surface.Surface = self.font.render(PENCIL, False, ALIVE_COLOR)
            self.eraser: pygame.surface.Surface = self.font.render(ERASER, False, ALIVE_COLOR)

        if collision_result.pencil:
            draw_outline(self.pencil)
            current_tool.set(PENCIL)

        elif collision_result.eraser:
            draw_outline(self.eraser)
            current_tool.set(ERASER)

        elif collision_result.size1:
            draw_outline(self.size1)
            tool_size.set(1)

        elif collision_result.size2:
            draw_outline(self.size2)
            tool_size.set(2)


def draw_outline(surface: pygame.surface.Surface) -> None:
    pygame.draw.line(surface, OUTLINE_COLOR, (0.0, 0.0), (surface.get_width(), 0), 1)
    pygame.draw.line(surface, OUTLINE_COLOR, (0.0, 0.0), (0, surface.get_height()), 1)
    pygame.draw.line(surface, OUTLINE_COLOR, (surface.get_width() - 1, surface.get_height() - 1),
                     (surface.get_width() - 1, 0), 2)
    pygame.draw.line(surface, OUTLINE_COLOR, (surface.get_width() - 1, surface.get_height() - 1),
                     (0, surface.get_height() - 1), 1)
