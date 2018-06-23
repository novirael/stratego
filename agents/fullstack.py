from agents.agent import Player, INF
from agents.heuristics import score, boxes_left, bonus_check


class AgentFullStack(Player):

    def evaluate(self, board_old, board_new):
        if board_old.is_over:
            return -INF
        if board_new.is_over:
            return INF
        return sum([
            score(board_new) - score(board_old),
            boxes_left(board_new) - boxes_left(board_old),
            bonus_check(board_new) - bonus_check(board_old),

        ])
