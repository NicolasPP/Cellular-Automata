import pygame

from src.gui.veriation_title import VariationTitleGui


class GuiManager:
    def __init__(self, board_rect: pygame.rect.Rect) -> None:
        self.variation_title: VariationTitleGui = VariationTitleGui(board_rect)

    def draw(self) -> None:
        self.variation_title.draw()
