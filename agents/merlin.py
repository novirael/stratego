from agents.agent import Player, INF
from agents.heuristics import boxes_left


class AgentMerlin(Player):

    def evaluate(self, board_old, board_new):
        if board_old.is_over:
            return -INF
        if board_new.is_over:
            return INF
        return sum([
            boxes_left(board_new) - boxes_left(board_old),
        ])

