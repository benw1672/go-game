# Import nonlocal dependencies.
import json, jsonpickle, os, sys, typing

# Import local dependencies.
from constants import *
import rule_checker as rc
import utils
from board import Board
from point import Point

def isValidStone(stone):
    return isinstance(stone, str) and stone in STONES

def isValidMaybeStone(maybe_stone):
    return isinstance(maybe_stone, str) and maybe_stone in MAYBE_STONES

def isValidBoard(board):
    return (isinstance(board, Board)
            and len(board._grid) == BOARD_ROW_LENGTH
            and all(len(row) == BOARD_COL_LENGTH for row in board._grid)
            and all(isValidMaybeStone(stone) for point, stone in iter(board)))


def command_player(player, json_element):
    try:
        command_name, *args = utils.jsoncommand2internal(json_element)
    except ValueError:
        return GO_HAS_GONE_CRAZY
    if command_name == "register":
        return player.register()
    elif command_name == "receive-stones":
        return player.receive_stones(*args)
    elif command_name == "make-a-move":
        return player.make_a_move(*args)


class RemoteProxyPlayer():
    def __init__(self, connection):
        self.name = None
        self.stone = None
        self.connection = connection


    def register(self):
        command = ["register"]
        # Use the connection to get a move over the wire.
        self.connection.send(utils.jsonify(command).encode())
        json_response = json.loads(self.connection.recv(2048).decode())
        if not json_response:
            raise RuntimeError("Connection to client is broken.")
        self.name = json_response
        return self.name


    def receive_stones(self, stone):
        command = ["receive-stones", stone]
        self.connection.send(utils.jsonify(command).encode())
        json_response = json.loads(self.connection.recv(2048).decode())
        if not json_response == "OK":
            raise RuntimeError("Connection to client is broken.")
        return


    def make_a_move(self, boards):
        # Use the connection to get a move over the wire.
        command = ["make-a-move", boards]
        self.connection.send(utils.jsonify(command).encode())
        json_response = json.loads(self.connection.recv(2048).decode())
        if not json_response:
            raise RuntimeError("Connection to client is broken.")
        if json_response == PASS:
            return PASS
        else:
            return Point.from_str(json_response)


class StateProxyPlayer():
    def __init__(self, real_player):
        self.real_player = real_player
        self.registered = False
        self.received_stone = False

    def register(self, name="no name"):
        if not self.registered:
            self.registered = True
            return self.real_player.register(name)
        else:
            return GO_HAS_GONE_CRAZY

    def receive_stones(self, stone):
        if self.registered and not self.received_stone:
            self.received_stone = True
            return self.real_player.receive_stones(stone)
        else:
            return GO_HAS_GONE_CRAZY

    def make_a_move(self, boards):
        if self.registered and self.received_stone:
            return self.real_player.make_a_move(boards)
        else:
            return GO_HAS_GONE_CRAZY


class ContractProxyPlayer():
    def __init__(self, real_player):
        self.real_player = real_player

    def register(self, name="no name"):
        return self.real_player.register(name)

    def receive_stones(self, stone):
        if isValidStone(stone):
            return self.real_player.receive_stones(stone)
        else:
            return GO_HAS_GONE_CRAZY

    def make_a_move(self, boards):
        if len(boards) <= 3 and all(isValidBoard(board) for board in boards):
            return self.real_player.make_a_move(boards)
        else:
            return GO_HAS_GONE_CRAZY


class AIPlayer():
    def __init__(self, strategy=None, name="no name", stone=None):
        self.strategy = strategy
        self.name = name
        self.stone = stone
        self.opponent_stone = None


    def register(self, name="no name"):
        self.name = name
        return self.name


    def receive_stones(self, stone: str):
        self.stone = stone
        self.opponent_stone = utils.get_opponent_stone_color(stone)
        return "OK"


    def make_a_move(self, boards: list):
        return self.strategy.get_move(self.stone, boards)
