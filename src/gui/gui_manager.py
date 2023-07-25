import pygame

from gui.board_control_gui import BoardControlGui
from gui.cycle_buttons_gui import CycleButtonsGui
from gui.iteration_count_gui import IterationCountGui
from gui.iteration_speed_gui import IterationSpeedGui
from gui.play_button_gui import PlayButtonGui
from gui.variation_title_gui import VariationTitleGui
from utils.callback_vars import BoolCB


class GuiManager:
    def __init__(self, board_rect: pygame.rect.Rect, iterate_board: BoolCB) -> None:
        self.variation_title: VariationTitleGui = VariationTitleGui(board_rect)
        self.cycle_buttons: CycleButtonsGui = CycleButtonsGui(board_rect)
        self.iteration_count: IterationCountGui = IterationCountGui(board_rect)
        self.iteration_speed: IterationSpeedGui = IterationSpeedGui(board_rect)
        self.board_control: BoardControlGui = BoardControlGui(board_rect)
        self.play_button: PlayButtonGui = PlayButtonGui(board_rect, iterate_board)

    def draw(self) -> None:
        self.variation_title.draw()
        self.cycle_buttons.draw()
        self.iteration_count.draw()
        self.iteration_speed.draw()
        self.board_control.draw()
        self.play_button.draw()
