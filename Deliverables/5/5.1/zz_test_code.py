import operator
import constants
from point import Point
from board import Board


if __name__ == "__main__":
    board = Board()
    point = Point(1, 1)
    stone = constants.BLACK

    board[point] = stone
    print(board._grid)


def printout(a, b):
    print("value a:", a)
    print("value b:", b)