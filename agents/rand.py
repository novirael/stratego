"""
A checkers agent that picks a random move
"""

import random


class AgentRandom():
    def best_move(self, board):
        # for move in board.get_moves():
        #     if board._is_available_tick(move[0],move[1]):
        #         return move

        return random.choice(board.get_moves())
