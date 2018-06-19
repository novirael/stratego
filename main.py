#!/usr/bin/python
import argparse

import sys

from agents.john import AgentJonh
from agents.merlin import AgentMerlin
from agents.rand import AgentRandom
from game import BVBGame, PVBGame, PVPGame
from test import test

PLAYER_VS_PLAYER = "pvp"
PLAYER_VS_BOT = "pvb"
BOT_VS_BOT = "bvb"
TEST_MODE = "test"


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Stratego game")
    parser.add_argument('mode', type=str, choices=[
        PLAYER_VS_PLAYER, PLAYER_VS_BOT, BOT_VS_BOT, TEST_MODE])
    parser.add_argument("--board_size", type=int, default=5)

    args = parser.parse_args()

    if args.mode == PLAYER_VS_PLAYER:
        game = PVPGame(board_size=3)
    elif args.mode == PLAYER_VS_BOT:
        game = PVBGame(board_size=4, bot_agent=AgentJonh())
    elif args.mode == BOT_VS_BOT:
        game = BVBGame(
            board_size=5,
            agent_alice=AgentRandom(),
            agent_bob=AgentJonh(depth=5)
        )
    elif args.mode == TEST_MODE:
        test(args.board_size)
        sys.exit()

    running = True
    while running:
        game.draw_toolbar()
        game.draw_board()
        game.refresh()
        running = game.check_events()

    del game
