import unittest
import logging
from board import Board, OutOfSpaceError, PlacedShip

class BoardTests(unittest.TestCase):
    def test_board_setup_exception(self):
        with self.assertRaises(ValueError) as ctx:
            _ = Board(1, [])
        self.assertEqual(str(ctx.exception), "Board size must be 2 or larger")

    def test_board_setup_success(self):
        board = Board(2, [])
        self.assertEqual(board._pretty_state(), [[" ", " "], [" ", " "]])
        board = Board(4, [])
        
        self.assertEqual(board._pretty_state(), [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]])

    def test_diagonal_boat(self):
        with self.assertRaises(ValueError) as ctx:
            board = Board(4, [])
            ship = PlacedShip("frigate", 2, 0, 1, 1, 2)
            board.place_ship(ship)
        
        self.assertEqual(str(ctx.exception), "Ship must be placed horizontally or vertically")

    def test_boat_out_of_bounds(self):
        with self.assertRaises(ValueError) as ctx:
            board = Board(4, [])
            ship = PlacedShip("frigate", 2, 0, 7, 0, 5)
            board.place_ship(ship)

    def test_valid_boat(self):
        board = Board(4, [])
        ship = PlacedShip("frigate", 2, 1, 1, 1, 2)
        self.assertTrue(board.place_ship(ship))
        
        board = Board(4, [])
        ship = PlacedShip("frigate", 2, 2, 3, 2, 4)
        self.assertTrue(board.place_ship(ship))
        
        board = Board(4, [])
        ship = PlacedShip("frigate", 3, 1, 1, 4, 1)
        self.assertTrue(board.place_ship(ship))

    def test_overlapping_boat(self):
        with self.assertRaises(ValueError) as ctx:
            board = Board(4, [])
            board.occupied_spaces = {(1, 1), (1, 2)}
            ship = PlacedShip("frigate", 2, 1, 1, 1, 2)
            board.place_ship(ship)
        self.assertEqual(str(ctx.exception), "Overlap detected at {(1, 1), (1, 2)}")

    def test_no_board_space(self):
        with self.assertRaises(OutOfSpaceError) as ctx:
            board = Board(4, [])
            board.largest_open_space = 1
            ship = PlacedShip("frigate", 2, 1, 1, 1, 2)
            board.place_ship(ship)
        self.assertEqual(str(ctx.exception), "No room available on board for ship of size 2")

        

