'''This module is for tools related to displaying boards.'''


class BoardTextDisplay(object):
    '''I know how to display a board using plain text.'''

    def display_piece(self, piece):
        '''Display a piece as a single character.'''

        if piece is None:
            return ' '

        return piece.symbol

    def display_board(self, board):
        '''Display a board as a table.'''

        x, y = board.dimensions

        header = '-' * (x * 2 + 1)
        lines = [header]

        for j in range(y):
            row_occupants = []
            for i in range(x):
                occupant = board.placements[(i, j)]
                row_occupants.append(occupant)

            line = '|'.join((self.display_piece(occ) for occ in row_occupants))
            line = '|%s|' % line
            lines.append(line)
            lines.append(header)

        block = '\n'.join(lines)
        return block
