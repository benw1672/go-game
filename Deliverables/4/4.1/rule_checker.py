# Import nonlocal dependencies.
import json, sys, os, typing, copy

# Import local dependencies.
from point import Point
from board import Board
from constants import *
import utils


def get_scores(board):
    '''
    input: board
    output: a dictionary, with keys "B" and "W" and values respective scores
    '''
    scores = {BLACK: 0, WHITE: 0}
    for point, maybe_stone in iter(board):
        if maybe_stone in STONES:
            scores[maybe_stone] += 1
        else:
            b_reachable = board.is_reachable(point, BLACK)
            w_reachable = board.is_reachable(point, WHITE)
            if b_reachable and not w_reachable:
                scores[BLACK] += 1
            elif w_reachable and not b_reachable:
                scores[WHITE] += 1
    return scores



def is_move_legal(stone, move):
    """
    input: stone, point, boards
    output: True or False
    """
    if move == PASS:
        return True
    str_point, json_boards = move
    point = Point.from_str(str_point)
    boards = [Board(json_board) for json_board in json_boards]
    if len(boards) == 1:
        return _check_legality_for_boards_of_length_one(stone, point, boards)
    elif len(boards) == 2:
        return _check_legality_for_boards_of_length_two(stone, point, boards)
    else:
        return _check_legality_for_boards_of_length_three(stone, point, boards)


def _check_legality_for_boards_of_length_one(stone, point, boards):
    return stone == BLACK and boards[0].is_fully_empty()


def _check_legality_for_boards_of_length_two(stone, point, boards):
    # Check that first board is legal.
    if stone != WHITE:
        return False
    if not boards[1].is_fully_empty():
        return False
    # Check that the progression from first to second board is legal.
    maybe_turn = _get_turn_if_legal_progression(boards[0], boards[1])
    if maybe_turn == None:
        return False
    # check new board validity
    maybe_board = _get_board_if_valid_move(boards[0], stone, point)
    if maybe_board == None:
        return False
    if not _is_valid_turns([maybe_turn,stone]):
        return False
    return True


def _check_legality_for_boards_of_length_three(stone, point, boards):
    # check history validity
    maybe_turn_1_2 = _get_turn_if_legal_progression(boards[1], boards[2])
    if maybe_turn_1_2 == None:
        return False
    maybe_turn_0_1 = _get_turn_if_legal_progression(boards[0], boards[1])
    if maybe_turn_0_1 == None:
        return False

    # edge case where the last board is empty
    if boards[2].is_fully_empty():
        # cannot pass two times in a row
        if maybe_turn_1_2 == PASS and maybe_turn_0_1 == PASS:
            return False
        if [maybe_turn_1_2, maybe_turn_0_1, stone] not in \
            [[BLACK, WHITE, BLACK],
            [BLACK, PASS, BLACK],
            [WHITE, BLACK, WHITE],
            [WHITE, PASS, WHITE],
            [PASS, WHITE, BLACK],
            ]:
            return False

    # checking if the board has captured stones
    for board in boards:
        if _get_captured_chains(board):
            return False

    if not _is_valid_turns([maybe_turn_1_2, maybe_turn_0_1, stone]):
        return False

    # check new board validity
    maybe_board = _get_board_if_valid_move(boards[0], stone, point)
    if maybe_board == None:
        return False

    #Check if Ko rule is violated, at this point no consecutive two passes have been made
    if boards[0] == boards[2]:
        return False
    if maybe_board == boards[1]:
        return False
    return True


def _get_points_with_added_stones(new_board, old_board):
    points_with_added_stones = []
    for point, new_maybe_stone in iter(new_board):
        if new_maybe_stone in STONES and old_board[point] == EMPTY:
            points_with_added_stones.append(point)
    return points_with_added_stones


def _get_turn_if_legal_progression(new_board, old_board):
    points_with_added_stones = _get_points_with_added_stones(new_board, old_board)
    # Handle case where it's a pass.
    if len(points_with_added_stones) == 0:
        if new_board == old_board:
            return PASS
    # Handle case where one new stone was placed.
    elif len(points_with_added_stones) == 1:
        point = points_with_added_stones[0]
        added_stone = new_board[point]
        legal_new_maybe_board = _get_board_if_valid_play(old_board, added_stone, point)
        if legal_new_maybe_board and legal_new_maybe_board == new_board:
            return added_stone
    # Handle case where multiple new stones were placed.
    return None


def _get_board_if_valid_play(board, player_stone, point):
    """
    input: board, stone that has the turn,
            dictionary of keys "stone" and "point" and values their values
    output: maybe board (i.e. board or None)
    """
    new_board = copy.deepcopy(board)
    # Step 1: Place a stone.
    if board.is_occupied(point):
        return None
    new_board.place(player_stone, point)
    # Step 2: Remove any stones of opponent's color that have no liberties.
    opponent_stone = utils.get_opponent_stone_color(player_stone)
    for chain in _get_captured_chains(new_board):
        if chain.stone_color == opponent_stone:
            for pt in chain.connected_points:
                new_board.remove(opponent_stone, pt)
    # Step 3: If there exists any of own color that have no liberties, self-capture has occured.
    if  _get_captured_chains(new_board):
        return None
    return new_board


def _is_valid_turns(sequence_of_turns):
    """
    sequence of turns is a list of stones that played,
        in the order from the oldest to the latest
    """
    return sequence_of_turns in \
        [[BLACK, WHITE, BLACK],
        [WHITE, BLACK, WHITE],
        [PASS, BLACK, WHITE],
        [PASS, WHITE, BLACK],
        [BLACK, PASS, BLACK],
        [WHITE, PASS, WHITE],
        [BLACK, WHITE],
        [PASS, WHITE]]


def _get_captured_chains(board):
    captured_chains = []
    all_chains = board.get_all_chains()
    for chain in all_chains:
        if len(chain.liberties) == 0:
            captured_chains.append(chain)
    return captured_chains
