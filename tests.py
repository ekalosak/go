# uses nosetests

# Import subroutines to test
from play_in_terminal import endgame, valid_move, neighbors, liberties,
    captured, chain

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
        board = array([[0,1,0],
                       [1,0,1],
                       [0,1,0]])
        move1 = (1, [2,2]) # player 1 tries to play in center, ok
        move2 = (2, [2,2]) # player 2 tries to play in center, surrounded
        assert(valid_move(move1, board))
        assert(not valid_move(move2, board))
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

        move1 = (1, [2,2]) # player 1 placing a stone at (2,2) the center
        move2 = (1, [3,2])
        move3 = (1, [1,1])
        assert(liberties(move1, board) == 4)
        assert(liberties(move2, board) == 3)
        assert(liberties(move3, board) == 2)

    def test_chain_stones(self):
        board = array([[0,1,0],
                       [1,0,0],
                       [0,0,0]])

        move1 = (1, [2,2])
        move2 = (1, [1,1])
        move3 = (1, [1,3])
        assert(liberties(move1, board) == 5)
        assert(liberties(move2, board) == 3)
        assert(liberties(move3, board) == 3)

    def test_complicated_chain(self):
        board = array([[1,1,0,0,0],
                       [0,1,1,0,0],
                       [0,0,1,0,0],
                       [0,0,1,0,0],
                       [0,0,1,0,0]])
        move1 = (1, [3,1])
        move2 = (1, [4,5])
        assert(liberties(move1, board) == 9)
        assert(liberties(move2, board) == 9)

    def test_with_other_players(self):
        board = array([[0,1,0],
                       [1,0,2],
                       [2,2,2]])
        move = (1, [2,2])
        assert(liberties(move, board) == 2)


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

    def test_small_chain(self):
        board = array([[0,1,0],
                       [1,0,1],
                       [0,0,0]])
        move = (1, [2,2])
        true_chain = [[1,2], [2,1], [2,2], [3,2]]
        calculated_chain = chain(move, board)
        assert(all([ch in calculated_chain for ch in true_chain]))
        assert(len(true_chain) == len(calculated_chain))

    def test_chain_with_other_colors(self):
        board = array([[2,1,2],
                       [1,0,1],
                       [2,2,0]])
        move = (1, [2,2])
        true_chain = [[1,2], [2,1], [2,2], [3,2]]
        calculated_chain = chain(move, board)
        assert(all([ch in calculated_chain for ch in true_chain]))
        assert(len(true_chain) == len(calculated_chain))

    def test_trivial_chain(self):
        board = array([[0,0,0],
                       [0,0,0],
                       [0,0,0]])
        move = (1, [1,1])
        assert(chain(move, board) == [[1,1]])

class TestCaptured:

    def test_simple_capture(self):
        board = array([[0,1,0],
                        [1,2,1],
                        [0,0,0]])

        move = (1, [2,3])
        assert(captured(move, board) == [(2, [2,2])])

    def test_chain_capture(self):
        assert(False)

    def test_no_capture(self):
        board = array([[0,1,0],
                        [1,2,1],
                        [0,0,0]])

        move = (1, [1,1])
        assert(captured(move, board) == [])
