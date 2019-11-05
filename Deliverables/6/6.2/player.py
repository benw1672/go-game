# Import nonlocal dependencies.
import json, os, sys, typing

# Import local dependencies.
from constants import *
from rule_checker import RuleChecker
import go_utils


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
        self.opponent_stone = go_utils.get_opponent_stone_color(stone)


    def make_a_move(self, boards: list):
        rc = RuleChecker()
        try:
            for board in boards:
                rc.validate_board(board)
        except:
            return "Invalid boards."

        if not rc.check_history(self.stone, boards):
            return "This history makes no sense!"

        return self.strategy.execute(self.stone, boards)


    def sort_points(self, points: list):
        '''
        input: list of (row, col)
        output: sorted list of (row, col)
            with col having higher priority
        '''
        def reversekey(x):
            return (x[1], x[0])
        return sorted(points, key=reversekey)