import math
import numpy as np

from copy import deepcopy, copy

RED_PLAYER = 1
GREEN_PLAYER = -1


def _get(state, x, y):
    l = int(math.sqrt(len(state)))
    return state[y*l + x]


class StrategoBoard(object):
    current_player = RED_PLAYER
    score_red = 0
    score_green = 0
    is_over = False

    def __init__(self, size=5, state=None):
        self.size = size
        if state:
            self._state = state
        else:
            self._state = [0 for _ in range(size**2)]

    def __iter__(self):
        for i in self._state:
           yield i

    def __deepcopy__(self, memo):
        id_self = id(self)
        _copy = memo.get(id_self)
        if _copy is None:
            _copy = StrategoBoard(
                state=copy(self._state),
                size=self.size
            )
            _copy.current_player = self.current_player
            _copy.score_red = self.score_red
            _copy.score_green = self.score_green
        return _copy

    def get_score(self, player):
        assert player in (RED_PLAYER, GREEN_PLAYER), "Unknown player."
        return self.score_red if player == RED_PLAYER else self.score_green

    def set_score(self, player, value, place):
        assert player in (RED_PLAYER, GREEN_PLAYER), "Unknown player."
        if player == RED_PLAYER:
            self.score_red += value
        else:
            self.score_green += value

        # print("Added {} points for player {} with {}".format(value, player, place))

    @property
    def winner(self):
        if self.is_over:
            if self.score_red > self.score_green:
                return RED_PLAYER
            elif self.score_red < self.score_green:
                return GREEN_PLAYER
            else:
                return 0

    def get_moves(self):
        return [
            (x,y)
            for y in range(self.size)
            for x in range(self.size)
            if self._state[y*self.size + x] == 0
        ]

    def peek_move(self, coors):
        board = deepcopy(self)
        board.update(coors)
        return board

    def update(self, coors):
        x, y = coors
        if not self.is_over and self._is_available_tick(x, y):
            self._tick_the_box(x, y)
            self._update_score(x, y)
            self._switch_player()

        self.is_over = not bool(self.get_moves())

    def _is_available_tick(self, x, y):
        return self._state[y*self.size + x] == 0

    def _tick_the_box(self, x, y):
        self._state[y*self.size + x] = self.current_player

    def _update_score(self, x, y):
        board_size = self.size
        matrix = np.array(self._state)
        matrix.shape = (self.size, self.size)

        # add row sum
        current_row = self._state[y*self.size:self.size+(y*self.size)]
        if not current_row.count(0):
            self.set_score(self.current_player, board_size, 'row')

        # add column sum
        current_col = [self._state[_y*self.size] for _y in range(board_size)]
        if not current_col.count(0):
            self.set_score(self.current_player, board_size, 'col')

        # add first diagonal sum
        positive_diagonal = matrix[::-1, :].diagonal(-board_size + 1 + x + y).tolist()
        if not positive_diagonal.count(0):
            self.set_score(self.current_player, len(positive_diagonal), 'diag_pos')

        # add second diagonal sum
        negative_diagonal = matrix.diagonal(x - y).tolist()
        if not negative_diagonal.count(0):
            self.set_score(self.current_player, len(negative_diagonal), 'diag_neg')

        # print(
        #     "Current row: {}\n"
        #     "Current col: {}\n"
        #     "Positive diagonal: {}\n"
        #     "Negative diagonal: {}".format(
        #         current_row,
        #         current_col,
        #         positive_diagonal,
        #         negative_diagonal
        #     )
        # )

    def _switch_player(self):
        self.current_player *= -1

    def get_merged_dimensions(self):
        dimensions = []

        matrix = np.array(self._state)
        matrix.shape = (self.size, self.size)

        # add rows
        dimensions.extend(matrix.tolist())
        # add columns
        dimensions.extend(matrix.transpose().tolist())
        # add diagonals
        dimensions.extend(
            matrix.diagonal(i).tolist()
            for i in range(matrix.shape[1] - 1, -matrix.shape[0], -1)
        )
        dimensions.extend(
            matrix[::-1,:].diagonal(i).tolist()
            for i in range(-matrix.shape[0] + 1, matrix.shape[1])
        )

        return dimensions
