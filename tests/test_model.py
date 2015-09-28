from unittest import TestCase

from xadrez.model import Board
from xadrez.model import Piece
from xadrez.model import King
from xadrez.model import Rook


class PieceTests(TestCase):
    def test_piece_creation(self):
        king = King()
        king2 = King()
        rook = Rook()

        # two pieces are equal if of the same class
        assert king == king2

        # otherwise not
        assert king != rook


class ModelTests(TestCase):
    def test_board_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            Board(dimensions=tuple())

        with self.assertRaises(ValueError):
            Board(dimensions=(4,))

        with self.assertRaises(ValueError):
            Board(dimensions=(4, 4, 4))

    def test_board_creation_empty(self):
        board = Board(dimensions=(2, 2))

        assert board.dimensions == (2, 2)
        assert board.placements == {
            (0, 0): None,
            (0, 1): None,
            (1, 0): None,
            (1, 1): None,
        }

    def test_board_creation_non_empty(self):
        king = King()
        rook = Rook()

        board = Board(
            dimensions=(2, 2),
            placements={
                (0, 0): king,
                (0, 1): None,
                (1, 0): rook,
                (1, 1): None,
            },
        )

        assert board.dimensions == (2, 2)
        assert board.placements == {
            (0, 0): king,
            (0, 1): None,
            (1, 0): rook,
            (1, 1): None,
        }
