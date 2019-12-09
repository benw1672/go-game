import sys, os

sys.path.append(os.path.abspath('..'))
import rule_checker as rc


class HistoryCheckProxyPlayer(object):
    def __init__(self, real_player):
        self.real_player = real_player
        self.stone = None

    def register(self):
        return self.real_player.register()

    def receive_stones(self, stone):
        self.stone = stone
        return self.real_player.receive_stones(stone)

    def make_a_move(self, boards):
        if not rc.is_history_legal(self.stone, boards):
            return "This history makes no sense!"
        else:
            return self.real_player.make_a_move(boards)

    def end_game(self):
        return self.real_player.end_game()

