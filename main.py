import logging
import sys
from src.board import Board, PlacedShip
from ai.ship_placement import NaivePlacementAgent
from ai.targeting import NaiveTargetingAgent

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    ships = [
        PlacedShip("Destroyer", 2, 1, 1, 1, 2),
        PlacedShip("Carrier", 5, 4, 1, 4, 5),
        PlacedShip("Cruiser", 3, 6, 5, 8, 5),
        PlacedShip("Submarine", 3, 6, 8, 8, 8),
        PlacedShip("BattleShip", 4, 2, 3, 2, 6)
    ]
    board = Board(8, ships)

    p_agent = NaivePlacementAgent(board)
    p_agent.deploy_ship(count=3)
    logger.info(board)

    t_agent = NaiveTargetingAgent(board)
    t_agent.fire_cannon(count = 12)
    logger.info(board)

