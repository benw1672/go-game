import sys, os, random
sys.path.append(os.path.abspath('..'))
import utils
from .order_proxy_player import OrderProxyPlayer
from .history_check_proxy_player import HistoryCheckProxyPlayer
from constants import *
from point import Point

def make_player():
    return HistoryCheckProxyPlayer(OrderProxyPlayer(RandomSometimesIllegalPlayer()))

class RandomSometimesIllegalPlayer():
    def __init__(self):
        self.name = None
        self.stone = None


    def register(self):
        self.name = "random sometimes illegal player"
        return self.name


    def receive_stones(self, stone: str):
        self.stone = stone


    def make_a_move(self, boards: list):
        x = random.randint(0, BOARD_ROW_LENGTH - 1)
        y = random.randint(0, BOARD_COL_LENGTH - 1)
        return Point(x, y)

    def end_game(self):
        return "OK"