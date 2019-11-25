import sys, os

from .strategies import SimpleStrategy
sys.path.append(os.path.abspath('..'))
import utils
from constants import *


def make_player():
    return DumbPlayer()


class DumbPlayer():
    def __init__(self):
        self.name = None
        self.stone = None


    def register(self):
        self.name = "dumb player"
        return self.name


    def receive_stones(self, stone: str):
        self.stone = stone


    def make_a_move(self, boards: list):
        return PASS

    def end_game(self):
        return "OK"