import logging

from ai.targeting import SuggestedBomb
from . import V
from .validation import GameStateValidator
from enum import Enum
from typing import List, Dict, NamedTuple, Set, Tuple, Generic
import itertools

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
    MISS = "-"


class Board(Generic[V]):
    board_size: int  # size of board matrix ie board_size X board_size
    game_state: List[List[BoardSpace]]  # tracks state of each cell in the board matrix
    occupied_spaces: Set[Tuple[int, int]]  # set of Tuples to keep track of occupied spaces
    largest_open_space: int  # longest contiguous block of EMPTY cells by row and column
    validator: V  # Generic Validator type

    def __init__(self, board_size: int, current_fleet: List[PlacedShip], validator: V = GameStateValidator) -> None:
        if board_size < 2:
            raise ValueError("Board size must be 2 or larger")
        self.board_size = board_size
        self.occupied_spaces = set()  # Guarantee idempotency between board instantiations
        self.validator = validator()
        self.__initialize_board(board_size)

        for ship in current_fleet:
            self.place_ship(ship)

        logger.info(self)

    def __str__(self) -> str:
        state = [str([f"{cell.value}" for cell in row])
                 for row in self.game_state]
        msg = "Current board state:\n"+"\n".join(state[::-1])
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
        logger.info(
            f"Placing {ship.type} from x1: {ship.x1} x2: {ship.x2} y1: {ship.y1} y2: {ship.y2}")
        
        # Validator always returns True or throws an Exception 
        if self.validator(ship, self):
            for y in range(ship.y1, ship.y2 + 1):
                for x in range(ship.x1, ship.x2 + 1):
                    # since everything is 1-indexed from an end user perspective, subtract 1
                    # to fit things into the 0-indexed matrix
                    self.game_state[y-1][x-1] = BoardSpace.SHIP
                    self.occupied_spaces.add((x, y))

            self.__update_open_space()
            return True
        else:
            return False

    def log_hit(self, bomb: SuggestedBomb) -> bool:
        x = bomb.x
        y = bomb.y

        # Occupied spaces are 1-indexed whereas bomb coordinates are 0-indexed
        if (x+1, y+1) in self.occupied_spaces:
            self.game_state[y][x] = BoardSpace.HIT
            return True
        else:
            self.game_state[y][x] = BoardSpace.MISS
            return False


    def __update_open_space(self):
        max_x = 0
        max_y = 0
        for row in self.game_state:
            x_groups = itertools.groupby(row, lambda x: x.value)
            for k, g in x_groups:
                if k == BoardSpace.EMPTY.value:
                    max_x = max(max_x, len(list(g)))

        cols = [[row[i] for row in self.game_state]
                for i in range(0, self.board_size)]
                
        for col in cols:
            y_groups = itertools.groupby(col, lambda x: x.value)
            for k, g in y_groups:
                if k == BoardSpace.EMPTY.value:
                    max_y = max(max_y, len(list(g)))

        self.largest_open_space = max(max_x, max_y)
        logger.info(f"Largest open space: {self.largest_open_space}")