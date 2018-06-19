"""
A checkers agent that picks a random move
"""

import random


class AgentRandom():
    def best_move(self, board):
        return random.choice(board.get_moves())
