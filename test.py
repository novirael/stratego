#!/usr/bin/python
import time

from agents.fullstack import AgentFullStack
from agents.merlin import AgentMerlin
from agents.rob import AgentRob
from board import GREEN_PLAYER, StrategoBoard
from board import RED_PLAYER
from agents.rand import AgentRandom
from agents.john import AgentJonh


class TestAnalyzer():
    """
    Test class
    """
    summary_text = """
        Games played: {games}
        Red wins: {score_red}
        Green wins: {score_green}
        Unresolved: {score_unresolved}
        Red thinking time (avg): {time_red_avg}
        Red thinking time (sum): {time_red_sum}
        Red thinking time: {time_red}
        Green thinking time (avg): {time_green_avg}
        Green thinking time (sum): {time_green_sum}
        Green thinking time: {time_green}
    """

    def __init__(self, board_size, red_player, green_player, games=3):
        self.board_size = board_size
        self.players = {
            RED_PLAYER: red_player,
            GREEN_PLAYER: green_player,
        }
        self.games_count = games
        self.stats = {
            "played_rounds": 0,
            "score": [],
            "thinking_time": {RED_PLAYER: [], GREEN_PLAYER: []},
        }

    def run(self):
        number = 0
        try:
            for number in range(1, self.games_count + 1):
                print("\n###### GAME %d" % number)
                self.run_single_game()
        except KeyboardInterrupt:
            print("Test interrupted on %d" % number)

        self.print_summary()

    def run_single_game(self):
        board = StrategoBoard(size=self.board_size)
        turn = 0
        start_time_overall = time.time()

        while not board.is_over:
            turn += 1

            if turn % 20 == 0:
                print("Over %d turns played" % turn)

            for player_id, player in self.players.items():
                while not board.is_over and board.current_player == player_id:
                    start_time = time.time()
                    move = player.best_move(board)
                    self.stats["thinking_time"][player_id].append(time.time() - start_time)
                    board.update(move)

        self.stats["score"].append(board.winner)
        self.stats["played_rounds"] += turn

        overall_time = time.time() - start_time_overall

        print(
            "Winner is: {winner}\n"
            "Red score: {score_red}\n"
            "Green score: {score_green}\n"
            "Overall time: {overall_time}".format(
                winner='RED' if board.winner == 1 else 'GREEN' if board.winner == -1 else 'UNRESOLVED',
                score_red=board.score_red,
                score_green=board.score_green,
                overall_time=str(overall_time),
            )
        )

    def print_summary(self):
        score = self.stats["score"]
        thinking_time = self.stats["thinking_time"]

        summary = self.summary_text.format(
            games=self.games_count,
            score_red=score.count(RED_PLAYER),
            time_red=", ".join([str(t) for t in thinking_time[RED_PLAYER]]),
            time_red_avg=sum(thinking_time[RED_PLAYER]) / len(thinking_time[RED_PLAYER]),
            time_red_sum=sum(thinking_time[RED_PLAYER]),
            score_green=score.count(GREEN_PLAYER),
            time_green=", ".join([str(t) for t in thinking_time[GREEN_PLAYER]]),
            time_green_avg=sum(thinking_time[GREEN_PLAYER]) / len(thinking_time[GREEN_PLAYER]),
            time_green_sum=sum(thinking_time[GREEN_PLAYER]),
            score_unresolved=score.count(0)
        )
        print(summary)


def test(board_size, games):
    tests = [
        # TestAnalyzer(
        #     board_size,
        #     AgentRandom(),
        #     AgentFullStack(depth=5),
        # ),
        TestAnalyzer(
            board_size,
            AgentJonh(depth=5),
            AgentFullStack(depth=5),
            games=games,
        ),
        TestAnalyzer(
            board_size,
            AgentMerlin(depth=5),
            AgentFullStack(depth=5),
            games=games,
        ),
        TestAnalyzer(
            board_size,
            AgentRob(depth=5),
            AgentFullStack(depth=5),
            games=games,
        ),

    ]
    for t in tests:
        t.run()
