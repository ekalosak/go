import sys
import os
import itertools as itt
from copy import copy

import numpy as np
import pandas as pd
import pygame as pg
import pdb

STONE_SIZE = 5
SCREEN_SIZE = 450, 450
REFRESH_RATE = 60
WHITE, BLACK = (0, 0, 0), (255, 255, 255)
LINE_COLOR = 0, 0, 0
LINE_WIDTH = 2
SELECTOR_COLOR = 255, 0, 0
SELECTOR_SIZE = LINE_WIDTH + 2
N_SURROUNDED = 4

class Player(object):

    def __init__(self, color):
        self.color = color
        self.score = 0
        self.captured = []

    def validate(self):
        for stone in self.captured:
            assert type(stone) == Stone

class Stone(object):

    def __init__(self, y, x, player, grid):
        self.location = self.y, self.x = y, x
        self.player = player
        self.size = STONE_SIZE
        self.grid = grid

    def draw(self, screen):
        pg.draw.circle(screen,
                self.player.color,
                self.grid.get_point(*self.location[::-1]),
                self.size)

    def surrounding_locations(self):
        locs = []

        for dx in [-1, 1]:
            x = self.x + dx
            y = self.y
            if x >= 0 and\
                    x < self.grid.dims[1] and\
                    y >= 0 and\
                    y < self.grid.dims[0]:
                locs.append((y, x))

        for dy in [-1, 1]:
            x = self.x
            y = self.y + dy
            if x >= 0 and\
                    x < self.grid.dims[1] and\
                    y >= 0 and\
                    y < self.grid.dims[0]:
                locs.append((y, x))

        return locs

class Grid(object):

    def __init__(self, screensize, x = 9, y = 9):
        self.dims = x, y
        self.screensize = screensize
        self.points = self._calculate_grid_points()

    def _calculate_grid_points(self):

        dy, dx = [self.screensize[a] / (self.dims[a] + 1) for a in range(2)]
        points = np.empty([self.dims[0], self.dims[1], 2])

        for x, y in itt.product(range(self.dims[0]), range(self.dims[1])):
            px = dx + x * dx
            py = dy + y * dy
            points[y, x, 0] = py
            points[y, x, 1] = px

        return points

    def get_point(self, y, x):
        return [int(a) for a in self.points[y, x]]

    def draw(self, screen):

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

class Selector(object):

    def __init__(self, color, size, grid):
        self.color = color
        self.size = size
        self.location = self.y, self.x = [0, 0]
        self.grid = grid

    def move(self, dirn):

        if dirn == pg.K_UP:
            if self.y - 1 >= 0:
                self.y = self.y - 1
        elif dirn == pg.K_DOWN:
            if self.y + 1 < self.grid.dims[0]:
                self.y = self.y + 1
        elif dirn == pg.K_LEFT:
            if self.x - 1 >= 0:
                self.x = self.x - 1
        elif dirn == pg.K_RIGHT:
            if self.x + 1 < self.grid.dims[1]:
                self.x = self.x + 1

        self.location = self.y, self.x

    def draw(self, screen):
        pg.draw.circle(screen,
                SELECTOR_COLOR,
                self.grid.get_point(*self.location[::-1]),
                SELECTOR_SIZE)

class State(object):

    def __init__(self, dims, turn, board_stones, bowl_stones):
        self.dims = dims
        self.turn = turn
        self.board_stones = board_stones
        self.bowl_stones = bowl_stones

    def stone_at(self, loc):
        for stone in self.board_stones:
            if stone.location == loc:
                return stone
        return False

    def capture_stone(self, stone):
        if stone in board_stones:
            self.board_stones.remove(stone)
            self.bowl_stones.remove(stone)
        else:
            raise Exception("Stone <{}> isn't on the board")

    def draw(self, screen):
        for stone in self.board_stones:
            stone.draw(screen)

class Board(object):

    def __init__(self, screensize, x = 9, y = 9):
        self.screensize = screensize
        self.players = Player(WHITE), Player(BLACK)
        self.grid = Grid(screensize, x, y)
        self.dims = self.grid.dims
        self.states = [State(self.dims, 0, [], [])]
        self.cur_player = self.players[0]
        self.selector = Selector(color = SELECTOR_COLOR,
                size = SELECTOR_SIZE,
                grid = self.grid)

    def set_state(self, state):
        self.states.append(state)

    def get_state(self):
        return self.states[-1]

    def move_select(self, dirn):
        self.selector.move(dirn)

    def stone_at(self, loc):
        state = self.get_state()
        return state.stone_at(loc)

    def place_stone(self):
        loc = self.selector.location
        new_stone = Stone(y = loc[0], x = loc[1],
                player = self.cur_player,
                grid = self.grid)
        if self.valid_move(new_stone):
            self.next_turn(new_stone)

    def valid_move(self, new_stone):
        # avoid collisions
        if self.stone_at(new_stone.location):
            return False

        # no placing in a surrounded position
        state = copy(self.get_state())
        state.board_stones = state.board_stones + [new_stone]
        chain = self.get_chain(new_stone, state)
        if self.is_surrounded(chain):
            return False

        # no placing into a previous state (note that state has new_stone in it)
        cstones = self.capturable_stones_next_to(new_stone, state)
        for cstone in cstones:
            state.capture_stone(cstone)

        if state in self.states:
            return False

        # otherwise valid move
        return state

    def next_turn(self, new_stone):
        # make a new state
        old_state = self.get_state()
        new_state = State(self.dims,
                old_state.turn + 1,
                old_state.board_stones + [new_stone],
                old_state.bowl_stones)

        # move captured stones into the bin
        capturable_stones = self.capturable_stones_next_to(new_stone, new_state)
        for cstone in capturable_stones:
            state.capture_stone(cstone)

        # switch player
        self.cur_player = self.players[new_state.turn % len(self.players)]
        # set the new state to the current state
        self.set_state(new_state)

    def capturable_stones_next_to(self, stone, state):
        assert type(stone) == Stone
        assert type(state) == State
        capturable_stones = []
        for loc in stone.surrounding_locations():
            if state.stone_at(loc):
                stone = state.stone_at(loc)
                if stone.player != self.cur_player:
                    chain = self.get_chain(stone, state)
                    if self.is_surrounded(chain):
                        for cstone in chain:
                            capturable_stones.append(cstone)
        return capturable_stones

    def is_surrounded(self, chain):
        # Return True if all stones in chain have stones all around them
        for stone in chain:
            for loc in stone.surrounding_locations():
                if not self.stone_at(loc):
                    return False
        return True

    def get_chain(self, stone, state):
        stones_to_check = [stone]
        checked_stones = []
        chain = [stone]
        while len(stones_to_check) > 0:
            print "checking stone"
            check_stone = stones_to_check.pop()
            checked_stones.append(check_stone)
            if check_stone.player == stone.player:
                for loc in check_stone.surrounding_locations():
                    if self.stone_at(loc):
                        possible_check_stone = self.stone_at(loc)
                        if possible_check_stone.player == stone.player:
                            if possible_check_stone not in checked_stones:
                                stones_to_check.append(possible_check_stone)
        return chain

    def draw(self, screen):
        self.grid.draw(screen)
        state = self.get_state()
        state.draw(screen)
        self.selector.draw(screen)

def test():
    print "Passed tests!!"

def main():

    pg.init()

    size = width, height = SCREEN_SIZE
    black = 0, 0, 0
    white = 255, 255, 255
    board_color = 204, 153, 0

    screen = pg.display.set_mode(size)
    clock = pg.time.Clock()
    board = Board(screen.get_size())

    while 1:
        clock.tick(REFRESH_RATE)
        for event in pg.event.get():

            if event.type == pg.QUIT:
                sys.exit()

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
            elif keypress[pg.K_SPACE]:
                board.place_stone()

            # Quit
            elif keypress[pg.K_ESCAPE]:
                sys.exit(1)

        screen.fill(board_color)
        board.draw(screen)
        pg.display.flip()

if __name__ == '__main__':
    test()
    main()
