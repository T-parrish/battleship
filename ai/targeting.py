import logging
import random
from typing import NamedTuple, List, Tuple, Set
from ai.agent import BaseAgent
from src import B

logger = logging.getLogger(__name__)

class AllBombedError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Bombs(NamedTuple):
    x: int
    y: int
    hit: bool
    sunk: bool

class SuggestedBomb(NamedTuple):
    x: int
    y: int


class NaiveTargetingAgent(BaseAgent):
    # Precomputed list of all (x, y) coordinate tuples for a given M x N matrix
    cell_opts: List[Tuple[int, int]] = list()
    hits: List[Bombs] = list()
    cache: Set = set()

    def __init__(self, board: B, seed: int = None):
        super().__init__(board, seed)
        # Precompute all possible grid targets on agent initialization
        for i in range(0, board.board_size):
            for j in range(0, board.board_size):
                self.cell_opts.append((i, j))

    def fire_cannon(self, count:int = 1):
        for _ in range(0, count):
            bomb = self.__suggest_bomb()
            if self.board_ref.log_hit(bomb):
                logger.info(f"Bomb hits at x: {bomb.x+1} y: {bomb.y+1}")
                self.hits.append(Bombs(x=bomb.x, y=bomb.y, hit=True, sunk=False))
            else:
                logger.info(f"Bomb miss at x: {bomb.x+1} y: {bomb.y+1}")


    def __suggest_bomb(self) -> SuggestedBomb:
        # Until all grid targets have been used, yield a new index at every loop
        while len(self.cache) < len(self.cell_opts):
            guess = random.randint(0, len(self.cell_opts)-1)
            if guess in self.cache:
                continue
            else:
                # when random returns an un-used (x,y) coordinate tuple, add
                # it to the cache and return a SuggestedBomb
                self.cache.add(guess)
                return SuggestedBomb(self.cell_opts[guess][0], self.cell_opts[guess][1])
        
        # If every option has been exhausted, throw an error
        raise AllBombedError("All spaces have been bombed, no moves left")
        

            
        

