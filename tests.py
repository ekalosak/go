# uses nosetests

# Import subroutines to test
from play_in_terminal import endgame, valid_move, neighbors, liberties

# Import constants used
from play_in_terminal import PASS

# Import requisite 3rd party libraries
from numpy import array

class TestEndgame:

    # Moves is list of (int, Move)
    #   where int indicates the player, a base.int
    #   and Move indicates the move made, either PASS or [int, int, ..]
    #       denoting the position of the stone placed

    def test_trivial_endgame(self):
        moves = [(1, PASS)]
        assert(endgame(moves, 1)) # a pass with one player ends the game

    def test_trivial_endgame2(self):
        moves = [(1, PASS), (2, PASS)]
        assert(endgame(moves, 2)) # two passes with two players ends the game

    def test_regular_endgame(self):
        # A case with some play before it
        moves = [(1, [1,1]), (2, [1,2]), (1, PASS), (2, PASS)]
        assert(endgame(moves, 2)) # game ends when everyone passes

    def test_not_endgame(self):
        # A failure case with some play before it
        moves = [(1, [1,1]), (2, [1,2]), (1, PASS), (2, [2,2])]
        assert(not endgame(moves, 2)) # game ends when everyone passes


class TestValidMove:

    def test_surrounded_stones(self):
        # TODO
        assert(False)

    def test_double_occupation(self):
        board = array([[1, 0], [0, 0]]) # stone only in upper left corner
        move1 = (1, [1,1]) # player 1 tries to play in upper left
        move2 = (2, [1,1]) # player 2 tries to play in upper left
        assert(not valid_move(move1, board))
        assert(not valid_move(move2, board))

    def test_no_state_reversal(self):
        # TODO
        assert(False)

class TestLiberties:

    def test_single_stone(self):
        board = array([[0,0,0],
                       [0,0,0],
                       [0,0,0]])

        move = (1, [2,2]) # player 1 placing a stone at (2,2) the center
        assert(liberties(move, board) == 4)

        move = (1, [3,2])
        assert(liberties(move, board) == 3)

        move = (1, [1,1])
        assert(liberties(move, board) == 2)

    def test_chain_stones(self):
        board = array([[0,1,0],
                       [1,0,0],
                       [0,0,0]])

        move = (1, [2,2])
        assert(liberties(move, board) == 5)

        move = (1, [1,1])
        assert(liberties(move, board) == 3)

        move = (1, [1,3])
        assert(liberties(move, board) == 3)

    def test_complicated_chain(self):
        board = array([[0,0,0,0,0],
                       [0,0,0,0,0],
                       [0,0,0,0,0],
                       [0,0,0,0,0],
                       [0,0,0,0,0]])
        #TODO more tests here
        raise(NotImplementedError)

class TestNeighbors:

    def setUp(self):
        self.board = array([[0,0,0],
                            [0,0,0],
                            [0,0,0]])

    def tearDown(self):
        pass

    def test_corners(self):
        move1 = (1, [1,1])
        move2 = (1, [1,3])
        move3 = (1, [3,1])
        move4 = (1, [3,3])

        ns1 = neighbors(move1, self.board)
        ns2 = neighbors(move2, self.board)
        ns3 = neighbors(move3, self.board)
        ns4 = neighbors(move4, self.board)

        tn1 = [[1,2],[2,1]]
        tn2 = [[1,2],[2,3]]
        tn3 = [[3,2],[2,1]]
        tn4 = [[3,2],[2,3]]

        assert(all([t in ns1 for t in tn1]))
        assert(all([t in ns2 for t in tn2]))
        assert(all([t in ns3 for t in tn3]))
        assert(all([t in ns4 for t in tn4]))

    def test_sides(self):
        move1 = (1, [1,2])
        move2 = (1, [2,1])
        move3 = (1, [3,2])
        move4 = (1, [2,3])

        ns1 = neighbors(move1, self.board)
        ns2 = neighbors(move2, self.board)
        ns3 = neighbors(move3, self.board)
        ns4 = neighbors(move4, self.board)

        tn1 = [[1,1],[1,3],[2,2]]
        tn2 = [[1,1],[3,1],[2,2]]
        tn3 = [[3,1],[3,3],[2,2]]
        tn4 = [[1,3],[3,3],[2,2]]

        assert(all([t in ns1 for t in tn1]))
        assert(all([t in ns2 for t in tn2]))
        assert(all([t in ns3 for t in tn3]))
        assert(all([t in ns4 for t in tn4]))

    def test_center(self):
        move1 = (1, [2,2])

        ns1 = neighbors(move1, self.board)

        tn1 = [[1,2],[2,1],[3,2],[2,3]]

        assert(all([t in ns1 for t in tn1]))

class TestChain:

    def test_trivial_chain(self):
        pass
