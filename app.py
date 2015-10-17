import sys
import os

import numpy as np
import pandas as pd
import pygame as pg
import pdb

REFRESH_RATE = 32
WHITE, BLACK = 'white', 'black'
LINE_COLOR = 0, 0, 0
LINE_WIDTH = 2

class Player(object):

    def __init__(self, color):
        self.color = color
        self.score = 0
        self.captured = []

    def validate(self):
        for stone in self.captured:
            assert type(stone) == Stone

class Stone(object):

    def __init__(self, x, y, color):
        self.location = x, y
        self.color = color

class Grid(object):

    def __init__(self, x = 9, y = 9):
        self.dims = x, y

class Board(object):

    def __init__(self, x = 9, y = 9):
        self.players = Player(WHITE), Player(BLACK)
        self.grid = Grid(x, y)
        self.dims = self.grid.dims
        self.states = []
        self.state = np.zeros(self.dims)
        self.whose_turn = self.players[0]
        self.selector = 0, 0

    def place_stone(self):
        # TODO put a stone where the selector is and validata/revert
        #   switch whose turn it is
        pdb.set_trace()

    def draw_grid(self, screen):

        sy, sx = screen.get_size()
        dy, dx = [screen.get_size()[a] / (self.dims[a] + 1) for a in range(2)]

        for k in range(self.dims[0]):
            st = dy + k * dy, dx
            ed = st[0], sx - dx
            pg.draw.line(screen, LINE_COLOR, st, ed, LINE_WIDTH)

        for k in range(self.dims[1]):
            st = dy, dx + k * dx
            ed = sy - dy, st[1]
            pg.draw.line(screen, LINE_COLOR, st, ed, LINE_WIDTH)

    def draw_stones(self, screen):
        pass

    def validate(self, state):
        # check that the move was valid
        #   remove captured stones
        pass

def test():
    print "Passed tests!!"

def main():

    pg.init()

    size = width, height = 320, 240
    black = 0, 0, 0
    white = 255, 255, 255
    board_color = 204, 153, 0

    screen = pg.display.set_mode(size)
    clock = pg.time.Clock()
    board = Board()

    while 1:

        clock.tick(REFRESH_RATE)

        if pg.key.get_focused():
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    sys.exit()

                elif event.type == pg.KEYUP:

                    keypress = pg.key.get_pressed()

                    # Move the selector
                    if keypress[pg.K_UP]:
                        board.move_select(pg.K_UP)
                    elif keypress[pg.K_DOWN]:
                        board.move_select(pg.K_DOWN)
                    elif keypress[pg.K_LEFT]:
                        board.move_select(pg.K_LEFT)
                    elif keypress[pg.K_RIGHT]:
                        board.move_select(pg.K_RIGHT)

                    # Enter a move
                    elif keypress[pg.SPACE]:
                        board.place_stone()

        screen.fill(board_color)
        board.draw_grid(screen)
        pg.display.flip()

if __name__ == '__main__':
    test()
    main()
