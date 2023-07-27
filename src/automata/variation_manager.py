from __future__ import annotations
import dataclasses
import json

from automata.cell import Cell
from automata.cell import CellState
from automata.board import Board
from utils.callback_vars import IntCB
from config import BIRTH
from config import DATA
from config import JSON_FILE_MODE
from config import NAME
from config import RULES_JSON
from config import SURVIVAL


@dataclasses.dataclass
class AutomataVariation:
    name: str
    birth: set[int]
    survival: set[int]

    def __eq__(self, other: AutomataVariation) -> bool:
        return self.birth == other.birth and self.survival == other.survival


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
            automata_variation: AutomataVariation = AutomataVariation(variation[NAME], set(variation[BIRTH]),
                                                                      set(variation[SURVIVAL]))
            if automata_variation in VariationManager.variations:
                print(f"variation {automata_variation.name} already exits")
            else:
                VariationManager.variations.append(automata_variation)

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
