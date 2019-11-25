import sys, os, random

from .strategies import SimpleStrategy
sys.path.append(os.path.abspath('..'))
import utils
from constants import *
from point import Point


def make_player():
    return RandomAnyPlayer()


class RandomAnyPlayer(object):
    def __init__(self):
        self.name = None
        self.stone = None


    def register(self):
        #global identifier
        self.name = "random any player"
        return self.name


    def receive_stones(self, stone: str):
        self.stone = stone
        

    def make_a_move(self, boards: list):
        x = random.randint(0, BOARD_ROW_LENGTH-1)
        y = random.randint(0, BOARD_COL_LENGTH-1)
        return Point(x, y)


    def end_game(self):
        return "OK"