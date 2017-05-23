# uses nosetests

# Import subroutines to test
from play_in_terminal import endgame

# Import constants used
from play_in_terminal import PASS

class TestEndgame:

    # Moves is list of (int, Move)
    #   where int indicates the player, a base.int
    #   and Move indicates the move made, either PASS or [int, int, ..]
    #       denoting the position of the stone placed

    def test_trivial_endgame(self):
        # First, trivial case
        moves = [(1, PASS)]
        assert(endgame(moves, 1)) # a pass with one player ends the game

    def test_trivial_endgame2(self):
        # Another trivial case
        moves = [(1, PASS), (2, PASS)]
        assert(endgame(moves, 2)) # a pass with one player ends the game

    def test_regular_endgame(self):
        # A final case with some play before it
        moves = [(1, [1,1]), (2, [1,2]), (1, PASS), (2, PASS)]
        assert(endgame(moves, 2)) # a pass with one player ends the game

class TestValidMove:

    def test_surrounded_stones(self):
        # TODO
        pass

    def test_double_occupation(self):
        # TODO
        pass

    def test_no_state_reversal(self):
        # TODO
        pass
