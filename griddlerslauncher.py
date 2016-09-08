import pygame
import sys
import collections

import pygame.locals as pgloc
import griddlersdisplay as gdisp
import griddlersbot as gbot

import griddlersrules as grules  # sert au cheat history

from pygame.locals import *

FPS = 30

KONAMI = (K_UP, K_UP, K_DOWN, K_DOWN, K_LEFT,
          K_RIGHT, K_LEFT, K_RIGHT, K_b, K_a)
ARROWS = (K_UP, K_DOWN, K_LEFT, K_RIGHT)

# sert au cheat history
INV_CLICK_RULES = {v: k for k, v in grules.CLICK_RULES.items()}


def main():
    row_clues = ([[1, 2], [1, 2], [2, 1], [1, 2, 1],
                 [4, 1, 1], [1, 1], [5, 1], [1, 4], [1, 4], [2, 3]])
    column_clues = ([[3], [2], [1, 1], [2, 1, 4],
                    [2, 1, 1], [3, 1], [1, 3], [6], [3], [7]])
    displayed_board = gdisp.BoardDrawer(column_clues, row_clues)
    displayed_board()

    cheat = collections.deque([0 for _ in range(len(KONAMI))], len(KONAMI))
    is_konami = False  # sera utile plus tard
    cheat_history_iterator = None

    fps_clock = pygame.time.Clock()

    while True:  # main game loop

        if is_konami:
            try:
                boxx, boxy, value = cheat_history_iterator.next()
            except StopIteration:
                is_konami = False
                cheat_history_iterator = None
                continue
            displayed_board.click_on_box(boxx, boxy, INV_CLICK_RULES[value])

        else:
            mouse_clicked = None

            for event in pygame.event.get():  # event handling loop
                if event.type == pgloc.QUIT or (event.type == pgloc.KEYUP and
                                                event.key == pgloc.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pgloc.MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouse_clicked = event.button
                    displayed_board.click_treatment(mousex, mousey, mouse_clicked)
                elif event.type == pygame.KEYDOWN:
                    char = event.dict['unicode']
                    if not char:
                        cheat.append(event.key)  # ajout caractere "fleche"
                    else:
                        cheat.append(ord(char))  # ajout d'un caractere ascii

                    if tuple(list(cheat)) == KONAMI:
                        bot = gbot.Bot(displayed_board)
                        bot()
                        # displayed_board.draw_board()
                        # pygame.display.update()
                        is_konami = True
                        # cheat_history_iterator = bot.history.__iter__()
                        cheat_history_iterator = iter(bot.history)


        fps_clock.tick(FPS)

if __name__ == '__main__':
    main()
