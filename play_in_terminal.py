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
cap_stones = np.zeros((PLAYERS, PLAYERS))
bottom_guide = np.arange(BOARD_SIZE) + 1
side_guide = np.array([np.arange(BOARD_SIZE + 1) + 1]).T

log.debug("Setup game objects")

## Subroutines

def endgame(moves):
    ## Determine whether the move <move> ends the game
    # Input
    #   moves : (list(tuple(int, move))) moves already played
    #       move is either PASS or [int, int, ...]
    #   nplayers : (int) number of players in the game
    # Output
    #   game_over : (bool) whether <move> ended the game

    if(len(moves) < PLAYERS):
        return(False)

    last_moves = moves[-PLAYERS:]
    were_pass = [l[1] == PASS for l in last_moves]
    return(all(were_pass))

def neighbors(move, board):
    # Return the positions of neighbors of a stone, handles edge cases
    # Note: moves are (int, [Y, X])
    # NOTE: only works for 2 Dimensions

    y, x = move[1]
    m = np.shape(board)[1]
    r = None

    # corners
    if(x == 1 and y == 1):
        r = [[1,2], [2,1]]
    elif(x == 1 and y == m):
        r = [[m-1,1], [m,2]]
    elif(x == m and y == 1):
        r = [[2,m], [1,m-1]]
    elif(x == m and y == m):
        r = [[m,m-1], [m-1,m]]

    # sides
    if(x == 1):
        r = [[y+1,1], [y-1,1], [y,2]]
    elif(x == m):
        r = [[y+1,m], [y-1,m], [y,m-1]]
    elif(y == 1):
        r = [[y,x-1], [y,x+1], [y+1,x]]
    elif(y == m):
        r = [[y,x-1], [y,x+1], [y-1,x]]

    else:
        r = [[y+1,x], [y-1,x], [y,x+1], [y,x-1]]

    # log.debug("Neighbors of <{}> are <{}>".format(move, r))

    return(r)

def chain(move, board):
    # TODO
    # Return the locations of the chain of stones connected to the stone placed
    #   in <move>
    pass

def stone_liberties(move, board):
    # Return the number of liberties of a single stone placed on the board
    pdb.set_trace()
    return(sum([move[0] == n[0] for n in neighbors(move=move, board=board)]))

def chain_liberties(move, board):
    # Return the number of liberties of a chain of stones placed on the board
    return(sum([stone_liberties(s) for s in chain(move=move, board=board)]))

def captured(move, board):
    # NOTE will only work properly for 2 players right now
    # Return the stones captured by playing <move> on <board>
    # return = list of lists e.g. [(2, [1,1]), (2, [1,2])]

    r = []
    for n in neighbors(move=move, board=board):
        if(not n[0] == move[0]): # if it's not your stone
            if(stone_liberties(move=n, board=board) == 0): # and it's dead
                r += chain(board=board, move=n) # add its chain to return
    return r

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
                move_loc = [int(i) for i in user_input.split()]
                within_bounds = [i > 0 and i <= BOARD_SIZE for i in move_loc]
                assert(all(within_bounds))
                move = (player, move_loc)
                log.debug("Move is <{}> within bounds <{}>".format(
                    move, within_bounds))

            except Exception as e:
                log.debug("User input <{}> raised Exception <{}>".format(
                    user_input, e))
                print("Invalid user input: {}".format(
                    user_input))
                continue # let the same player try again

        ## Determine whether move is valid and play it if it is
        if move != PASS:
            if valid_move(board=board, move=move):
                # Put stone on board
                board[tuple([m - 1 for m in move[1]])] = move[0]
                # Remove captured stones
                for mv in captured(board=board, move=move):
                    cap_stones[player, mv[0]] += 1 # record the capture
                    mvloc = tuple([m-1 for m in mv[1]])
                    board[mvloc] = 0
            else:
                print("Invalid move: <{}>, please try another".format(
                    user_input))
                continue # let the same player try again

        # Update the game log
        moves.append((player, move))
        boards.append(board)

        # Determine whether endgame conditions are met and act accordingly
        if(endgame(moves)):
            log.debug("Game has ended after {} turns".format(turn))
            break

        # Switch players, increment turns, and other cleanup
        log.debug("End of turn {}".format(turn))
        player = (player % PLAYERS) + 1
        turn = turn + 1

    sys.exit(0)
    # TODO
    # Calculate and report score
    score = score_game(board)
    log.debug("Game score is {}".format(score))

    # Save game to disk
    log.debug("Saving game")
    save_game(moves)
