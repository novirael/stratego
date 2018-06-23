#!/usr/bin/python
import argparse

import sys

from agents.fullstack import AgentFullStack
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
    parser.add_argument("--games", type=int, default=3)

    args = parser.parse_args()

    if args.mode == PLAYER_VS_PLAYER:
        game = PVPGame(board_size=args.board_size)
    elif args.mode == PLAYER_VS_BOT:
        game = PVBGame(board_size=args.board_size, bot_agent=AgentFullStack())
    elif args.mode == BOT_VS_BOT:
        game = BVBGame(
            board_size=args.board_size,
            agent_alice=AgentMerlin(depth=5),
            agent_bob=AgentJonh(depth=5)
        )
    elif args.mode == TEST_MODE:
        test(args.board_size, args.games)
        sys.exit()

    running = True
    while running:
        game.draw_toolbar()
        game.draw_board()
        game.refresh()
        running = game.check_events()

    del game
