# uses nosetests

# Import subroutines to test
from play_in_terminal import endgame

# Import constants used
from play_in_terminal import PASS

def test_endgame():

    # Moves is list of (int, Move)
    #   where int indicates the player, a base.int
    #   and Move indicates the move made, either PASS or [int, int, ..]
    #       denoting the position of the stone placed

    # First, trivial case
    moves = [(1, PASS)]
    assert(endgame(moves, 1)) # a pass with one player ends the game

    # Another trivial case
    moves = [(1, PASS), (2, PASS)]
    assert(endgame(moves, 2)) # a pass with one player ends the game

    # A final case with some play before it
    moves = [(1, [1,1]), (2, [1,2]), (1, PASS), (2, PASS)]
    assert(endgame(moves, 2)) # a pass with one player ends the game
