"""
Helpers and evaluation funcions.
"""
import sys

INF = sys.maxsize


class Player:
    search_methods = ['min_max', 'alpha_beta', 'nega_max']
    search_method_name = search_methods[-1]

    def __init__(self, depth=5, search_with='alpha_beta'):
        self.depth = depth
        self.search_method_name = search_with

    def best_move(self, board):
        def search(move):
            board_new = board.peek_move(move)
            color = 1 if board_new.current_player == board.current_player else -1
            attributes = [board, board_new, self.depth, color]
            if self.search_method_name in ('alpha_beta', 'nega_max'):
                attributes += [-INF, INF]
            return getattr(self, self.search_method_name)(*attributes)

        available_moves = board.get_moves()
        return max(available_moves, key=search)

    def evaluate(self, board_old, board_new):
        raise NotImplementedError

    def min_max(self, board_old, board_new, depth, color):
        if depth == 0 or board_new.is_over:
            return self.evaluate(board_old, board_new) * color

        best_value = -INF if color == 1 else INF

        for move in board_new.get_moves():
            board = board_new.peek_move(move)
            if board.current_player != board_new.current_player:
                val = self.min_max(board_new, board, depth - 1, -color)
            else:
                val = self.min_max(board_new, board, depth,  color)

            if color == 1:
                best_value = max(val, best_value)
            else:
                best_value = min(val, best_value)

        return best_value

    def alpha_beta(self, board_old, board_new, depth, color, alpha, beta):
        if depth == 0 or board_new.is_over:
            return self.evaluate(board_old, board_new) * color

        best_value = -INF if color == 1 else INF

        for move in board_new.get_moves():
            board = board_new.peek_move(move)
            if board.current_player != board_new.current_player:
                val = self.alpha_beta(board_new, board, depth - 1, -color, -alpha, -beta)
            else:
                val = self.alpha_beta(board_new, board, depth, color, alpha, beta)

            if color == 1:
                best_value = max(val, best_value)
                alpha = max(best_value, alpha)
            else:
                best_value = min(val, best_value)
                beta = min(best_value, beta)

            if alpha >= beta:
                break

        return best_value

    def nega_max(self, board_old, board_new, depth, color, alpha, beta):
        if depth == 0 or board_new.is_over:
            return self.evaluate(board_old, board_new) * color

        best_value = -INF

        for move in board_new.get_moves():
            board = board_new.peek_move(move)
            if board.current_player != board_new.current_player:
                val = -self.nega_max(board_new, board, depth - 1, -color, -beta, -alpha)
            else:
                val = self.nega_max(board_new, board, depth, color, alpha, beta)

            best_value = max(best_value, val)
            alpha = max(alpha, val)
            if alpha >= beta:
                break

        return best_value
