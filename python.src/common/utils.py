import json, jsonpickle
# Import local dependencies.
from common.constants import *
from common.point import Point
from common.board import Board


# General utility functions.
def all_points():
    for i in range(1, BOARD_ROW_LENGTH+1):
        for j in range(1, BOARD_COL_LENGTH+1):
            yield Point(i, j)


def get_opponent_stone_color(player_stone_color):
    return "W" if player_stone_color == "B" else "B"


def jsonify(internal_object):
    return jsonpickle.encode(internal_object, unpicklable=False)


def jsoncommand2internal(json_element):
    if not json_element or not isinstance(json_element, list):
        raise ValueError("JSON command string is not valid.")
    command_name, *args = json_element
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
    elif command_name == "end-game":
        try:
            assert len(args) == 0
        except Exception:
            raise ValueError
        return [command_name]
    else:
        raise ValueError("JSON command string is not valid.")