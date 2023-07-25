import pygame

from gui.variation_title_gui import VariationTitleGui
from gui.cycle_buttons_gui import CycleButtonsGui
from gui.iteration_count_gui import IterationCountGui


class GuiManager:
    def __init__(self, board_rect: pygame.rect.Rect) -> None:
        self.variation_title: VariationTitleGui = VariationTitleGui(board_rect)
        self.cycle_buttons: CycleButtonsGui = CycleButtonsGui(board_rect)
        self.iteration_count: IterationCountGui = IterationCountGui(board_rect)

    def draw(self) -> None:
        self.variation_title.draw()
        self.cycle_buttons.draw()
        self.iteration_count.draw()
