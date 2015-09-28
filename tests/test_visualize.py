from unittest import TestCase

from xadrez.model import Bishop
from xadrez.model import Board
from xadrez.model import King
from xadrez.model import Knight
from xadrez.model import Queen
from xadrez.model import Rook
from xadrez.visualize import BoardTextDisplay


BOARD_2x2_EMPTY = '''
-----
| | |
-----
| | |
-----
'''.strip()

BOARD_3x2_FULL = '''
-------
|K|B|R|
-------
|Q|Q|N|
-------
'''.strip()


class BoardTextDisplayTests(TestCase):
    def test_2x2_empty(self):
        board = Board(dimensions=(2, 2))
        display = BoardTextDisplay()

        assert display.display_board(board) == BOARD_2x2_EMPTY

    def test_3x2_full(self):
        board = Board(
            dimensions=(3, 2),
            placements={
                (0, 0): King(),
                (1, 0): Bishop(),
                (2, 0): Rook(),
                (0, 1): Queen(),
                (1, 1): Queen(),
                (2, 1): Knight(),
            },
        )
        display = BoardTextDisplay()

        assert display.display_board(board) == BOARD_3x2_FULL
