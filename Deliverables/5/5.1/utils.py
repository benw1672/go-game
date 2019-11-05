# Import local dependencies.
from constants import *
from point import Point


# Utility functions for Point.
def is_row_index_in_bounds(x: int):
    return 0 < x <= BOARD_ROW_LENGTH


def is_col_index_in_bounds(y: int):
    return 0 < y <= BOARD_COL_LENGTH


def point_in_bounds(point):
    return 0 < point.x <= BOARD_ROW_LENGTH \
        and 0 < point.y <= BOARD_COL_LENGTH


def get_valid_neighbors(point):
    x, y = point
    neighbors = [Point(x-1, y), 
                 Point(x, y-1), 
                 Point(x+1, y), 
                 Point(x, y+1)]
    return [p for p in neighbors if point_in_bounds(p)]


# Utility functions for Board.
def validate_board(board):
    if len(board) != BOARD_ROW_LENGTH:
        raise ValueError("Incorrect row numbers. Got: " + str(len(board)))
    for i in board:
        if len(i) != BOARD_COL_LENGTH:
            raise ValueError("Incorrect column numbers.")
    for row in range(BOARD_ROW_LENGTH):
        for col in range(BOARD_COL_LENGTH):
            if board[row][col] not in MAYBE_STONES:
                raise ValueError("Incorrect stone type")


# Utility functions for stone.
def is_valid_stone(stone):
    return stone in STONES


def is_valid_maybe_stone(maybe_stone):
    return maybe_stone in MAYBE_STONES


# General utility functions.
def all_points():
    for i in range(1, BOARD_ROW_LENGTH+1):
        for j in range(1, BOARD_COL_LENGTH+1):
            yield Point(i, j)


def get_opponent_stone_color(player_stone_color):
    return "W" if player_stone_color == "B" else "B"