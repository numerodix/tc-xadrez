from unittest import TestCase

from xadrez.model import Bishop
from xadrez.model import Board
from xadrez.model import ConflictError
from xadrez.model import King
from xadrez.model import Knight
from xadrez.model import Piece
from xadrez.model import Queen
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

    def test_filter_outside_board(self):
        piece = Piece()
        dimensions = (2, 3)

        assert piece.is_outside_board(dimensions, (-1, -1)) is True
        assert piece.is_outside_board(dimensions, (0, -1)) is True
        assert piece.is_outside_board(dimensions, (-1, 0)) is True

        assert piece.is_outside_board(dimensions, (0, 0)) is False
        assert piece.is_outside_board(dimensions, (1, 0)) is False
        assert piece.is_outside_board(dimensions, (0, 1)) is False
        assert piece.is_outside_board(dimensions, (1, 1)) is False
        assert piece.is_outside_board(dimensions, (0, 2)) is False
        assert piece.is_outside_board(dimensions, (1, 2)) is False

        assert piece.is_outside_board(dimensions, (2, 0)) is True
        assert piece.is_outside_board(dimensions, (2, 1)) is True
        assert piece.is_outside_board(dimensions, (2, 2)) is True
        assert piece.is_outside_board(dimensions, (2, 3)) is True
        assert piece.is_outside_board(dimensions, (3, 3)) is True


__TEMPLATE = '''
(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
(0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
(0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
(0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
(0, 4), (1, 4), (2, 4), (3, 4), (4, 4),
'''


class BoardTests(TestCase):
    def test_board_creation_invalid(self):
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
        assert board.piece_index == {}

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
        assert board.piece_index == {
            king: (0, 0),
            rook: (1, 0),
        }


    def test_bishop_reach(self):
        bishop = Bishop()
        dimensions = (5, 5)

        cells = bishop.reaches((2, 2), dimensions)
        assert sorted(cells) == sorted([
            (0, 0),                         (4, 0),
                    (1, 1),         (3, 1),

                    (1, 3),         (3, 3),
            (0, 4),                         (4, 4),
        ])

    def test_king_reach(self):
        king = King()
        dimensions = (3, 3)

        cells = king.reaches((1, 0), dimensions)
        assert sorted(cells) == sorted([
            (0, 0),         (2, 0),
            (0, 1), (1, 1), (2, 1),
        ])

    def test_knight_reach(self):
        knight = Knight()
        dimensions = (5, 5)

        cells = knight.reaches((2, 2), dimensions)
        assert sorted(cells) == sorted([
                    (1, 0),         (3, 0),
            (0, 1),                         (4, 1),

            (0, 3),                         (4, 3),
                    (1, 4),         (3, 4),
        ])

    def test_queen_reach(self):
        queen = Queen()
        dimensions = (5, 5)

        cells = queen.reaches((2, 2), dimensions)
        assert sorted(cells) == sorted([
            (0, 0),         (2, 0),         (4, 0),
                    (1, 1), (2, 1), (3, 1),
            (0, 2), (1, 2),         (3, 2), (4, 2),
                    (1, 3), (2, 3), (3, 3),
            (0, 4),         (2, 4),         (4, 4),
        ])

    def test_rook_reach(self):
        rook = Rook()
        dimensions = (5, 5)

        cells = rook.reaches((2, 2), dimensions)
        assert sorted(cells) == sorted([
                            (2, 0),
                            (2, 1),
            (0, 2), (1, 2),         (3, 2), (4, 2),
                            (2, 3),
                            (2, 4),
        ])


    def test_check_valid_adjacent(self):
        board = Board(
            dimensions=(2, 1),
            placements={
                (0, 0): Rook(),
                (1, 0): King(),
            },
        )

        with self.assertRaises(ConflictError) as cm:
            board.check_valid()

        exc = cm.exception
        assert exc.message == 'Overlap detected at (1, 0): contains piece King and is reachable by Rook at (0, 0)'

    def test_check_valid_no_conflict(self):
        board = Board(
            dimensions=(3, 1),
            placements={
                (0, 0): King(),
                (1, 0): None,
                (2, 0): King(),
            },
        )

        # does not raise
        board.check_valid()
