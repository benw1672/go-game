import sys, os
sys.path.append(os.path.abspath('..'))
import utils
from .strategies import SimpleStrategy, PrioritizeCaptureStrategy


def make_player():
    return AIPlayer(strategy=SimpleStrategy())

class AIPlayer():
    def __init__(self, strategy=None):
        self.strategy = strategy
        self.name = None
        self.stone = None


    def register(self):
        self.name = "ai player"
        return self.name


    def receive_stones(self, stone: str):
        self.stone = stone


    def make_a_move(self, boards: list):
        return self.strategy.get_move(self.stone, boards)

    def end_game(self):
        return "OK"