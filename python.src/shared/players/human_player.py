import sys, os

from shared.players.order_proxy_player import OrderProxyPlayer
from shared.players.history_check_proxy_player import HistoryCheckProxyPlayer
from shared.players.logging_proxy_player import LoggingProxyPlayer
from shared.players.player import Player

def make_player():
    return LoggingProxyPlayer(HistoryCheckProxyPlayer(OrderProxyPlayer(HumanPlayer())))

class HumanPlayer(Player):
    def __init__(self):
        self.name = None
        self.stone = None


    def register(self):
        text = input("register: ")
        self.name = text
        return self.name


    def receive_stones(self, stone: str):
        print("receive-stones", stone)
        self.stone = stone


    def make_a_move(self, boards: list):
        text = input("make-a-move: ")
        return text


    def end_game(self):
        text = input("end-game: ")
        return text