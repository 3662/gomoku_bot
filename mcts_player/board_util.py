"""
board_util.py
Utility functions for Go board.
"""

import numpy as np
import random
import time

from patterns import *

"""
Encoding of colors on and off a Go board.
FLODDFILL is used internally for a temporary marker
"""
EMPTY = 0
BLACK = 1
WHITE = 2
BORDER = 3


def is_black_white(color):
    return color == BLACK or color == WHITE


def is_black_white_empty(color):
    return color == BLACK or color == WHITE or color == EMPTY


"""
A GO_POINT is a point on a Go board.
It is encoded as a 32-bit integer, using the numpy type.
"""
GO_POINT = np.int32

"""
Encoding of special pass move
"""
PASS = None

"""
Encoding of "not a real point", used as a marker
"""
NULLPOINT = 0

"""
The largest board we allow. 
To support larger boards the coordinate printing in
GtpConnection.format_point needs to be changed.
"""
MAXSIZE = 25

"""
where1d: Helper function for using np.where with 1-d arrays.
The result of np.where is a tuple which contains the indices 
of elements that fulfill the condition.
For 1-d arrays, this is a singleton tuple.
The [0] indexing is needed to extract the result from the singleton tuple.
"""
def where1d(condition):
    return np.where(condition)[0]


def coord_to_point(row, col, boardsize):
    """
    Transform two dimensional (row, col) representation to array index.

    Arguments
    ---------
    row, col: int
             coordinates of the point  1 <= row, col <= size

    Returns
    -------
    point
    
    Map (row, col) coordinates to array index
    Below is an example of numbering points on a 3x3 board.
    Spaces are added for illustration to separate board points 
    from BORDER points.
    There is a one point BORDER between consecutive rows (e.g. point 12).
    
    16   17 18 19   20

    12   13 14 15
    08   09 10 11
    04   05 06 07

    00   01 02 03

    File board_util.py defines the mapping of colors to integers,
    such as EMPTY = 0, BORDER = 3.
    For example, the empty 3x3 board is encoded like this:

    3  3  3  3  3
    3  0  0  0
    3  0  0  0
    3  0  0  0
    3  3  3  3

    This board is represented by the array
    [3,3,3,3,  3,0,0,0,  3,0,0,0,  3,0,0,0,  3,3,3,3,3]
    """
    assert 1 <= row
    assert row <= boardsize
    assert 1 <= col
    assert col <= boardsize
    NS = boardsize + 1
    return NS * row + col

class GoBoardUtil(object):
    @staticmethod
    def generate_legal_moves(board, color):
        """
        generate a list of all legal moves on the board.
        Does not include the Pass move.

        Arguments
        ---------
        board : np.array
            a SIZExSIZE array representing the board
        color : {'b','w'}
            the color to generate the move for.
        """
        moves = board.get_empty_points()
        legal_moves = []
        for move in moves:
            if board.is_legal(move, color):
                legal_moves.append(move)
        return legal_moves

    @staticmethod
    def generate_random_move(board, color):
        """
        Generate a random move.
        Return PASS if no move found

        Arguments
        ---------
        board : np.array
            a 1-d array representing the board
        color : BLACK, WHITE
            the color to generate the move for.
        """
        moves = board.get_empty_points()
        if len(moves) == 0:
            return PASS
        np.random.shuffle(moves)
        return moves[0]

    """
    return the type of moves and set of moves to consider for a policy of 
    random selection of moves
    """
    @staticmethod
    def random_policy_moves(board, color):
        move_type = "Random"
        list_of_moves = board.get_empty_points()

        return move_type, list_of_moves 

    """
    return the type of moves and set of moves to consider for a policy of 
    rulebased selection of moves
    """
    @staticmethod
    def rulebased_policy_moves(board, color):

        # # rule 5: random move
        # move_type, list_of_moves = GoBoardUtil.random_policy_moves(board, color)
        # return move_type, list_of_moves

        move_type = ""
        list_of_moves = []

        five_in_a_row_groups_pos = board.five_in_a_row_groups
        five_in_a_row_groups_color = []

        for group in five_in_a_row_groups_pos:
            temp = []
            for c in group:
                temp.append(board.get_color(c))
            five_in_a_row_groups_color.append(temp)

        # rule 1: win in one move
        if color == 1:
            for i in range(len(five_in_a_row_groups_color)):
                pattern = "".join([str(c) for c in five_in_a_row_groups_color[i]])

                if pattern in BLACK_WIN.keys():
                    for j in BLACK_WIN[pattern]:
                        list_of_moves.append(five_in_a_row_groups_pos[i][j])

        if color == 2:
            for i in range(len(five_in_a_row_groups_color)):
                pattern = "".join([str(c) for c in five_in_a_row_groups_color[i]])

                if pattern in WHITE_WIN.keys():
                    for j in WHITE_WIN[pattern]:
                        list_of_moves.append(five_in_a_row_groups_pos[i][j]) 

        if len(list_of_moves) > 0:
            move_type = "Win"

            return move_type, list_of_moves

        # rule 2: block the win of opponent
        if color == 2:
            for i in range(len(five_in_a_row_groups_color)):
                pattern = "".join([str(c) for c in five_in_a_row_groups_color[i]])

                if pattern in BLACK_WIN.keys():
                    for j in BLACK_WIN[pattern]:
                        list_of_moves.append(five_in_a_row_groups_pos[i][j])

        if color == 1:
            for i in range(len(five_in_a_row_groups_color)):
                pattern = "".join([str(c) for c in five_in_a_row_groups_color[i]])

                if pattern in WHITE_WIN.keys():
                    for j in WHITE_WIN[pattern]:
                        list_of_moves.append(five_in_a_row_groups_pos[i][j])  

        if len(list_of_moves) > 0:
            move_type = "BlockWin"

            return move_type, list_of_moves

        six_in_a_row_groups_pos = board.six_in_a_row_groups
        six_in_a_row_groups_color = []

        for group in six_in_a_row_groups_pos:
            temp = []
            # print(group)
            for c in group:
                temp.append(board.get_color(c))
            six_in_a_row_groups_color.append(temp)

        # rule 3: moves that creates an open four .XXXX.
        if color == 1:
            for i in range(len(six_in_a_row_groups_color)):
                pattern = "".join([str(c) for c in six_in_a_row_groups_color[i]])

                if pattern in OPEN_FOUR_BLACK_6.keys():
                    for j in OPEN_FOUR_BLACK_6[pattern]:
                        list_of_moves.append(six_in_a_row_groups_pos[i][j])

        if color == 2:
            for i in range(len(six_in_a_row_groups_color)):
                pattern = "".join([str(c) for c in six_in_a_row_groups_color[i]])

                if pattern in OPEN_FOUR_WHITE_6.keys():
                    for j in OPEN_FOUR_WHITE_6[pattern]:
                        list_of_moves.append(six_in_a_row_groups_pos[i][j]) 

        if len(list_of_moves) > 0:
            move_type = "OpenFour"

            return move_type, list_of_moves

        seven_in_a_row_groups_pos = board.seven_in_a_row_groups

        seven_in_a_row_groups_color = []

        for group in seven_in_a_row_groups_pos:
            temp = []
            # print(group)
            for c in group:
                temp.append(board.get_color(c))
            seven_in_a_row_groups_color.append(temp)

        # rule 4: moves that prevent the creation of an open four by opponent
        if color == 1:
            for i in range(len(seven_in_a_row_groups_color)):
                pattern = "".join([str(c) for c in seven_in_a_row_groups_color[i]])

                if pattern in PREVENT_OPEN_FOUR_WHITE_7.keys():
                    for j in PREVENT_OPEN_FOUR_WHITE_7[pattern]:
                        list_of_moves.append(seven_in_a_row_groups_pos[i][j])

        if color == 2:
            for i in range(len(seven_in_a_row_groups_color)):
                pattern = "".join([str(c) for c in seven_in_a_row_groups_color[i]])

                if pattern in PREVENT_OPEN_FOUR_BLACK_7.keys():
                    for j in PREVENT_OPEN_FOUR_BLACK_7[pattern]:
                        list_of_moves.append(seven_in_a_row_groups_pos[i][j]) 

        if len(list_of_moves) > 0:
            move_type = "BlockOpenFour"

            # remove duplicates
            list_of_moves = list(set(list_of_moves))

            return move_type, list_of_moves

        if color == 1:
            for i in range(len(six_in_a_row_groups_color)):
                pattern = "".join([str(c) for c in six_in_a_row_groups_color[i]])

                if pattern in PREVENT_OPEN_FOUR_WHITE_6.keys():
                    for j in PREVENT_OPEN_FOUR_WHITE_6[pattern]:
                        list_of_moves.append(six_in_a_row_groups_pos[i][j])

        if color == 2:
            for i in range(len(six_in_a_row_groups_color)):
                pattern = "".join([str(c) for c in six_in_a_row_groups_color[i]])

                if pattern in PREVENT_OPEN_FOUR_BLACK_6.keys():
                    for j in PREVENT_OPEN_FOUR_BLACK_6[pattern]:
                        list_of_moves.append(six_in_a_row_groups_pos[i][j])

        if len(list_of_moves) > 0:
            move_type = "BlockOpenFour"

            # remove duplicates
            list_of_moves = list(set(list_of_moves))

            return move_type, list_of_moves

        # rule 5: random move
        move_type, list_of_moves = GoBoardUtil.random_policy_moves(board, color)
        return move_type, list_of_moves

    @staticmethod
    def testing_2(board):
        list_of_groups = board.five_in_a_row_groups

        list_of_colors = []

        for group in list_of_groups:
            new_group = []
            for element in group:
                new_group.append(board.get_color(element))
            list_of_colors.append(new_group)

        print(list_of_colors)

    """
    generate the best move found based on "Flat Monte Carlo" algorithm and
    random/rulebased selection of moves
    """
    @staticmethod
    def generate_fmt_move(board, color, num_sim, timelimit):
        START_TIME = time.process_time()

        _, moves = GoBoardUtil.rulebased_policy_moves(board, color)
        num_moves = len(moves)

        current_move = 0
        number_of_simulations = 0

        wins = [0] * num_moves
        times_played = [0] * num_moves

        while (time.process_time() - START_TIME) < timelimit:
            # score[current_move] = GoBoardUtil.simulation(board.copy(), moves[current_move], color)

            board_copy = board.copy()

            # play the first move before the simulation
            board_copy.play_move(moves[current_move], color)

            result = board_copy.detect_five_in_a_row()

            while result == 0 and len(board_copy.get_empty_points()) > 0:
                to_play = board_copy.current_player

                # find a move to play based on policy (rulebased or random)
                _, list_of_moves = GoBoardUtil.rulebased_policy_moves(board_copy, to_play)
                np.random.shuffle(list_of_moves)

                move = list_of_moves[0]
                could = board_copy.play_move(move, to_play)

                result = board_copy.detect_five_in_a_row()

            if result == color:
                wins[current_move] += 1

            times_played[current_move] += 1

            number_of_simulations += 1
            current_move += 1

            if current_move >= num_moves:
                current_move = 0

        # for i in range(num_moves):
        #     score[i] = GoBoardUtil.simulation(board.copy(), moves[i], color, num_sim)

        best_move = None
        best_score = -1

        for i in range(num_moves):
            if times_played[i] > 0:
                s = wins[i] / times_played[i]
            else:
                s = 0

            if s > best_score:
                best_move = moves[i]
                best_score = s

        # print("simulations: ", number_of_simulations, "move: ", best_move, "score: ", best_score)

        return best_move

    """
    finishes the game until completion a given number of times using a given policy (rulebased or random) 
    returns an evaluation of the position after simulating it "num_sim" number of times
    this evaluation is based on the percentage of wins by "player" in position "board" and
    starting with move "first_move"
    """
    @staticmethod
    def simulation(board, first_move, player):
        # play the first move before the simulation
        board.play_move(first_move, player)

        # player's number of wins 
        wins = 0

        # simulate starting from child of root (first move)
        for i in range(num_sim):
            board_copy = board.copy()
            result = board_copy.detect_five_in_a_row()

            while result == 0 and len(board_copy.get_empty_points()) > 0:
                to_play = board_copy.current_player

                # find a move to play based on policy (rulebased or random)
                _, list_of_moves = GoBoardUtil.rulebased_policy_moves(board_copy, to_play)
                np.random.shuffle(list_of_moves)

                move = list_of_moves[0]
                could = board_copy.play_move(move, to_play)

                result = board_copy.detect_five_in_a_row()

            if result == player:
                wins += 1

        return (wins / num_sim)

    @staticmethod
    def generate_random_moves(board, use_eye_filter):
        """
        Return a list of random (legal) moves with eye-filtering.
        """
        empty_points = board.get_empty_points()
        color = board.current_player
        moves = []
        for move in empty_points:
            legal = not (
                use_eye_filter and board.is_eye(move, color)
            ) and board.is_legal(move, color)
            if legal:
                moves.append(move)
        return moves

    @staticmethod
    def opponent(color):
        return WHITE + BLACK - color

    @staticmethod
    def get_twoD_board(goboard):
        """
        Return: numpy array
        a two dimensional numpy array with the stones as the goboard.
        Does not pad with BORDER
        Rows 1..size of goboard are copied into rows 0..size - 1 of board2d
        """
        size = goboard.size
        board2d = np.zeros((size, size), dtype=GO_POINT)
        for row in range(size):
            start = goboard.row_start(row + 1)
            board2d[row, :] = goboard.board[start : start + size]
        return board2d

    @staticmethod
    def point_to_coord(point, boardsize):
        """
        Transform point given as board array index 
        to (row, col) coordinate representation.
        Special case: PASS is not transformed
        """
        if point == PASS:
            return PASS
        else:
            NS = boardsize + 1
            return divmod(point, NS)

    @staticmethod
    def format_point(move):
        """
        Return move coordinates as a string such as 'A1', or 'PASS'.
        """
        assert MAXSIZE <= 25
        column_letters = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
        if move == PASS:
            return "PASS"
        row, col = move
        if not 0 <= row < MAXSIZE or not 0 <= col < MAXSIZE:
            raise ValueError
        return column_letters[col - 1] + str(row)
