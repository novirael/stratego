from agents.agent import Player, INF
from agents.heuristics import bonus_check


class AgentRob(Player):

    def evaluate(self, board_old, board_new):
        if board_old.is_over:
            return -INF
        if board_new.is_over:
            return INF
        return sum([
            bonus_check(board_new) - bonus_check(board_old),
        ])

