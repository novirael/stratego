from agents.agent import Player, INF
from agents.heuristics import score, boxes_left


class AgentJonh(Player):

    def evaluate(self, board_old, board_new):
        if board_old.is_over:
            return -INF
        if board_new.is_over:
            return INF
        return sum([
            score(board_new) - score(board_old),
        ])

