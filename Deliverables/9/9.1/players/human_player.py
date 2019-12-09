import sys, os

sys.path.append(os.path.abspath('..'))
import utils
from .order_proxy_player import OrderProxyPlayer
from .history_check_proxy_player import HistoryCheckProxyPlayer
from .logging_proxy_player import LoggingProxyPlayer

def make_player():
    return LoggingProxyPlayer(HistoryCheckProxyPlayer(OrderProxyPlayer(HumanPlayer())))

class HumanPlayer(object):
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