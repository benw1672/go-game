# Import nonlocal dependencies.
import json, os, sys, typing

# Import local dependencies.
from constants import *
import rule_checker as rc
import utils


class Player():
    def __init__(self, strategy, name="no name", stone=None):
        self.strategy = strategy
        self.name = name
        self.stone = stone
        self.opponent_stone = None


    def __repr__(self):
        return 'Player name: "{}"; Player color: {}'.format(self.name, self.stone)


    def receive_stones(self, stone: str):
        if stone not in STONES:
            raise ValueError("not a valid stone")
        self.stone = stone
        self.opponent_stone = utils.get_opponent_stone_color(stone)


    def make_a_move(self, boards: list):
        return self.strategy.get_move(self.stone, boards)
