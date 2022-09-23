# We’ll need a Python AI module that has functions to do two things: 
# 1) place the bot’s ships on the gameboard
# 2) choose where to launch the next bomb when it’s the bot’s turn.
import logging
import sys
from board import Board

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    board = Board(4, [])

    logger.info(board)