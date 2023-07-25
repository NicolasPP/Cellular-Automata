import pygame

from config import ALIVE_COLOR
from config import BLOCK_FONT
from config import CONTROL_FONT_SIZE
from config import DEFAULT_PAD
from config import HOVER_ALPHA
from config import HOVER_COLOR
from config import PLAY
from config import STOP
from utils.callback_vars import BoolCB


class PlayButtonGui:
    def __init__(self, board_rect: pygame.rect.Rect, board_iterate: BoolCB) -> None:
        self.board_rect: pygame.rect.Rect = board_rect
        self.iterate_board: BoolCB = board_iterate
        self.font: pygame.font.Font = pygame.font.Font(BLOCK_FONT, CONTROL_FONT_SIZE)
        self.play_render: pygame.surface.Surface = self.font.render(PLAY, False, ALIVE_COLOR)
        self.stop_render: pygame.surface.Surface = self.font.render(STOP, False, ALIVE_COLOR)
        self.current_render: pygame.surface.Surface = self.play_render
        self.pos: pygame.rect.Rect = pygame.rect.Rect(0, 0, 0, 0)
        self.update_pos()

    def draw(self) -> None:
        pygame.display.get_surface().blit(self.current_render, self.pos)
        if self.check_collision():
            hover_surface: pygame.surface.Surface = pygame.surface.Surface(self.current_render.get_size())
            hover_surface.set_alpha(HOVER_ALPHA)
            hover_surface.fill(HOVER_COLOR)
            pygame.display.get_surface().blit(hover_surface, self.pos)

    def check_collision(self) -> bool:
        rect: pygame.rect.Rect = pygame.rect.Rect(*self.pos.topleft, 0, 0)
        if self.iterate_board.get():
            rect.size = self.stop_render.get_rect().size

        else:
            rect.size = self.play_render.get_rect().size

        return rect.collidepoint(pygame.mouse.get_pos())

    def handle_left_click(self) -> None:
        if self.check_collision():
            self.iterate_board.set(not self.iterate_board.get())
            self.update_current_render()

    def update_current_render(self) -> None:
        if self.iterate_board.get():
            self.current_render = self.stop_render

        else:
            self.current_render = self.play_render

        self.update_pos()

    def update_pos(self) -> None:
        rect: pygame.rect.Rect = pygame.rect.Rect(0, 0, 0, 0)
        if self.iterate_board.get():
            rect.size = self.stop_render.get_rect().size

        else:
            rect.size = self.play_render.get_rect().size

        rect.midtop = self.board_rect.midbottom
        rect.y += DEFAULT_PAD
        self.pos = rect
