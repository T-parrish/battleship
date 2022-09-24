import logging
import random
from ai.agent import BaseAgent
from src import B
from src.validation import OutOfSpaceError, InvalidShipError
from typing import List, Dict, Set
from src.board import PlacedShip

logger = logging.getLogger(__name__)


class NaivePlacementAgent(BaseAgent):
    cache: Set = set()
    ship_opts: List[Dict] = [
        {'type': 'Destroyer', 'size': 2},
        {'type': 'Battleship', 'size': 4},
        {'type': 'Carrier', 'size': 5},
        {'type': 'Submarine', 'size': 3},
        {'type': 'Cruiser', 'size': 3}
    ]

    def __init__(self, board: B, seed: int = None):
        super().__init__(board, seed)

    def _select_ship_type(self) -> Dict:
        # Selects an object containing base ship info by index at random
        target = random.randint(0, len(self.ship_opts)-1)
        return self.ship_opts[target]

    def _make_ship(self, ship_opt: Dict) -> PlacedShip:
        # Creates a ship from the base ship info and some randomness
        dir = random.randint(0, 1)
        start_x = random.randint(0, self.board_ref.board_size-1)
        start_y = random.randint(0, self.board_ref.board_size-1)
        pos = {"x1": 0, "x2": 0, "y1": 0, "y2": 0}

        if dir == 0:
            pos.update({"x1": start_x, "x2": start_x +
                       ship_opt.get("size", 0)-1})
            pos.update({"y1": start_y, "y2": start_y})
        elif dir == 1:
            pos.update({"x1": start_x, "x2": start_x})
            pos.update({"y1": start_y, "y2": start_y +
                       ship_opt.get("size", 0)-1})

        ship = PlacedShip(**ship_opt, **pos)
        return ship

    def deploy_ship(self, count: int = 1):
        '''
        Public function to deploy a ship to the board
            :Param: count: int
                Specifies how many ships to randomly generate and deploy to board
        '''
        for i in range(0, count):
            # Each iteration attempts to build and deploy a ship.
            # if an Error is thrown, each Error class is handled differently.
            while True:
                ship = self._select_ship_type()
                ship = self._make_ship(ship)
                logger.info(f"Created ship: {ship}")
                if ship in self.cache:
                    logger.info("Ship exists in cache... trying again")
                    continue
                self.cache.add(ship)
                try:
                    self.board_ref.place_ship(ship)
                    break
                except ValueError as v_e:
                    logger.warn(v_e)
                # If the ship doesn't fit on the board, break the loop
                except OutOfSpaceError as o_e:
                    logger.warn(o_e)
                    break
                # Shouldn't hit this, but can catch regressions with ship building functions
                except InvalidShipError as i_e:
                    logger.error(i_e)
