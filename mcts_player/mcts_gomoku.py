"""
MCTS implementation for the game of Gomoku.
Part of the code was adapted from Go5 code from lecture:
    https://jrwright.info/cmput455/python/index.html#Go4

"""

import numpy as np
import time
import patterns

from board_util import GoBoardUtil, BLACK, WHITE, EMPTY
from gtp_connection import point_to_coord, format_point

def uct_val(node, child, exploration, max_flag):
    if child._visits == 0:
        return float("inf")
    if max_flag:
        return float(child._black_wins) / child._visits + exploration * np.sqrt(
            np.log(node._visits) / child._visits
        )
    else:
        return float(child._white_wins) / child._visits + exploration * np.sqrt(
            np.log(node._visits) / child._visits
        )

class TreeNode():
    def __init__(self, parent):
        self._parent = parent
        self._visits = 0
        self._black_wins = 0
        self._white_wins = 0
        self._expanded = False

        # move used to get to this TreeNode
        self._move = None 

        # key: move from node position, value: child TreeNode
        self._children =  {}

    """
    expand (add children) the TreeNode with moves
    """
    def expand(self, board, color):
        # get all legal moves (can also select moves based on policy)
        _, moves = patterns.rulebased_policy_moves(board, color)

        for move in moves:
            self._children[move] = TreeNode(self)
            self._children[move]._move = move 

        self._expanded = True 

    """
    select move among children with highest UCT value
    returns move, next_node
    """
    def select(self, exploration, max_flag):
        best_move = None 
        next_node = None
        best_value = -1

        for key in self._children:
            temp_val = uct_val(self, self._children[key], exploration, max_flag)

            if temp_val > best_value:
                best_move = key 
                next_node = self._children[key]
                best_value = temp_val

        return best_move, next_node

    """
    update this TreeNode based on leaf TreeNode evaluation
    """
    def update(self, leaf_value):
        if leaf_value == BLACK:
            self._black_wins += 1
        elif leaf_value == WHITE:
            self._white_wins += 1
        elif leaf_value == EMPTY:
            self._black_wins += 0.5
            self._white_wins += 0.5
        else:
            raise Exception

        self._visits += 1

    """
    update all ancestors recursively
    """
    def update_recursive(self, leaf_value):
        if self._parent:
            self._parent.update_recursive(leaf_value)

        self.update(leaf_value)

    def is_leaf(self):
        return self._children == {}

    def is_root(self):
        return self._parent is None 

class MCTS():
    def __init__(self):
        self._root = TreeNode(None) 
        self._to_play = BLACK
        self.exploration = None

    """
    run iterations and find a move to play
    """
    def get_move(self, board, color, exploration, timelimit):
        START_TIME = time.process_time()

        if self._to_play != color:
            self.update(board.last_move)
            assert self._to_play == color

        self.exploration = exploration

        # run iterations until time limit
        while (time.process_time() - START_TIME) < timelimit:
            board_copy = board.copy()
            d = self._playout(board_copy, color)

        # select move with the most visits
        moves_ls = [
            (move, node._visits) for move, node in self._root._children.items()
        ]
        if not moves_ls:
            return None
        moves_ls = sorted(moves_ls, key=lambda i: i[1], reverse=True)
        move = moves_ls[0]

        # print("     best: ", point_to_coord(move[0], board.size))
        # # print("     all: ", self._root._children)
        # for key in self._root._children:
        #     the_move = point_to_coord(key, board.size)
        #     the_value = uct_val(self._root, self._root._children[key], 0.4, (color == BLACK))
        #     print("     move: ", the_move, " value: ", the_value, " visited: ", self._root._children[key]._visits)

        return move[0]

    """
    run an iteration of the MCTS: 
        from the root, select best child until a leaf node is reached
        expand the leaf node and select new leaf node
        evaluate leaf node using simulations until the end of the game
        back propagate the evaluation 

    note: pass a copy of the board
    """
    def _playout(self, board, color):
        node = self._root

        if not node._expanded:
            node.expand(board, color)

        # search
        while not node.is_leaf():
            # determine min-max player
            max_flag = (color == BLACK)

            # greedily selects next node 
            move, next_node = node.select(self.exploration, max_flag)

            board.play_move(move, color)
            color = GoBoardUtil.opponent(color)

            node = next_node

        assert node.is_leaf()
        assert board.current_player == color

        # expand
        if not node._expanded:
            node.expand(board, color)

        # determine min-max player
        max_flag = (color == BLACK)
        # greedily selects next node 
        move, next_node = node.select(self.exploration, max_flag)

        if next_node is not None:
            board.play_move(move, color)
            color = GoBoardUtil.opponent(color)
            node = next_node
            assert node.is_leaf()
            assert board.current_player == color

        # rollout/simulation
        leaf_value = self._simulate(board, color)

        # backpropagate
        node.update_recursive(leaf_value)

    """
    given a state and player, simulate the game until it finishes and return 
    the final score
    """
    def _simulate(self, board, color):
        result = board.detect_five_in_a_row()

        while result == 0 and len(board.get_empty_points()) > 0:
            to_play = board.current_player

            # find a move to play based on policy (rulebased or random)
            _, moves = patterns.rulebased_policy_moves(board, to_play)

            move = moves[np.random.randint(0, len(moves))]
            board.play_move(move, to_play)

            result = board.detect_five_in_a_row()

        return result 

    """
    update after a move has been played
    update the root of MCTS after a move has been played. this helps maintain
    knowledge we have about suctrees of children of root
    """
    def update(self, last_move):
        if last_move in self._root._children:
            self._root = self._root._children[last_move]
        else:
            # print("current MCTS discarded")
            self._root = TreeNode(None)

        self._root._parent = None
        self._to_play = GoBoardUtil.opponent(self._to_play)










    

    

        