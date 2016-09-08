
UNDEFINED = 'u'
EMPTY = '0'
FILLED = '1'

LEFT_CLICK = 1
MIDDLE_CLICK = 2
RIGHT_CLICK = 3

CLICK_RULES = {LEFT_CLICK: FILLED,
               RIGHT_CLICK: UNDEFINED,
               MIDDLE_CLICK: EMPTY}


class Board:
    def __init__(self, row_clues, column_clues):
        self.row_clues = row_clues
        self.column_clues = column_clues

        self.board_width = len(column_clues)
        self.board_height = len(row_clues)

        self.state = self._init_board()

        self.validated_rows = [False for i in range(self.board_height)]
        self.validated_columns = [False for i in range(self.board_width)]

    def _init_board(self):
        return [[UNDEFINED
                for y in range(self.board_height)]
                for x in range(self.board_width)]

    def click_on_board(self, boxx, boxy, click_state):
        self.state[boxx][boxy] = CLICK_RULES[click_state]
        self.check_filled_lines()

    def check_filled_lines(self):
        for rowIndex in range(self.board_height):
            self.validated_rows[rowIndex] = (
                self.validate_line(
                    line=self.get_row(rowIndex),
                    clue=self.row_clues[rowIndex]))

        for colIndex in range(self.board_width):
            self.validated_columns[colIndex] = (
                self.validate_line(
                    line=self.get_column(colIndex),
                    clue=self.column_clues[colIndex]))

    def validate_line(self, line, clue):
        line = filter(None, ''.join(line)
                              .replace(UNDEFINED, EMPTY)
                              .split(EMPTY))

        # empty line case
        if clue is None and line is None:
            return True

        # not the amount of blocks case
        if len(line) != len(clue):
                return False

        # "classic" case
        for i in range(len(clue)):
            if clue[i] != len(line[i]):
                return False

        return True

    def check_win(self):
        for r in self.validated_rows:
            if not r:
                return False
        for c in self.validated_columns:
            if not c:
                return False
        return True

    def get_row(self, rowIndex):
        return [self.state[x][rowIndex]
                for x in range(self.board_width)]

    def get_column(self, columnIndex):
        return [self.state[columnIndex][y]
                for y in range(self.board_height)]

    def printBoard(self):
        for y in range(self.board_height):
            for x in range(self.board_width):
                sys.stdout.write(str(self.state[x][y]))
                sys.stdout.write(' ')
            sys.stdout.write('\n')


if __name__ == '__main__':

    board = Board([[], [], []], [[], [], []])
    board.check_filled_lines()

    print board.validated_rows
    print "\n"
    print board.validated_columns
