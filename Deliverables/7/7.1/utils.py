# Import local dependencies.
from constants import *
from point import Point
import json, jsonpickle
from board import Board

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


def jsonify(internal_object):
    return jsonpickle.encode(internal_object, unpicklable=False)


def jsoncommand2internal(python_repr):
    if not python_repr or not isinstance(python_repr, list):
        raise ValueError("JSON command string is not valid.")
    command_name, *args = python_repr
    if command_name == "make-a-move":
        try:
            assert len(args) == 1
            boards = [Board(json_board) for json_board in args[0]]
        except Exception:
            raise ValueError("JSON command string is not valid make-a-move command")
        return [command_name, boards]
    elif command_name == "register":
        try:
            assert len(args) == 0
        except Exception:
            raise ValueError
        return [command_name]
    elif command_name == "receive-stones":
        try:
            assert len(args) == 1
            assert args[0] in STONES
        except Exception:
            raise ValueError
        return [command_name, *args]
    else:
        raise ValueError("JSON command string is not valid.")