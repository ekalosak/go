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
MOVE_INSTRUCTIONS = "'X Y' or '{}' for pass".format(PASS)
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

def valid_move(move, board):

    ## Determine whether <move> is valid
    # Input
    #   move : (int, [int, int]) player plays stone at [int, int, ..]
    #   board : (np.array) the current state of the board
    # Output
    #   valid : (bool) whther the move is valid or not

    # TODO
    # Occupied spot cannot be twice occupied
    # Cannot kill self or own stones

    # Cannot return board to previous state (NOTE not implemented)

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
            player, move))

        # Determine whether it's a valid input
        if user_input == PASS:
            move = PASS

        else:
            try:
                move = [int(i) for i in user_input.split()]
                within_bounds = [i > 0 and i <= BOARD_SIZE for i in move]
                log.debug("Move is <{}> within bounds <{}>".format(
                    move, within_bounds))
                assert(all(within_bounds))

            except Exception as e:
                log.debug("User input <{}> raised Exception <{}>".format(
                    user_input, e))
                print("Invalid user input: {}".format(
                    user_input))
                continue # let the same player try again

        # Update the game log
        moves.append((player, move))

        # Determine whether endgame conditions are met and act accordingly
        game_over = endgame(moves, PLAYERS)
        if(game_over):
            log.debug("Game has ended after {} turns".format(turn))
            break

        # Determine whether move is valid
        if move != PASS:
            if valid_move(board, move):
                # If it is, apply move and calculate consequences
                log.debug("TODO: apply the move to the board")
            else:
                # If it isn't, ask for a different move
                print("Invalid move: {}".format(
                    user_input))
                continue # let the same player try again

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
