from typing import Generic
from . import S, B


class OutOfSpaceError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidShipError(Exception):
    def __init__(self, message):
        super().__init__(message)


class GameStateValidator(Generic[S, B]):
    def __call__(self, ship: S, board: B) -> bool:
        valid = [self.__validate_open_board_space(ship, board),
                 self.__validate_ship_orientation(ship),
                 self.__validate_ship_bounds(ship, board),
                 self.__validate_ship_overlap(ship, board),
                 self.__validate_ship_format(ship),
                 ]
        return all(valid)

    def __validate_ship_orientation(self, ship: S) -> True:
        if ship.x1 == ship.x2 or ship.y1 == ship.y2:
            return True
        else:
            raise ValueError("Ship must be placed horizontally or vertically")

    def __validate_ship_bounds(self, ship: S, board: B) -> bool:
        if board.board_size < ship.x1 or ship.x1 < 1:
            raise ValueError(
                f"Ship x1 value should be between 1 and {board.board_size}")
        if board.board_size < ship.x2 or ship.x2 < 1:
            raise ValueError(
                f"Ship x2 value should be between 1 and {board.board_size}")
        if board.board_size < ship.y1 or ship.y1 < 1:
            raise ValueError(
                f"Ship y1 value should be between 1 and {board.board_size}")
        if board.board_size < ship.y2 or ship.y2 < 1:
            raise ValueError(
                f"Ship y2 value should be between 1 and {board.board_size}")

        else:
            return True

    def __validate_open_board_space(self, ship: S, board: B) -> bool:
        if ship.size > board.largest_open_space:
            raise OutOfSpaceError(
                f"No room available on board for ship of size {ship.size}")
        else:
            return True

    def __validate_ship_format(self, ship: S) -> bool:
        if ship.x1 > ship.x2 or ship.y1 > ship.y2:
            raise ValueError(
                f"Ship dimensions invalid: make sure x1 <= x2 and y1 <= y2")
        else:
            return True

    def __validate_ship_overlap(self, ship: S, board: B) -> bool:
        # It would be nice to have a method on the Ship object to
        # calculate + store reserved spaces to avoid recomputing 
        reserved_spaces = set()
        for i in range(ship.x1, ship.x2 + 1):
            for j in range(ship.y1, ship.y2 + 1):
                reserved_spaces.add((i, j))

        if len(reserved_spaces) > ship.size:
            raise InvalidShipError(
                "Size of ship not correlated to reserved spaces")

        intersection = board.occupied_spaces.intersection(reserved_spaces)

        if len(intersection) == 0:
            return True
        else:
            raise ValueError(
                f"Overlap detected at {str(intersection)}")
