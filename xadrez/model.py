class Piece(object):
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
        x, y = dimensions
        i, j = cell

        return (
            i < 0 or j < 0 or
            i > (x - 1) or j > (y - 1)
        )

    def filter_inside_board(self, dimensions, cells):
        return [cell for cell in cells
                if not self.is_outside_board(dimensions, cell)]

    def reaches(self, coord, dimensions):
        raise NotImplementedError


def get_bishop_reach(coord, dimensions):
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
    symbol = 'B'

    def reaches(self, coord, dimensions):
        return get_bishop_reach(coord, dimensions)

class King(Piece):
    symbol = 'K'

    def reaches(self, coord, dimensions):
        i, j = coord
        cells = [
            (i-1, j-1), (i, j-1), (i-1, j-1),
            (i-1, j),             (i+1, j),
            (i-1, j+1), (i, j+1), (i+1, j+1),
        ]

        cells = self.filter_inside_board(dimensions, cells)
        return cells

class Knight(Piece):
    symbol = 'N'

    def reaches(self, coord, dimensions):
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
    symbol = 'Q'

    def reaches(self, coord, dimensions):
        bishop_cells = get_bishop_reach(coord, dimensions)
        rook_cells = get_rook_reach(coord, dimensions)
        cells = bishop_cells + rook_cells
        return cells

class Rook(Piece):
    symbol = 'R'

    def reaches(self, coord, dimensions):
        return get_rook_reach(coord, dimensions)


class Board(object):
    def __init__(self, dimensions, placements=None):
        try:
            x, y = dimensions
        except TypeError:
            raise ValueError("Must pass dimensions as iterable of size two")

        # If we are passed a placements vector we trust the input we receive,
        # otherwise we generate an empty one
        if placements is None:
            placements = {}
            for i in range(x):
                for j in range(y):
                    coord = (i, j)
                    placements[coord] = None

        self.dimensions = (x, y)
        self.placements = placements

    def __repr__(self):
        placements = sorted(self.placements.items())
        return '<%s dimensions=%r, placements=%r>' % (
            self.__class__.__name__,
            self.dimensions,
            placements,
        )
