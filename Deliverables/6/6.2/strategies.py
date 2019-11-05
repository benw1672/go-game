# Import local dependencies.
from constants import *
from rule_checker import RuleChecker
import utils


class SimpleStrategy(object):
    def execute(self, boards, stone):
        return select_simple_move(stone, boards)


class PrioritizeCaptureStrategy(object):
    def __init__(self, max_search_depth=1):
        self.max_search_depth = max_search_depth

    def execute(self, stone, boards):
        return select_move_prioritizing_capture(stone, boards, self.max_search_depth)


def select_simple_move(player_stone_color, boards):
    '''
    input: boards
    output:
        if there is a move that self can make,
            returns a point with the lowest column index,
            and then with the lowest row index
        if there isn't,
            returns a string "pass"
    '''
    rc = RuleChecker()
    for point, maybe_stone in iter(boards[0]):
        if maybe_stone == EMPTY:
            if rc.check_legality(player_stone_color, point, boards):
                return str(point)
    return "pass"


def select_move_prioritizing_capture(player_stone_color, boards, depth):
    '''
    moves =
    [
        [point1, point2, ...] (from oldest to newest)
        ...
    ]
    [[(1,1)], []]
    '''
    rc = RuleChecker()
    most_recent_board = boards[0]
    opponent_stone_color = utils.get_opponent_stone_color(player_stone_color)
    moves = []
    if depth == 1:
        chains = most_recent_board.get_all_chains()
        opponent_chains = [chain for chain in chains if chain.stone_color == opponent_stone_color]
        for chain in opponent_chains:
            if len(chain.liberties) == 1:
                liberties = list(chain.liberties)
                if rc.check_legality(player_stone_color, liberties[0], boards):
                    moves.append(liberties[0])
    if depth > 1:
        # Idea: define new_move as [point()]
        # all_moves = generate_all_moves_that_d
        # return select_simple_move(boards)
        raise NotImplementedError()
    if moves:
        return sorted(moves)
    else:
        return select_simple_move(player_stone_color, boards)