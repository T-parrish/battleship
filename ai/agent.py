import logging
from typing import Generic, Set, Optional
from src import B

import random

logger = logging.getLogger(__name__)


class BaseAgent(Generic[B]):
    '''
    Base Type for AI agents, makes it fairly simple for all subclasses to hold 
    references to the same Generic Board object. 
    '''
    board_ref: B

    def __init__(self, board: B, seed: Optional[int] = None):
        self.board_ref = board
        if seed is not None:
            # allows us to configure our agents for 'deterministic' randomization
            random.seed(seed)
