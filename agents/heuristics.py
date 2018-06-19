
def score(board):
    return board.get_score(board.current_player)


def boxes_left(board):
    dimensions = board.get_merged_dimensions()
    result = 0
    for dim in dimensions:
        result += 100 / dim.count(0) if dim.count(0) > 0 else 0
    return result
