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

    def reaches(self):
        raise NotImplementedError


class Bishop(Piece):
    symbol = 'B'

class King(Piece):
    symbol = 'K'

class Knight(Piece):
    symbol = 'N'

class Queen(Piece):
    symbol = 'Q'

class Rook(Piece):
    symbol = 'R'


class Board(object):
    def __init__(self, dimensions, placements=None):
        try:
            x, y = dimensions
        except TypeError:
            raise ValueError("Must pass dimensions as iterable of size two")

        # If we are paced a placements vector we trust the input we receive,
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
