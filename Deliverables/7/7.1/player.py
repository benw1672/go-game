# Import nonlocal dependencies.
import json, os, sys, typing

# Import local dependencies.
from constants import *
import rule_checker as rc
import utils
from board import Board
from point import Point

GO_HAS_GONE_CRAZY = "GO has gone crazy!"

def isValidStone(stone):
    return isinstance(stone, str) and stone in STONES

def isValidMaybeStone(maybe_stone):
    return isinstance(maybe_stone, str) and maybe_stone in MAYBE_STONES

def isValidBoard(board):
    return (isinstance(board, Board)
            and len(board._grid) == BOARD_ROW_LENGTH
            and all(len(row) == BOARD_COL_LENGTH for row in board._grid)
            and all(isValidMaybeStone(stone) for point, stone in iter(board)))

def handle_player(player, json_expr):
    command, *args = json_expr
    if command == "register" and len(args) == 0:
        return player.register()
    elif command == "receive-stones" and len(args) == 1:
        return player.receive_stones(*args)
    elif command == "make-a-move" and len(args) == 1:
        boards = [Board(json_board) for json_board in args[0]]
        move = player.make_a_move(boards)
        if isinstance(move, str):
            return move
        elif isinstance(move, Point):
            return str(move)
    else:
        #print("INVALID COMMAND: " + command)
        return GO_HAS_GONE_CRAZY


class PlayerStateProxy():
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
            #print("receive stones called before register")
            return GO_HAS_GONE_CRAZY

    def make_a_move(self, boards):
        if self.registered and self.received_stone:
            return self.real_player.make_a_move(boards)
        else:
            #print("make_a_move called before register and receive_stones")
            return GO_HAS_GONE_CRAZY

class PlayerContractProxy():
    def __init__(self, real_player):
        self.real_player = real_player

    def register(self, name="no name"):
        return self.real_player.register(name)

    def receive_stones(self, stone):
        if isValidStone(stone):
            return self.real_player.receive_stones(stone)
        else:
            #print("not a valid stone: " + stone)
            return GO_HAS_GONE_CRAZY

    def make_a_move(self, boards):
        if len(boards) <= 3 and all(isValidBoard(board) for board in boards):
            return self.real_player.make_a_move(boards)
        else:
            #print("not valid boards")
            return GO_HAS_GONE_CRAZY


class Player():
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


    def make_a_move(self, boards: list):
        return self.strategy.get_move(self.stone, boards)
