import pygame
import griddlersrules as grules


GAP_SIZE = 1                # size of gap between boxes (in pixels)
BORDER_SIZE = GAP_SIZE*10   # gap between board and clues (in pixels)

# COLOR = (R, G, B)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
BLACK = (0, 0, 0)
NAVY_BLUE = (60, 60, 100)
LIGHT_GREY = (230, 230, 230)

UNDEFINED_COLOR = WHITE
EMPTY_COLOR = GREY
FILLED_COLOR = BLACK
BG_COLOR = NAVY_BLUE
CLUE_BOX_COLOR = LIGHT_GREY
TEXT_COLOR = BLACK

COLOR_RULES = {grules.UNDEFINED: UNDEFINED_COLOR,
               grules.EMPTY: EMPTY_COLOR,
               grules.FILLED: FILLED_COLOR}

LEFT_CLICK = 1
MIDDLE_CLICK = 2
RIGHT_CLICK = 3


class BoardDrawer:

    def __init__(self, column_clues, row_clues,
                 screen_width=640, screen_height=580):

        # display related attributes
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.screen = pygame.display.set_mode((self.screen_width,
                                              self.screen_height))

        # game related attributes
        self.column_clues = column_clues
        self.row_clues = row_clues

        self.board = grules.Board(row_clues, column_clues)

        # objects displayed related attributes
        self.board_width = len(column_clues)
        self.board_height = len(row_clues)
        self.row_clues_width = max(len(t) for t in row_clues)
        self.column_clues_height = max(len(t) for t in column_clues)

        self.box_size = min(self._potential_height_size(),
                            self._potential_width_size())

    def __call__(self):
        pygame.init()
        pygame.display.set_caption('Griddlers')
        self.screen.fill(BG_COLOR)
        self.draw_board()
        pygame.display.update()

    def click_treatment(self, mousex, mousey, mouseClicked):
        boxx, boxy = self.get_box_at_pixel(mousex, mousey)
        if boxx is not None and \
           boxy is not None and \
           mouseClicked is not None:
            self.click_on_box(boxx, boxy, mouseClicked)

    def click_on_box(self, boxx, boxy, mouseClicked):
        self.board.click_on_board(boxx, boxy, mouseClicked)
        # self.draw_board()
        self.draw_box(boxx, boxy)
        # pygame.display.update(a rectangle or some list of rectangles)
        # --> dans draw_box...
        # pygame.display.update()

    def draw_board(self):

        # Draws all of the boxes of the board
        for boxx in range(self.board_width):
            for boxy in range(self.board_height):
                left, top = self.get_coords_of_box(boxx, boxy)
                box_color = COLOR_RULES[self.board.state[boxx][boxy]]
                box_loc = (left, top, self.box_size, self.box_size)
                pygame.draw.rect(self.screen,
                                 box_color,
                                 box_loc)

        # Draws row clues boxes
        for boxx in range(self.row_clues_width):
            for boxy in range(self.board_height):
                left, top = self.get_coords_of_row_clue_box(boxx, boxy)
                pygame.draw.rect(self.screen,
                                 CLUE_BOX_COLOR,
                                 (left, top, self.box_size, self.box_size))
                # draw number in box
                swap_width = (self.column_clues_height -
                              len(self.board.row_clues[boxy]))
                if boxx in range(swap_width, self.column_clues_height):
                    font = pygame.font.Font(None, self.box_size)
                    text = str(self.board.row_clues[boxy][boxx - swap_width])
                    text = font.render(text, True, TEXT_COLOR)
                    self.screen.blit(text,
                                     (left+self.box_size/4,
                                      top+self.box_size/4))

        # Draws column clues boxes
        for boxx in range(self.board_width):
            for boxy in range(self.column_clues_height):
                left, top = self.get_coords_of_column_clue_box(boxx, boxy)
                pygame.draw.rect(self.screen,
                                 CLUE_BOX_COLOR,
                                 (left, top, self.box_size, self.box_size))
                # draw number in box
                swapHeight = (self.row_clues_width -
                              len(self.board.column_clues[boxx]))
                if boxy in range(swapHeight, self.row_clues_width):
                    font = pygame.font.Font(None, self.box_size)
                    text = str(self.board
                               .column_clues[boxx][boxy - swapHeight])
                    text = font.render(text, True, TEXT_COLOR)
                    self.screen.blit(text,
                                     (left+self.box_size/4,
                                      top+self.box_size/4))

    def draw_box(self, boxx, boxy):
        left, top = self.get_coords_of_box(boxx, boxy)
        box_color = COLOR_RULES[self.board.state[boxx][boxy]]
        box_loc = (left, top, self.box_size, self.box_size)
        pygame.draw.rect(self.screen,
                         box_color,
                         box_loc)
        pygame.display.update(box_loc)

    def get_box_at_pixel(self, x, y):
        for boxx in range(self.board_width):
            for boxy in range(self.board_height):
                left, top = self.get_coords_of_box(boxx, boxy)
                boxRect = pygame.Rect(left, top, self.box_size,
                                      self.box_size)
                if boxRect.collidepoint(x, y):
                    return (boxx, boxy)
        return (None, None)

    def get_coords_of_box(self, boxx, boxy):
        # Convert board coords to pixel coords (left top corner)
        left = (boxx*(self.box_size + GAP_SIZE) +
                self.row_clues_width*(self.box_size + GAP_SIZE) +
                BORDER_SIZE)
        if boxx/5 != 0:
            left += (boxx/5)*GAP_SIZE

        top = (boxy*(self.box_size + GAP_SIZE) +
               self.column_clues_height*(self.box_size + GAP_SIZE) +
               BORDER_SIZE)
        if boxy/5 != 0:
            top += (boxy/5)*GAP_SIZE

        return (left, top)

    def get_coords_of_row_clue_box(self, boxx, boxy):
        # Convert row clues coords to pixel coords (left top corner)
        left = boxx * (self.box_size + GAP_SIZE)

        top = (boxy*(self.box_size + GAP_SIZE) +
               self.column_clues_height*(self.box_size + GAP_SIZE) +
               BORDER_SIZE)
        if boxy/5 != 0:
            top += (boxy/5)*GAP_SIZE

        return (left, top)

    def get_coords_of_column_clue_box(self, boxx, boxy):
        # Convert column clues coords to pixel coords (left top corner)
        left = (boxx*(self.box_size + GAP_SIZE) +
                self.row_clues_width*(self.box_size + GAP_SIZE) +
                BORDER_SIZE)
        if boxx/5 != 0:
            left += (boxx/5)*GAP_SIZE

        top = boxy * (self.box_size + GAP_SIZE)

        return (left, top)

    def _potential_height_size(self):
        return ((self.screen_height -
                GAP_SIZE*(self.board_height-1) -
                GAP_SIZE*self.board_height/5 -
                BORDER_SIZE -
                GAP_SIZE*(self.column_clues_height - 1)) /
                (self.board_height+self.column_clues_height))

    def _potential_width_size(self):
        return ((self.screen_width -
                GAP_SIZE*(self.board_width - 1) -
                GAP_SIZE*self.board_width/5 -
                BORDER_SIZE -
                GAP_SIZE*(self.row_clues_width - 1)) /
                (self.board_width+self.row_clues_width))
