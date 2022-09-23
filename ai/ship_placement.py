"""
Write a function to choose a placement for a ship of a given size, 
given the dimensions of the gameboard and a list of ships that have already been placed.
    1. The x1 and x2 coordinates should be between 1 and the board width.
    2. The y1 and y2 coordinates should be between 1 and the board height.
    3. Ships are placed either horizontally or vertically - i.e. either x1 == x2 or y1 == y2.
    4. Ships must not overlap existing ships.
    5. Ships placements should ensure that x1 <= x2 and y1 <= y2
    6. Throw an error if there is no available placement
""" 

from typing import NamedTuple

class PlacedShip(NamedTuple):
    type: str
    size: int
    x1: int
    y1: int
    x2: int
    y2: int

