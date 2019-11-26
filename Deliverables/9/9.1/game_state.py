from constants import *
from point import Point
from board import Board
import rule_checker as rc
from game_result import GameResult


class ReceiveStonesBlack(object):
    def act(self, container):
        try:
            container.black_player.receive_stones(BLACK)
            container.next_action = ReceiveStonesWhite()
        except RuntimeError:
            container.next_action = BlackIllegalMove()


class ReceiveStonesWhite(object):
    def act(self, container):
        try:
            container.white_player.receive_stones(WHITE)
            container.next_action = MakeAMoveBlack()
        except:
            container.next_action = WhiteIllegalMove()


class MakeAMoveBlack(object):
    def act(self, container):
        try:
            response = container.black_player.make_a_move(container.boards)
            if response == PASS and rc.is_move_legal(BLACK, PASS):
                if container.previous_move_was_pass:
                    container.next_action = LegalEnd()
                else:
                    container.previous_move_was_pass = True
                    container.boards = [container.boards[0], *container.boards[0:2]]
                    container.next_action = MakeAMoveWhite()
            elif isinstance(response, Point) and rc.is_move_legal(BLACK, (response, container.boards)):
                container.previous_move_was_pass = False
                new_board = rc.get_board_if_valid_play(container.boards[0], BLACK, response)
                container.boards = [new_board, *container.boards[0:2]]
                container.next_action = MakeAMoveWhite()
            else:
                container.next_action = BlackIllegalMove()
        except RuntimeError:
            container.next_action = BlackIllegalMove()


class MakeAMoveWhite(object):
    def act(self, container):
        try:
            response = container.white_player.make_a_move(container.boards)
            if response == PASS and rc.is_move_legal(WHITE, PASS):
                if container.previous_move_was_pass:
                    container.next_action = LegalEnd()
                else:
                    container.previous_move_was_pass = True
                    container.boards = [container.boards[0], *container.boards[0:2]]
                    container.next_action = MakeAMoveBlack()
            elif isinstance(response, Point) and rc.is_move_legal(WHITE, (response, container.boards)):
                container.previous_move_was_pass = False
                new_board = rc.get_board_if_valid_play(container.boards[0], WHITE, response)
                container.boards = [new_board, *container.boards[0:2]]
                container.next_action = MakeAMoveBlack()
            else:
                container.next_action = WhiteIllegalMove()
        except RuntimeError:
            container.next_action = WhiteIllegalMove()


class BlackIllegalMove(object):
    def act(self, container):
        try:
            container.black_player.end_game()
        except RuntimeError:
            pass
        try:
            container.white_player.end_game()
        except RuntimeError:
            pass
        container.game_result = GameResult(winner=container.white_player,
                                        loser=container.black_player,
                                        game_was_draw=False,
                                        loser_was_cheating=True)


class WhiteIllegalMove(object):
    def act(self, container):
        try:
            container.black_player.end_game()
        except RuntimeError:
            pass
        try:
            container.white_player.end_game()
        except RuntimeError:
            pass
        container.game_result = GameResult(winner=container.black_player,
                                        loser=container.white_player,
                                        game_was_draw=False,
                                        loser_was_cheating=True)


class LegalEnd(object):
    def act(self, container):
        try:
            container.black_player.end_game()
        except RuntimeError:
            container.next_action = BlackIllegalMove()
            return

        try:
            container.white_player.end_game()
        except RuntimeError:
            container.next_action = WhiteIllegalMove()
            return
            
        scores = rc.get_scores(container.boards[0])
        if scores["B"] > scores["W"]:
            container.game_result = GameResult(winner=container.black_player,
                                            loser=container.white_player,
                                            game_was_draw=False,
                                            loser_was_cheating=False)
        elif scores["W"] > scores["B"]:
            container.game_result = GameResult(winner=container.white_player,
                                            loser=container.black_player,
                                            game_was_draw=False,
                                            loser_was_cheating=False)
        else:
            container.game_result = GameResult(winner=None,
                                            loser=None,
                                            game_was_draw=True,
                                            loser_was_cheating=False)


class GameStateContainer(object):
    def __init__(self, black_player, white_player):
        self.next_action = ReceiveStonesBlack()
        self.black_player = black_player
        self.white_player = white_player
        self.boards = [Board()]
        self.previous_move_was_pass = False
        self.game_result = None

    
    def act(self, *args):
        self.next_action.act(self, *args)