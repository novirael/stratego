#!/usr/bin/python
import time

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
        Blue wins: {score_blue}
        Unresolved: {score_unresolved}
        Red thinking time (avg): {time_red}
        Blue thinking time (avg): {time_blue}
    """

    def __init__(self, board_size, red_player, green_player, games=5):
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
        board = StrategoBoard(self.board_size)
        turn = 0

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

        print("Winner is: {winner}\nRed score: {score_red}\nGreen score: {score_green}".format(
            winner='RED' if board.winner == 1 else 'GREEN' if board.winner == -1 else 'UNRESOLVED',
            score_red=board.score_red,
            score_green=board.score_green,
        ))

    def print_summary(self):
        score = self.stats["score"]
        thinking_time = self.stats["thinking_time"]

        summary = self.summary_text.format(
            games=self.games_count,
            score_red=score.count(RED_PLAYER),
            time_red=sum(thinking_time[RED_PLAYER]) / len(thinking_time[RED_PLAYER]),
            score_blue=score.count(GREEN_PLAYER),
            time_blue=sum(thinking_time[GREEN_PLAYER]) / len(thinking_time[GREEN_PLAYER]),
            score_unresolved=score.count(0)
        )
        print(summary)


def test(board_size):
    tests = [
        TestAnalyzer(board_size, AgentJonh(), AgentRandom()),
    ]
    for t in tests:
        t.run()
