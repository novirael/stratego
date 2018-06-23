import pygame
from functools import wraps

from board import RED_PLAYER, GREEN_PLAYER, StrategoBoard

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

TOOLBAR_HEIGHT = 30
WINDOW_WIDTH = 800
WINDOW_HEIGHT = WINDOW_WIDTH + TOOLBAR_HEIGHT

clock = pygame.time.Clock()


def mouse_click(view_func):
    def _decorator(self, *args, **kwargs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.board.is_over:
                    view_func(self, *args, **kwargs)
                break
        return True
    return wraps(view_func)(_decorator)


def any_event(view_func):
    def _decorator(self, *args, **kwargs):
        if not self.board.is_over:
            view_func(self, *args, **kwargs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    return wraps(view_func)(_decorator)


class Game(object):
    grid_size = 40
    margin = 2
    color_mapping = {
        RED_PLAYER: RED,
        GREEN_PLAYER: GREEN,
        0: WHITE
    }

    def __init__(self, board_size=7):
        self.board = StrategoBoard(board_size)

        margins = board_size + 1 * self.margin
        self.grid_size = (WINDOW_WIDTH - margins) / board_size

        pygame.init()
        pygame.display.set_caption("Stratego")

        self.window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.window.fill(BLACK)

        self.font = pygame.font.SysFont("arial", 15)
        self.font.set_bold(True)

    def __delete__(self, instance):
        pygame.quit()
        return super(Game, self).__delete__(instance)

    @mouse_click
    def check_events(self):
        raise NotImplementedError

    def _get_box_coords(self, pos):
        event_x, event_y = pos
        x = int(event_x / (self.grid_size + self.margin))
        y = int((event_y - TOOLBAR_HEIGHT) / (self.grid_size + self.margin))
        # print(
        #     "Event (x,y): ({},{})\n"
        #     "Grid size: {}\n"
        #     "Coords (x,y): ({},{})".format(
        #         event_x, event_y, self.grid_size, x, y
        #     )
        # )
        return x, y

    def draw_toolbar(self):
        rect = pygame.Rect(0, 0, WINDOW_WIDTH, TOOLBAR_HEIGHT)
        pygame.draw.rect(self.window, WHITE, rect)

        self.window.blit(
            self.font.render(
                "Player {}".format(self.board.current_player),
                True,
                self.color_mapping[self.board.current_player]
            ),
            (100, int((TOOLBAR_HEIGHT - self.font.get_height()) / 2))
        )

        for i, player in enumerate([RED_PLAYER, GREEN_PLAYER], start=2):
            self.window.blit(
                self.font.render(
                    "Score player {}: {}".format(player, self.board.get_score(player)),
                    True,
                    self.color_mapping[player]
                ),
                (200 * i, int((TOOLBAR_HEIGHT - self.font.get_height()) / 2))
            )

    def draw_board(self):
        for y in range(self.board.size):
            for x in range(self.board.size):
                rect = pygame.Rect(
                    x * (self.grid_size + self.margin),
                    TOOLBAR_HEIGHT + y * (self.grid_size + self.margin),
                    self.grid_size,
                    self.grid_size,
                )
                value = self.board._state[y*self.board.size + x]
                pygame.draw.rect(self.window, self.color_mapping[value], rect)

        if self.board.is_over:
            self._draw_game_over()

    def _draw_game_over(self):
        names = {
            RED_PLAYER: "RED",
            GREEN_PLAYER: "GREEN",
            0: "EVERYONE"
        }
        message = "The winner is {}.".format(names[self.board.winner])
        msg_width, msg_height = self.font.size(message)
        self.window.blit(
            self.font.render(message, True, WHITE),
            (
                int((WINDOW_WIDTH - msg_width) / 2),
                int((WINDOW_HEIGHT - TOOLBAR_HEIGHT - msg_height) / 2)
            )
        )

    @staticmethod
    def refresh():
        pygame.display.flip()
        clock.tick(30)


class PVPGame(Game):
    """
    Player vs player game.
    """
    @mouse_click
    def check_events(self):
        pos = pygame.mouse.get_pos()
        coords = self._get_box_coords(pos)
        self.board.update(coords)


class PVBGame(Game):
    """
    Player vs bot game.
    """
    def __init__(self, bot_agent, board_size=7, bot_player=GREEN_PLAYER):
        self.bot_agent = bot_agent
        self.bot_player = bot_player
        super(PVBGame, self).__init__(board_size=board_size)

    @mouse_click
    def check_events(self):
        # human move
        if self.board.current_player != self.bot_player:
            pos = pygame.mouse.get_pos()
            coords = self._get_box_coords(pos)
            self.board.update(coords)

            # bot move if humar user did correct move
            if self.board.current_player == self.bot_player:
                coords = self.bot_agent.best_move(self.board)
                self.board.update(coords)


class BVBGame(Game):
    """
    Bot vs bot game.
    """
    def __init__(self, agent_alice, agent_bob, board_size=7):
        self.agent_alice = agent_alice
        self.agent_bob = agent_bob
        super(BVBGame, self).__init__(board_size=board_size)

    @any_event
    def check_events(self):
        if self.board.current_player == RED_PLAYER:
            coords = self.agent_alice.best_move(self.board)
            self.board.update(coords)
        elif self.board.current_player == GREEN_PLAYER:
            coords = self.agent_bob.best_move(self.board)
            self.board.update(coords)
