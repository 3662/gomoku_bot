#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from board import GoBoard

from mcts_gomoku import *

class Gomoku4():
    def __init__(self):
        """
        "Flat Monte Carlo" Gomoku player that selects moves based on simulation from 
        the set of legal moves.
        Passes/resigns only at the end of the game.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "GomokuAssignment4"
        self.version = 4.0

        self.mcts = MCTS()

    def get_move(self, board, color, timelimit):
        # return GoBoardUtil.generate_fmt_move(board, color, self.number_of_simulations, timelimit)
        move = self.mcts.get_move(board, color, 0.1, timelimit)
        self.mcts.update(move)

        return move


def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(Gomoku4(), board)
    con.start_connection()


if __name__ == "__main__":
    run()
