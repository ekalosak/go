### Play the game of Go in your terminal
# Author: Eric Kalosa-Kenyon
# Date: May 24, 2017
# License: MIT
###

### BEGIN: Code

## Imports

# Standard libraries
import sys
import os
import itertools as itt
from copy import copy

# 3rd party libraries
import numpy as np
import pdb

# Local libraries
import utils

## Preamble

log = utils.make_logger('go-in-terminal', verbose = True)
log.debug("Libraries successfully imported")

## Parameterize game

PASS = 'p'
MOVE_INSTRUCTIONS = "'Y X' or '{}' for pass".format(PASS)
BOARD_SIZE = 9 # Make an X by X sized go board
DIMENSIONS = 2 # Dimensionality of the board, if not 2, YMMV
PLAYERS = 2 # Players, usually 2, if more or less YMMV
log.debug("Playing on board size {}^{} with {} players".format(
    BOARD_SIZE, DIMENSIONS, PLAYERS))

## Setup the game

game_over = False
player = 1
shape = [BOARD_SIZE for b in range(DIMENSIONS)]
board = np.zeros(shape, dtype=np.int8)
boards = []
move = None
moves = []
bottom_guide = np.arange(BOARD_SIZE) + 1
side_guide = np.array([np.arange(BOARD_SIZE + 1) + 1]).T

log.debug("Setup game objects")

## Subroutines

def endgame(moves, nplayers):
    ## Determine whether the move <move> ends the game
    # Input
    #   moves : (list(tuple(int, move))) moves already played
    #       move is either PASS or [int, int, ...]
    #   nplayers : (int) number of players in the game
    # Output
    #   game_over : (bool) whether <move> ended the game

    last_moves = moves[-nplayers:]
    print(last_moves)
    return(all([l[1] == PASS for l in last_moves]))

def neighbors(move, board):
    # TODO
    # Return the positions of neighbors of a stone, handles edge cases
    # Note: moves are (int, [X, Y])
    # NOTE: only works for 2 Dimensions

    y, x = move[1]
    m = np.shape(board)[1]
    r = None

    if(x == 1):
        if(y == 1):
            r = [[1,2], [2,1]]
        elif(y == m):
            r = [[1,m-1], [2,m]]
        else:
            r = [[1,y+1], [1,y-1], [2,y]]

    elif(x == m):
        if(y == 1):
            r = [[m,2], [m-1,1]]
        elif(y == m):
            r = [[m,m-1], [m-1,m]]
        else:
            r = [[m,y+1], [m,y-1], [m-1,y]]

    else:
        r = [[x,y+1], [x,y-1], [x+1,y], [x-1,y]]

    return(r)

def chain(move, board):
    # TODO
    # Return the locations of the chain of stones connected to the stone placed
    #   in <move>
    pass

def liberties(move, board):
    # TODO
    # Return the number of liberties of a stone placed on the board
    #   more or less depth first search of a chain of stones connected to move
    pass

def captured(move, board):
    # TODO
    # NOTE will only work properly for 2 players right now
    # Return the stones captured by playing <move> on <board>
    # return = list of lists e.g. [[1,1], [1,2]] for stones at those locs
    pass

def valid_move(move, board):

    ## Determine whether <move> is valid
    # Input
    #   move : (int, [int, int]) player plays stone at [int, int, ..]
    #   board : (np.array) the current state of the board
    # Output
    #   valid : (bool) whther the move is valid or not

    # Occupied spot cannot be twice occupied
    # i.e cannot play on a stone already there
    move_loc = [m - 1 for m in move[1]]
    # subboard = board
    # for i in range(DIMENSIONS - 1): # This loop collapses the potentially
    #                                 # multimdimensional go board
    #     subboard = subboard[move_loc[i], :]
    # board_at_loc = subboard[move_loc[DIMENSIONS - 1]]
    board_at_loc = board[tuple(move_loc)]

    if(board_at_loc != 0):
        return False

    # TODO
    # Cannot kill self or own stones
    # Cannot return board to previous state

    return True

## Main loop

if __name__ == "__main__":

    turn = 0
    while(game_over == False):

        # Show the user the game board (NOTE: currently works only for 2-dim)
        print_board = np.vstack((board, bottom_guide))
        print_board = np.hstack((print_board, side_guide))
        print(print_board)

        # Ask user for a move
        log.debug("After {} turns, it's player {}'s move".format(
            turn, player))
        print("Player {}: please select a move {}".format(
            player, MOVE_INSTRUCTIONS))
        user_input = input()
        log.debug("Player {} gave input <{}>".format(
            player, user_input))

        # Determine whether it's a valid input
        if user_input == PASS:
            move = PASS
        else:
            try:
                move = [int(i) for i in user_input.split()]
                within_bounds = [i > 0 and i <= BOARD_SIZE for i in move]
                assert(all(within_bounds))
                log.debug("Move is <{}> within bounds <{}>".format(
                    move, within_bounds))

            except Exception as e:
                log.debug("User input <{}> raised Exception <{}>".format(
                    user_input, e))
                print("Invalid user input: {}".format(
                    user_input))
                continue # let the same player try again

        # Check that the move is valid under game logic
        if(not valid(move, board)):
            log.debug("User move <{}> invalid".format(move))
            print("Move invalid, please try another")
            continue # let the same player try again

        # Determine whether endgame conditions are met and act accordingly
        if(endgame(moves, PLAYERS)):
            log.debug("Game has ended after {} turns".format(turn))
            break

        ## Determine whether move is valid and play it if it is
        if move != PASS:
            if valid_move(board, move):
                # If it is, apply move and calculate consequences
                # TODO Put stone on board
                # TODO Remove captured stones
                pass
            else:
                # If it isn't, ask for a different move
                print("Invalid move: <{}>, please try another".format(
                    user_input))
                continue # let the same player try again

        # Update the game log
        moves.append((player, move))
        boards.append(board)

        # Switch players, increment turns, and other cleanup
        log.debug("End of turn {}".format(turn))
        player = ((player + 1) % PLAYERS) + 1
        turn = turn + 1

    sys.exit(0)
    # TODO
    # Calculate and report score
    score = score_game(board)
    log.debug("Game score is {}".format(score))

    # Save game to disk
    log.debug("Saving game")
    save_game(moves)
