import sys, os
sys.path.append(os.path.abspath('..'))
import utils

class AIPlayer():
    def __init__(self, strategy=None):
        self.strategy = strategy
        self.name = None
        self.stone = None
        self.opponent_stone = None


    def register(self):
        self.name = "no name"
        return self.name


    def receive_stones(self, stone: str):
        self.stone = stone
        self.opponent_stone = utils.get_opponent_stone_color(stone)
        return "OK"


    def make_a_move(self, boards: list):
        return self.strategy.get_move(self.stone, boards)
