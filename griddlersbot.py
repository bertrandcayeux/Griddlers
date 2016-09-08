import griddlersdisplay as gdisp
import griddlersrules as grules
import pygame

class Bot:

    def __init__(self, displayed_board):

        self.displayed_board = displayed_board
        self.board = displayed_board.board

        # self.self.board.row_clues = self.board.self.board.row_clues
        # self.self.board.column_clues = self.board.self.board.column_clues

        self.board_width = displayed_board.board_width
        self.board_height = displayed_board.board_height

        # self.board.state = [[grules.UNDEFINED
        #                     for y in range(self.board_height)]
        #                     for x in range(self.board_width)]
        self.reinit_board()

        self.history = []

    def __call__(self):
        self.bot()

    def reinit_board(self):
        self.board.state = [[grules.UNDEFINED
                            for y in range(self.board_height)]
                            for x in range(self.board_width)]
        self.board.validated_rows = [False for i in range(self.board_height)]
        self.board.validated_columns = [False for i in range(self.board_width)]
        self.displayed_board.draw_board()
        pygame.display.update()


    def bot(self):
        self.reinit_board()

        fits_r = [ [list(sRow) for sRow in fit(row, self.board_height)] for row in self.board.row_clues ]
        fits_c = [ [list(sCol) for sCol in fit(col, self.board_height)] for col in self.board.column_clues ]
        # fits = [fits_r, fits_c]
        # row_col = 0 # current index into fits; 0 = row, 1 = column



        while not self.board.check_win():
            didNothing = True

            # rows treatment
            for rowIndex, row in enumerate(fits_r):
                # already validated row case
                if self.board.validated_rows[rowIndex]:
                    for i in range(self.board_width):
                        if self.board.state[i][rowIndex] == grules.UNDEFINED:
                            #
                            #
                            self.board.state[i][rowIndex] = grules.EMPTY
                            self.history.append((i, rowIndex, grules.EMPTY))
                            didNothing = False
                    continue
                # remove not viable candidates
                candidatesToRemove = []
                for candidate in row:
                    for i in range(self.board_width):
                        if self.board.state[i][rowIndex] == grules.FILLED and candidate[i] != grules.FILLED:
                            candidatesToRemove.append(candidate)
                            # row.remove(candidate)
                            didNothing = False
                            break
                        if self.board.state[i][rowIndex] == grules.EMPTY and candidate[i] != grules.EMPTY:
                            candidatesToRemove.append(candidate)
                            # row.remove(candidate)
                            didNothing = False
                            break
                for c in candidatesToRemove:
                    row.remove(c)

                assert row, "il n'y a plus de candidat..."

                # if only one candidate left
                if len(row) == 1:
                    didNothing = False
                    for i in range(self.board_width):
                        #
                        #
                        if self.board.state[i][rowIndex] == grules.UNDEFINED:
                            self.board.state[i][rowIndex] = row[0][i]
                            self.history.append((i, rowIndex, row[0][i]))

                # else put definitive blocks
                for i in range(self.board_width):
                    definitiveBlock = True
                    for j in range(1, len(row)):
                        if row[0][i] != row[j][i] or row[0][i] == self.board.state[i][rowIndex]:
                            definitiveBlock = False
                            break
                    if definitiveBlock:
                        didNothing = False
                        #
                        #
                        if self.board.state[i][rowIndex] == grules.UNDEFINED:
                            self.board.state[i][rowIndex] = row[0][i]
                            self.history.append((i, rowIndex, row[0][i]))

            self.board.check_filled_lines()

            # cols treatment
            for colIndex, col in enumerate(fits_c):
                # already validated row case + replace UNKNOWS by EMPTYS
                if self.board.validated_columns[colIndex]:
                    for i in range(self.board_height):
                        if self.board.state[colIndex][i] == grules.UNDEFINED:
                            #
                            #
                            self.board.state[colIndex][i] = grules.EMPTY
                            self.history.append((colIndex, i, grules.EMPTY))
                            didNothing = False
                    continue
                # remove not viable candidates
                candidatesToRemove = []
                for candidate in col:
                    for i in range(self.board_height):
                        if self.board.state[colIndex][i] == grules.FILLED and candidate[i] != grules.FILLED:
                            candidatesToRemove.append(candidate)
                            # row.remove(candidate)
                            didNothing = False
                            break
                        if self.board.state[colIndex][i] == grules.EMPTY and candidate[i] != grules.EMPTY:
                            candidatesToRemove.append(candidate)
                            # row.remove(candidate)
                            didNothing = False
                            break
                for c in candidatesToRemove:
                    col.remove(c)

                assert col, "il n'y a plus de candidat..."

                # if only one candidate left
                if len(col) == 1:
                    didNothing = False
                    for i in range(self.board_height):
                        #
                        #
                        if self.board.state[colIndex][i] == grules.UNDEFINED:
                            self.board.state[colIndex][i] = col[0][i]
                            self.history.append((colIndex, i, col[0][i]))

                # else put definitive blocks
                for i in range(self.board_height):
                    definitiveBlock = True
                    for j in range(1, len(col)):
                        if col[0][i] != col[j][i] or col[0][i] == self.board.state[colIndex][i]:
                            definitiveBlock = False
                            break
                    if definitiveBlock:
                        didNothing = False
                        #
                        #
                        if self.board.state[colIndex][i] == grules.UNDEFINED:
                            self.board.state[colIndex][i] = col[0][i]
                            self.history.append((colIndex, i, col[0][i]))

            self.board.check_filled_lines()

            if didNothing:
                break

        self.board.state = [[grules.UNDEFINED
                            for y in range(self.board_height)]
                            for x in range(self.board_width)]

def min_width(blocks):
    """The minimum width into which the supplied blocks will fit

    e.g. min_width([1,2,3]) = 8
    """
    assert(len(blocks) > 0)
    return sum(blocks) + len(blocks) - 1



def fit(blocks, size):
    """Return all possible ways of fitting the supplied blocks into the
    supplied size.
    """
    assert(len(blocks) > 0)
    assert(size >= min_width(blocks))
    if len(blocks) == 1:
        return [grules.EMPTY * i + grules.FILLED * blocks[0] + grules.EMPTY * (size - blocks[0] - i) \
                for i in range(size - blocks[0] + 1)]
    else:
        return [grules.EMPTY * (i - blocks[0]) + grules.FILLED * blocks[0] + grules.EMPTY + f2 \
                for i in range(blocks[0], size - min_width(blocks[1:])) \
                for f2 in fit(blocks[1:], size - i - 1)]

if __name__ == '__main__':
    bot()