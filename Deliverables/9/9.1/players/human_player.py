import sys, os

sys.path.append(os.path.abspath('..'))
import utils

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
        print(utils.jsonify(boards))
        text = input("make-a-move: ")
        return text


    def end_game(self):
        text = input("end-game: ")
        return text