import logging
from . import V
from .validation import GameStateValidator
from enum import Enum
from typing import List, Dict, NamedTuple, Set, Tuple, Generic

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


class Board(Generic[V]):
    board_size: int
    game_state: List[List[Dict]]
    occupied_spaces: Set[Tuple[int, int]] = set()
    largest_open_space: int
    validator: V

    def __init__(self, board_size: int, current_fleet: List[PlacedShip], validator: V = GameStateValidator) -> None:
        if board_size < 2:
            raise ValueError("Board size must be 2 or larger")
        self.board_size = board_size
        self.validator = validator()
        self.__initialize_board(board_size)

        for ship in current_fleet:
            self.place_ship(ship)

        logger.info(self)

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
        logger.info(f"Placing {ship.type} from x1: {ship.x1} x2: {ship.x2} y1: {ship.y1} y2: {ship.y2}")
        if self.validator(ship, self):
            for i in range(ship.x1, ship.x2 + 1):
                for j in range(ship.y1, ship.y2 + 1):
                    # since everything is 1-indexed from an end user perspective, subtract 1
                    # to fit things into the 0-indexed matrix
                    self.game_state[i-1][j-1] = BoardSpace.SHIP
                    self.occupied_spaces.add((i-1, j-1))

            return True
        else:
            return False
