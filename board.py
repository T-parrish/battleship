import logging
from enum import Enum
from typing import List, Dict, NamedTuple, Set, Tuple

logger = logging.getLogger(__name__)


class PlacedShip(NamedTuple):
    type: str
    size: int
    x1: int
    y1: int
    x2: int
    y2: int


class BoardSpace(Enum):
    EMPTY = " "
    SHIP = "O"
    HIT = "X"


class OutOfSpaceError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Board:
    board_size: int
    game_state: List[List[Dict]]
    occupied_spaces: Set[Tuple[int, int]] = set()
    largest_open_space: int

    def __init__(self, board_size: int, current_fleet: List[PlacedShip]) -> None:
        if board_size < 2:
            raise ValueError("Board size must be 2 or larger")
        self.board_size = board_size
        self.__initialize_board(board_size)

        map(lambda x: self.place_ship(x), current_fleet)

    def __str__(self) -> str:
        state = [str([f"{cell.value}" for cell in row])
                 for row in self.game_state]
        msg = "Current board state:\n"+"\n".join(state)
        return msg

    def _pretty_state(self) -> str:
        return [[f"{cell.value}" for cell in row]
                for row in self.game_state]

    def __initialize_board(self, board_size: int) -> None:
        logger.info(
            f"Initializing board with dimensions: {board_size} x {board_size}")
        self.game_state = [
            [BoardSpace.EMPTY for i in range(0, board_size)] for j in range(0, board_size)]

        # Before placing any boats, can assume the longest contiguous block of
        # empty cells to be == the size of the board
        self.largest_open_space = board_size

    def place_ship(self, ship: PlacedShip) -> bool:
        valid = [self.__validate_open_board_space(ship),
                 self.__validate_ship_orientation(ship),
                 self.__validate_ship_bounds(ship),
                 self.__validate_ship_overlap(ship),
                 self.__validate_ship_format(ship),
                 ]
        return all(valid)


    def __validate_ship_orientation(self, ship: PlacedShip) -> True:
        if ship.x1 == ship.x2 or ship.y1 == ship.y2:
            return True
        else:
            raise ValueError("Ship must be placed horizontally or vertically")

    def __validate_ship_bounds(self, ship: PlacedShip) -> bool:
        if self.board_size < ship.x1 or ship.x1 < 1:
            raise ValueError(
                f"Ship x1 value should be between 1 and {self.board_size}")
        if self.board_size < ship.x2 or ship.x2 < 1:
            raise ValueError(
                f"Ship x2 value should be between 1 and {self.board_size}")
        if self.board_size < ship.y1 or ship.y1 < 1:
            raise ValueError(
                f"Ship y1 value should be between 1 and {self.board_size}")
        if self.board_size < ship.y2 or ship.y2 < 1:
            raise ValueError(
                f"Ship y2 value should be between 1 and {self.board_size}")

        else:
            return True

    def __validate_open_board_space(self, ship: PlacedShip) -> bool:
        if ship.size > self.largest_open_space:
            raise OutOfSpaceError(f"No room available on board for ship of size {ship.size}")
        else:
            return True

    def __validate_ship_format(self, ship: PlacedShip) -> bool:
        if ship.x1 > ship.x2 or ship.y1 > ship.y2:
            raise ValueError(
                f"Ship dimensions invalid: make sure x1 <= x2 and y1 <= y2")
        else:
            return True

    def __validate_ship_overlap(self, ship: PlacedShip) -> bool:
        reserved_spaces = set()
        for i in range(ship.x1, ship.x2 + 1):
            for j in range(ship.y1, ship.y2 + 1):
                reserved_spaces.add((i, j))

        intersection = self.occupied_spaces.intersection(reserved_spaces)
        if len(intersection) == 0:
                return True
        else:
            raise ValueError(
                f"Overlap detected at {str(intersection)}")