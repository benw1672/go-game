import sys, os, time

import common.rule_checker as rc
from common.constants import *
from common.players.order_proxy_player import OrderProxyPlayer
from common.players.history_check_proxy_player import HistoryCheckProxyPlayer
from common.players.player import Player
import common.utils as utils

def make_player():
    return HistoryCheckProxyPlayer(OrderProxyPlayer(PrioritizeCapturePlayer()))

class PrioritizeCapturePlayer(Player):
    def __init__(self):
        self.max_search_depth = 1
        self.name = None
        self.stone = None


    def register(self):
        self.name = "prioritize capture player " + str(time.time())
        return self.name


    def receive_stones(self, stone: str):
        self.stone = stone


    def make_a_move(self, boards):
        '''
        moves =
        [
            [point1, point2, ...] (from oldest to newest)
            ...
        ]
        [[(1,1)], []]
        '''
        # check if the board history makes sense
        if not rc.is_history_legal(self.stone, boards):
            return "This history makes no sense!"
        most_recent_board = boards[0]
        opponent_stone_color = utils.get_opponent_stone_color(self.stone)
        moves = []
        if self.max_search_depth == 1:
            chains = most_recent_board.get_all_chains()
            opponent_chains = [chain for chain in chains if chain.stone_color == opponent_stone_color]
            for chain in opponent_chains:
                if len(chain.liberties) == 1:
                    point = list(chain.liberties)[0]
                    if rc.is_new_move_legal(self.stone, (point, boards)):
                        moves.append(point)
        if self.max_search_depth > 1:
            # Idea: define new_move as [point()]
            # all_moves = generate_all_moves_that_d
            # return select_simple_move(boards)
            raise NotImplementedError()
        if moves:
            return sorted(moves, key=lambda p: (p.y, p.x))[0]
        else:
            # simple strategy if no capturing move can be found
            if not rc.is_history_legal(self.stone, boards):
                return "This history makes no sense!"

            for point, maybe_stone in iter(boards[0]):
                if maybe_stone == EMPTY:
                    new_move = (point, boards)
                    if rc.is_new_move_legal(self.stone, new_move):
                        return point
            return PASS

    def end_game(self):
        return "OK"