import sys, os, time
sys.path.append(os.path.abspath('..'))
import utils
from constants import *
import rule_checker as rc
from .order_proxy_player import OrderProxyPlayer
from .history_check_proxy_player import HistoryCheckProxyPlayer

def make_player():
    return HistoryCheckProxyPlayer(OrderProxyPlayer(SimplePlayer()))

class SimplePlayer(object):
    def __init__(self):
        self.name = None
        self.stone = None


    def register(self):
        self.name = "simple player " + str(time.time())
        return self.name


    def receive_stones(self, stone: str):
        self.stone = stone


    def make_a_move(self, boards: list):
        for point, maybe_stone in iter(boards[0]):
            if maybe_stone == EMPTY:
                new_move = (point, boards)
                if rc.is_new_move_legal(self.stone, new_move):
                    return point
        return PASS


    def end_game(self):
        return "OK"