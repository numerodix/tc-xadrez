'''This module contains a model of a chess board and its pieces.'''


class ConflictError(Exception):
    '''I am intended to be used to indicate that two pieces on a board conflict
    with each other.'''
    pass


class Piece(object):
    '''I represent an abstract piece on a board - I am not intended to be
    instantiated directly.'''

    symbol = None

    def __repr__(self):
        return '<%s symbol=%r>' % (
            self.__class__.__name__,
            self.symbol,
        )

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
        )

    def is_outside_board(self, dimensions, cell):
        '''Check whether the given cell falls outside the board given the
        dimensions.'''

        x, y = dimensions
        i, j = cell

        return (
            i < 0 or j < 0 or
            i > (x - 1) or j > (y - 1)
        )

    def filter_inside_board(self, dimensions, cells):
        '''Filter out `cells` that fall outside the board given the
        `dimensions`.'''

        return [cell for cell in cells
                if not self.is_outside_board(dimensions, cell)]

    def reaches(self, coord, dimensions):
        '''Compute all cells that are reachable by the piece (excluding the
        cell the piece itself occupies).'''

        raise NotImplementedError


def get_bishop_reach(coord, dimensions):
    '''Compute the reach of a bishop.'''

    i, j = coord
    x, y = dimensions

    cells = []

    # from coord to top left
    zx, zy = i - 1, j - 1
    while zx > -1 and zy > -1:
        cells.append((zx, zy))

        zx -= 1
        zy -= 1

    # from coord to top right
    zx, zy = i + 1, j - 1
    while zx < x and zy > -1:
        cells.append((zx, zy))

        zx += 1
        zy -= 1

    # from coord to bottom left
    zx, zy = i - 1, j + 1
    while zx > -1 and zy < y:
        cells.append((zx, zy))

        zx -= 1
        zy += 1

    # from coord to bottom right
    zx, zy = i + 1, j + 1
    while zx < x and zy < y:
        cells.append((zx, zy))

        zx += 1
        zy += 1

    return cells


def get_rook_reach(coord, dimensions):
    '''Compute the reach of a rook.'''

    i, j = coord
    x, y = dimensions

    cells = []

    # horizontal
    for zx in range(x):
        if zx != i:
            cells.append((zx, j))

    # vertical
    for zy in range(y):
        if zy != j:
            cells.append((i, zy))

    return cells


class Bishop(Piece):
    '''I represent a bishop piece on a board.'''

    symbol = 'B'

    def reaches(self, coord, dimensions):
        return get_bishop_reach(coord, dimensions)


class King(Piece):
    '''I represent a king piece on a board.'''

    symbol = 'K'

    def reaches(self, coord, dimensions):
        # pylint: disable=bad-whitespace

        i, j = coord
        cells = [
            (i-1, j-1), (i, j-1), (i-1, j-1),
            (i-1, j),             (i+1, j),
            (i-1, j+1), (i, j+1), (i+1, j+1),
        ]

        cells = self.filter_inside_board(dimensions, cells)
        return cells


class Knight(Piece):
    '''I represent a knight piece on a board.'''

    symbol = 'N'

    def reaches(self, coord, dimensions):
        # pylint: disable=bad-continuation
        # pylint: disable=bad-whitespace

        i, j = coord
        cells = [
                        (i-1, j-2),         (i+1, j-2),
            (i-2, j-1),                                  (i+2, j-1),

            (i-2, j+1),                                  (i+2, j+1),
                        (i-1, j+2),         (i+1, j+2),
        ]

        cells = self.filter_inside_board(dimensions, cells)
        return cells


class Queen(Piece):
    '''I represent a queen piece on a board.'''

    symbol = 'Q'

    def reaches(self, coord, dimensions):
        bishop_cells = get_bishop_reach(coord, dimensions)
        rook_cells = get_rook_reach(coord, dimensions)
        cells = bishop_cells + rook_cells
        return cells


class Rook(Piece):
    '''I represent a rook piece on a board.'''

    symbol = 'R'

    def reaches(self, coord, dimensions):
        return get_rook_reach(coord, dimensions)


class Board(object):
    '''I represent a chess board with dimensions (x, y) and placements of
    pieces on the board.'''

    def __init__(self, dimensions, placements=None, backfill_placements=True):
        try:
            x, y = dimensions
        except TypeError:
            raise ValueError("Must pass dimensions as iterable of size two")

        # If we are passed a placements vector we trust the input we receive,
        # otherwise we generate an empty one
        empty_placements = False
        if placements is None:
            empty_placements = True
            placements = {}
            for i in range(x):
                for j in range(y):
                    coord = (i, j)
                    placements[coord] = None

        # If the collection of placements passed was incomplete let's back fill
        # it (no need if we just generated them all in the previous step though)
        if not empty_placements and backfill_placements:
            for i in range(x):
                for j in range(y):
                    coord = (i, j)
                    if coord not in placements:
                        placements[coord] = None

        # TODO: should probably check that all placements are actually on the board

        # Build an index on pieces because it's useful to have easy access to
        # them
        piece_index = {}
        for coord, piece in placements.items():
            if piece is not None:
                piece_index[piece] = coord

        self.dimensions = (x, y)
        self.placements = placements
        self.piece_index = piece_index

    def __repr__(self):
        placements = sorted(self.placements.items())
        return '<%s dimensions=%r, placements=%r>' % (
            self.__class__.__name__,
            self.dimensions,
            placements,
        )

    def check_valid(self):
        '''Check the board for validity. If the board is valid that means no
        piece on the board can reach any other piece. Raises ConflictError if
        validity does not hold.'''

        # For each piece get its coordinates
        for piece, coord in self.piece_index.items():

            # Compute the cells it reaches
            cells = piece.reaches(coord, self.dimensions)

            # Iterate over these cells
            for cell in cells:

                # If the cell (which this piece can reach) matches one of the
                # coordinates of the pieces on the board we have a conflict.
                # Note that it's safe to include the current piece's
                # coordinates, because those will always be excluded from its
                # own reach.
                reachable_piece = self.placements.get(cell)
                if reachable_piece is not None:
                    raise ConflictError(
                        (
                            "Overlap detected at %s: "
                            "contains piece %s "
                            "and is reachable by %s at %s"
                        ) % (
                            repr(cell),
                            reachable_piece.__class__.__name__,
                            piece.__class__.__name__,
                            coord,
                        )
                    )
