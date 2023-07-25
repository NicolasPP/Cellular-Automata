import dataclasses
import json
import typing

from cell import Cell
from cell import CellState
from config import BIRTH
from config import DATA
from config import NAME
from config import RULES_JSON
from config import SURVIVAL
from config import JSON_FILE_MODE


@dataclasses.dataclass
class Rule:
    name: str
    birth: set[int]
    survival: set[int]


class Rules:
    rules: list[Rule] = []
    index: int = 0

    @staticmethod
    def load_rules() -> None:
        with open(RULES_JSON, JSON_FILE_MODE) as rules_file:
            rules = json.load(rules_file)

        for rule in rules[DATA]:
            print(rule[NAME])
            Rules.rules.append(Rule(rule[NAME], set(rule[BIRTH]), set(rule[SURVIVAL])))

        print(Rules.get_current_rule().name)

    @staticmethod
    def get_current_rule() -> Rule:
        if len(Rules.rules) == 0: raise Exception("no rules loaded")
        return Rules.rules[Rules.index % len(Rules.rules)]

    @staticmethod
    def cycle(direction) -> None:
        Rules.index += (1 * direction)
        print(Rules.get_current_rule().name)

    @staticmethod
    def get_cells_to_change(board: list[list[Cell]]) -> list[Cell]:
        cells_to_change: list[Cell] = []
        possible_neighbour_count: set[int] = set(range(9))
        rule = Rules.get_current_rule()

        def check_rule(desired_values: set[int], alive_count: int, current_cell: Cell) -> None:
            for value in desired_values:
                if alive_count == value:
                    cells_to_change.append(current_cell)
                    return

        for cell, alive_neighbours in board_it(board):

            if cell.state == CellState.DEAD:
                check_rule(rule.birth, alive_neighbours, cell)

            elif cell.state == CellState.ALIVE:
                check_rule(possible_neighbour_count - rule.survival, alive_neighbours, cell)

        return cells_to_change


def get_alive_neighbours_count(cell: Cell, board: list[list[Cell]]) -> int:
    alive_neighbour_count: int = 0
    for index in cell.neighbours:
        x, y = index
        if board[y][x].state is CellState.ALIVE:
            alive_neighbour_count += 1
    return alive_neighbour_count


def board_it(board: list[list[Cell]]) -> typing.Generator[tuple[Cell, int], None, None]:
    for board_row in board:
        for cell in board_row:
            yield cell, get_alive_neighbours_count(cell, board)
