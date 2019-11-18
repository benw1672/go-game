import sys, os

sys.path.append(os.path.abspath('..'))
from constants import *


class StateProxyPlayer():
    def __init__(self, real_player):
        self.real_player = real_player
        self.registered = False
        self.received_stone = False
        self.name = None


    def register(self):
        if not self.registered:
            self.registered = True
            name = self.real_player.register()
            self.name = name
            return name
        else:
            return GO_HAS_GONE_CRAZY


    def receive_stones(self, stone):
        if self.registered and not self.received_stone:
            self.received_stone = True
            return self.real_player.receive_stones(stone)
        else:
            return GO_HAS_GONE_CRAZY


    def make_a_move(self, boards):
        if self.registered and self.received_stone:
            return self.real_player.make_a_move(boards)
        else:
            return GO_HAS_GONE_CRAZY
