import sys, os, random, time

from common.players.order_proxy_player import OrderProxyPlayer
from common.players.history_check_proxy_player import HistoryCheckProxyPlayer
from common.players.logging_proxy_player import LoggingProxyPlayer
from common.players.player import Player
from common.point import Point
from common.constants import *

def make_player():
    return LoggingProxyPlayer(HistoryCheckProxyPlayer(OrderProxyPlayer(RandomSometimesIllegalPlayer())))

class RandomSometimesIllegalPlayer(Player):
    def __init__(self):
        self.name = None
        self.stone = None


    def register(self):
        self.name = "random sometimes illegal player " + str(time.time())
        return self.name


    def receive_stones(self, stone: str):
        self.stone = stone


    def make_a_move(self, boards: list):
        x = random.randint(0, BOARD_ROW_LENGTH - 1)
        y = random.randint(0, BOARD_COL_LENGTH - 1)
        return Point(x, y)


    def end_game(self):
        return "OK"