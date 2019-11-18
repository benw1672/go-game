from constants import *
from point import Point
from board import Board
import rule_checker as rc


class RegisterBlack(object):
    def act(self, container, results):
        name = container.black_player.register()
        container.results.append(name)
        container.next_action = RegisterWhite()


class RegisterWhite(object):
    def act(self, container, results):
        name = container.white_player.register()
        container.results.append(name)
        container.next_action = ReceiveStonesBlack()


class ReceiveStonesBlack(object):
    def act(self, container, results):
        container.black_player.receive_stones(BLACK)
        container.next_action = ReceiveStonesWhite()


class ReceiveStonesWhite(object):
    def act(self, container, results):
        container.white_player.receive_stones(WHITE)
        container.next_action = MakeAMoveBlack()


class MakeAMoveBlack(object):
    def act(self, container, results):
        container.results.append(container.boards)
        response = container.black_player.make_a_move(container.boards)
        if response == PASS and rc.is_move_legal(BLACK, PASS):
            if container.previous_move_was_pass:
                container.next_action = LegalEnd()
            else:
                container.previous_move_was_pass = True
                container.next_action = MakeAMoveWhite()
        elif isinstance(response, Point) and rc.is_move_legal(BLACK, (response, container.boards)):
            new_board = rc._get_board_if_valid_play(container.boards[0], BLACK, response)
            container.boards = [new_board, *container.boards[0:2]]
            container.next_action = MakeAMoveWhite()
        else:
            container.next_action = BlackIllegalMove()


class MakeAMoveWhite(object):
    def act(self, container, results):
        container.results.append(container.boards)
        response = container.white_player.make_a_move(container.boards)
        if response == PASS and rc.is_move_legal(WHITE, PASS):
            if container.previous_move_was_pass:
                container.next_action = LegalEnd()
            else:
                container.previous_move_was_pass = True
                container.next_action = MakeAMoveBlack()
        elif isinstance(response, Point) and rc.is_move_legal(WHITE, (response, container.boards)):
            new_board = rc._get_board_if_valid_play(container.boards[0], WHITE, response)
            container.boards = [new_board, *container.boards[0:2]]
            container.next_action = MakeAMoveBlack()
        else:
            container.next_action = WhiteIllegalMove()


class BlackIllegalMove(object):
    def act(self, container):
        container.results.append([container.white_player.name])


class WhiteIllegalMove(object):
    def act(self, container):
        container.results.append([container.black_player.name])


class LegalEnd(object):
    def act(self, container):
        scores = rc.get_scores(container.board[0])
        if scores["B"] > scores["W"]:
            container.results.append([container.black_player.name])
        elif scores["W"] > scores["B"]:
            container.results.append([container.white_player.name])
        else:
            container.results.append([container.black_player.name,
                                        container.white_player.name])


class GameStateContainer(object):
    def __init__(self, black_player, white_player):
        self.next_action = RegisterBlack()
        self.black_player = black_player
        self.white_player = white_player
        self.boards = [Board()]
        self.results = []
        self.previous_move_was_pass = False

    
    def act(self, *args):
        self.next_action.act(self, *args)


    def get_results(self):
        return self.results