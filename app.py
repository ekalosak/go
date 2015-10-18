import sys
import os
import itertools as itt
from copy import copy

import numpy as np
import pandas as pd
import pygame as pg
import pdb

import utils

STONE_SIZE = 10
SCREEN_SIZE = 450, 450
REFRESH_RATE = 60
WHITE, BLACK = (0, 0, 0), (255, 255, 255)
LINE_COLOR = 0, 0, 0
LINE_WIDTH = 2
SELECTOR_COLOR = 255, 0, 0
SELECTOR_SIZE = LINE_WIDTH + 2

class Player(object):

    def __init__(self, color):
        self.color = color
        self.score = 0
        log.debug("created player: <{}>".format(self))

    def __repr__(self):
        msg = "<Player: color={}, score={}>".format(self.color, self.score)
        return msg

    def __eq__(self, other):
        if type(other) != Player:
            msg = "<Received type <{}>, expected <{}>>".format(
                    type(other), Player)
            raise TypeError(msg)
        return self.color == other.color

    def validate(self):
        pass

class Stone(object):

    def __init__(self, y, x, player, grid):
        self.location = self.y, self.x = y, x
        self.player = player
        self.size = STONE_SIZE
        self.grid = grid
        log.debug("created stone: <{}>".format(self))

    def __repr__(self):
        msg = "<Stone: location={}, player={}>"
        msg = msg.format(self.location, self.player)
        return msg

    def __eq__(self, other):
        if type(other) != Stone:
            msg = "Received type <{}>, expected <{}>".format(
                    type(other), Stone)
            raise TypeError(msg)
        eq_relations = [self.location == other.location,
                self.player == self.player]
        return all(eq_relations)

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

        log.debug("the points surrounding <{}> are <{}>".format(
            self.location, locs))
        return locs

    def draw(self, screen):
        pg.draw.circle(screen,
                self.player.color,
                self.grid.get_point(*self.location[::-1]),
                self.size)

class Grid(object):

    def __init__(self, screensize, x = 9, y = 9):
        self.dims = x, y
        self.screensize = screensize
        self.points = self._calculate_grid_points()
        log.debug("created grid: <{}>".format(self))

    def __repr__(self):
        msg = "<Grid: dimensions={}>".format(self.dims)
        return msg

    def __eq__(self, other):
        if type(other) != Grid:
            msg = "Received type <{}>, expected <{}>".format(
                    type(other), Grid)
            raise TypeError(msg)
        return self.dims == other.dims

    def _calculate_grid_points(self):

        dy, dx = [self.screensize[a] / (self.dims[a] + 1) for a in range(2)]
        points = np.empty([self.dims[0], self.dims[1], 2])

        for x, y in itt.product(range(self.dims[0]), range(self.dims[1])):
            px = dx + x * dx
            py = dy + y * dy
            points[y, x, 0] = py
            points[y, x, 1] = px

        log.debug("calculated grid points: <{}>".format(
            np.shape(points)))
        return points

    def get_point(self, y, x):
        point = [int(a) for a in self.points[y, x]]
        # NOTE this gets called in a draw loop so it's debugging spam
        # log.debug("point <{}> is located at <{}>".format(
        #     (y, x), point))
        return point

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
        log.debug("created selector: <{}>".format(self))

    def __repr__(self):
        msg = "<Selector: location={}>".format(self.location)
        return msg

    def __eq__(self, other):
        if type(other) != Selector:
            msg = "Received type <{}>, expected <{}>".format(
                    type(other), Selector)
            raise TypeError(msg)
        return self.location == other.location

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
        log.debug("moved selector in direction <{}> to <{}>".format(
            pg.key.name(dirn), self.location))

    def draw(self, screen):
        pg.draw.circle(screen,
                SELECTOR_COLOR,
                self.grid.get_point(*self.location[::-1]),
                SELECTOR_SIZE)

class State(object):

    def __init__(self, turn, board_stones, bowl_stones):
        self.turn = turn
        self.board_stones = board_stones
        self.bowl_stones = bowl_stones
        log.debug("created state: <{}>".format(self))

    def __repr__(self):
        msg = "<State: turn={}, nstones={}>"
        msg = msg.format(self.turn, len(self.get_stones()))
        return msg

    def __eq__(self, other):
        if type(other) != State:
            msg = "Received type <{}>, expected <{}>".format(
                    type(other), State)
            raise TypeError(msg)
        o_stones = other.get_stones()
        for stone in self.get_stones():
            if stone not in o_stones:
                return False
        assert self.turn == other.turn
        return True

    def get_stones(self):
        return self.board_stones + self.bowl_stones

    def stone_at(self, loc):
        for stone in self.board_stones:
            if stone.location == loc:
                log.debug("there is a stone at <{}>".format(loc))
                return stone
        log.debug("there is not a stone at <{}>".format(loc))
        return False

    def capture_stone(self, stone):
        if stone in board_stones:
            self.board_stones.remove(stone)
            self.bowl_stones.remove(stone)
            log.debug("<{}> has been captured".format(stone))
        else:
            msg = "stone <{}> isn't on the board".format(stone)
            log.error(msg)
            raise Exception(msg)

    def draw(self, screen):
        for stone in self.board_stones:
            stone.draw(screen)

class Board(object):

    def __init__(self, screensize, x = 9, y = 9):
        self.screensize = screensize
        self.players = Player(WHITE), Player(BLACK)
        self.grid = Grid(screensize, x, y)
        self.dims = self.grid.dims
        self.states = [State(0, [], [])]
        self.cur_player = self.players[0]
        self.selector = Selector(color = SELECTOR_COLOR,
                size = SELECTOR_SIZE,
                grid = self.grid)
        log.debug("created board: <{}>".format(self))

    def __repr__(self):
        msg = "<Board: dimensions={}, nplayers={}, nstates={}, " +\
                "curplayer={}, selector at {}>"
        msg = msg.format(self.dims, len(self.players), len(self.states),
                self.cur_player, self.selector.location)
        return msg

    def __eq__(self, other):
        if type(other) != Board:
            msg = "Received type <{}>, expected <{}>".format(
                    type(other), Board)
            raise TypeError(msg)
        eq_relations = [self.grid == other.grid,
                self.players == other.players,
                self.cur_player == other.cur_player,
                self.get_state() == other.get_state(),
                self.selector == other.selector]
        return all(eq_relations)

    def undo(self):
        log.warning("undo not yet implemented")
    def pass_move(self):
        log.warning("pass_move not yet implemented")

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

        state = self.valid_move(new_stone)
        if state:
            state.turn = state.turn + 1
            self.next_turn(state)

    def valid_move(self, new_stone):
        # avoid collisions
        if self.stone_at(new_stone.location):
            log.debug("move <{}> is invalid due to collision".format(
                new_stone))
            return False

        # no placing in a surrounded position
        state = copy(self.get_state())
        state.board_stones = state.board_stones + [new_stone]
        chain = self.get_chain(new_stone, state)
        if self.is_surrounded(chain):
            log.debug("move <{}> is invalid because it is surrounded".format(
                new_stone))
            return False

        # capture stones if there are any capturable
        cstones = self.capturable_stones_next_to(new_stone, state)
        if cstones: log.debug("capturing stones: <{}>".format(cstones))
        else: log.debug("no stones to capture")
        for cstone in cstones:
            state.capture_stone(cstone)

        # make sure it's not a repeat move
        if state in self.states:
            log.debug("move <{}> is invalid due to repeat state <{}>".format(
                new_stone, self.states(self.states.index(state))))
            return False

        # otherwise valid move
        log.debug("<{}> is a valid move".format(new_stone))
        return state

    def next_turn(self, next_state):
        # switch player
        self.cur_player = self.players[next_state.turn % len(self.players)]
        # set the new state to the current state
        self.set_state(next_state)
        log.debug("starting turn <{}> with player <{}>".format(
            next_state.turn, self.cur_player))
        log.debug("-" * 40)

    def capturable_stones_next_to(self, stone, state):
        assert type(stone) == Stone
        assert type(state) == State
        capturable_stones = []
        for loc in stone.surrounding_locations():
            stone = state.stone_at(loc)
            if stone:
                if stone.player != self.cur_player:
                    chain = self.get_chain(stone, state)
                    if self.is_surrounded(chain):
                        for cstone in chain:
                            capturable_stones.append(cstone)
        log.debug("the capturable stones next to <{}> are: <{}>".format(
            stone, capturable_stones))
        return capturable_stones

    def is_surrounded(self, chain):
        # Return True if all stones in chain have stones all around them
        for stone in chain:
            for loc in stone.surrounding_locations():
                if not self.stone_at(loc):
                    log.debug("chain with <{}> is not surrounded".format(
                        chain[0]))
                    return False
        log.debug("chain with <{}> is surrounded".format(chain[0]))
        return True

    def get_chain(self, stone, state):
        log.debug("getting chain starting at <{}>".format(stone))
        stones_to_check = [stone]
        checked_stones = []
        chain = [stone]
        while len(stones_to_check) > 0:
            check_stone = stones_to_check.pop()
            checked_stones.append(check_stone)
            if check_stone.player == stone.player:
                for loc in check_stone.surrounding_locations():
                    if self.stone_at(loc):
                        possible_check_stone = self.stone_at(loc)
                        if possible_check_stone.player == stone.player:
                            if possible_check_stone not in checked_stones:
                                chain.append(possible_check_stone)
                                stones_to_check.append(possible_check_stone)

        log.debug("calculated chain connected to <{}>: <{}>".format(
            stone, chain))
        log.debug("chain length: <{}>".format(len(chain)))
        return chain

    def draw(self, screen):
        self.grid.draw(screen)
        state = self.get_state()
        state.draw(screen)
        self.selector.draw(screen)

def test(log):
    log.debug("no tests")

def main(log):

    log.debug("initializing app")
    pg.init()

    size = width, height = SCREEN_SIZE
    black = 0, 0, 0
    white = 255, 255, 255
    board_color = 204, 153, 0

    screen = pg.display.set_mode(size)
    clock = pg.time.Clock()
    board = Board(screen.get_size())

    log.debug("starting main loop")
    while 1:
        clock.tick(REFRESH_RATE)
        for event in pg.event.get():

            if event.type == pg.QUIT:
                log.debug("quitting")
                sys.exit()

            keypress = pg.key.get_pressed()
            if sum(keypress) > 0:
                key_name = pg.key.name(keypress.index(1))
                log.debug("key pressed: <{}>".format(key_name))

            # Move the selector
            if keypress[pg.K_UP]:
                board.move_select(pg.K_UP)
            elif keypress[pg.K_DOWN]:
                board.move_select(pg.K_DOWN)
            elif keypress[pg.K_LEFT]:
                board.move_select(pg.K_LEFT)
            elif keypress[pg.K_RIGHT]:
                board.move_select(pg.K_RIGHT)

            # Place a stone
            elif keypress[pg.K_SPACE]:
                log.debug("placing stone")
                board.place_stone()

            # TODO
            elif keypress[pg.K_p]:
                log.debug("passing")
                board.pass_move()
            elif keypress[pg.K_u]:
                log.debug("undoing")
                board.undo()

            # Quit
            elif keypress[pg.K_ESCAPE]:
                log.debug("quitting")
                sys.exit(1)

        screen.fill(board_color)
        board.draw(screen)
        pg.display.flip()

if __name__ == '__main__':
    log = utils.make_logger('go-app', verbose = True)
    test(log)
    main(log)
