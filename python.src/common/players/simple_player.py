import sys, os, time

from common.constants import *
import common.rule_checker as rc
from common.players.order_proxy_player import OrderProxyPlayer
from common.players.history_check_proxy_player import HistoryCheckProxyPlayer
from common.players.player import Player

def make_player():
    return HistoryCheckProxyPlayer(OrderProxyPlayer(SimplePlayer()))

class SimplePlayer(Player):
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