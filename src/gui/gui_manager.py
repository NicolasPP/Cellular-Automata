import pygame

from src.gui.verification_title_gui import VariationTitleGui
from src.gui.cycle_buttons_gui import CycleButtonsGui


class GuiManager:
    def __init__(self, board_rect: pygame.rect.Rect) -> None:
        self.variation_title: VariationTitleGui = VariationTitleGui(board_rect)
        self.cycle_buttons: CycleButtonsGui = CycleButtonsGui(board_rect)

    def draw(self) -> None:
        self.variation_title.draw()
        self.cycle_buttons.draw()
