import dataclasses
import json

from src.automata.cell import Cell
from src.automata.cell import CellState
from src.automata.board import Board
from src.utils.callback_vars import IntCB
from src.config import BIRTH
from src.config import DATA
from src.config import JSON_FILE_MODE
from src.config import NAME
from src.config import RULES_JSON
from src.config import SURVIVAL


@dataclasses.dataclass
class AutomataVariation:
    name: str
    birth: set[int]
    survival: set[int]


class VariationManager:
    variations: list[AutomataVariation] = []
    index: IntCB = IntCB(0)

    @staticmethod
    def get_index() -> IntCB:
        return VariationManager.index

    @staticmethod
    def load_rules() -> None:
        with open(RULES_JSON, JSON_FILE_MODE) as variation_file:
            variations = json.load(variation_file)

        for variation in variations[DATA]:
            VariationManager.variations.append(
                AutomataVariation(variation[NAME], set(variation[BIRTH]), set(variation[SURVIVAL]))
            )

    @staticmethod
    def get_current_variation() -> AutomataVariation:
        if len(VariationManager.variations) == 0: raise Exception("no rules loaded")
        return VariationManager.variations[VariationManager.get_index().get() % len(VariationManager.variations)]

    @staticmethod
    def cycle(direction) -> None:
        VariationManager.index.set(VariationManager.get_index().get() + (1 * direction))

    @staticmethod
    def get_cells_to_change(board: Board) -> list[Cell]:
        cells_to_change: list[Cell] = []
        possible_neighbour_count: set[int] = set(range(9))
        variation = VariationManager.get_current_variation()

        def check_rule(desired_values: set[int], alive_count: int, current_cell: Cell) -> None:
            for value in desired_values:
                if alive_count == value:
                    cells_to_change.append(current_cell)
                    return

        for cell in board.cells_gen():
            alive_neighbours: int = board.get_alive_neighbours_count(cell)

            if cell.state == CellState.DEAD:
                check_rule(variation.birth, alive_neighbours, cell)

            elif cell.state == CellState.ALIVE:
                check_rule(possible_neighbour_count - variation.survival, alive_neighbours, cell)

        return cells_to_change
